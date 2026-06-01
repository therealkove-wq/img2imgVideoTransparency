"""
Wan-Alpha Custom Nodes for ComfyUI
Provides nodes for generating videos with transparency using Wan-Alpha model
"""

import os
import torch
import numpy as np
from PIL import Image
from typing import Union, Tuple, List, Dict, Any
from pathlib import Path
import folder_paths
import node_helpers

class WanAlphaVideoGenerator:
    """
    Generates RGBA videos using the Wan 2.1 model with the RGBA LoRA.
    Loads the real Wan-Alpha pipeline on first run and caches it.
    """

    _wan_model = None
    _wan_clip  = None
    _wan_vae_rgb   = None
    _wan_vae_alpha = None
        
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "first_frame": ("IMAGE",),
                "first_mask": ("MASK",),
                "last_frame": ("IMAGE",),
                "last_mask": ("MASK",),
                "text_prompt": ("STRING", {
                    "multiline": True,
                    "default": "This video has a transparent background. "
                }),
                "frame_count": ("INT", {
                    "default": 24,
                    "min": 8,
                    "max": 256,
                    "step": 8,
                }),
                "height": ("INT", {
                    "default": 480,
                    "min": 256,
                    "max": 1024,
                    "step": 64,
                }),
                "width": ("INT", {
                    "default": 832,
                    "min": 256,
                    "max": 1024,
                    "step": 64,
                }),
                "steps": ("INT", {
                    "default": 4,
                    "min": 1,
                    "max": 50,
                    "step": 1,
                }),
                "guidance_scale": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 10.0,
                    "step": 0.1,
                }),
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 0xffffffffffffffff,
                }),
            },
            "optional": {
                "use_fp16": ("BOOLEAN", {"default": True}),
                "use_vae_guidance": ("BOOLEAN", {"default": True}),
                "alpha_shift_mean": ("FLOAT", {
                    "default": 0.05,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                }),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("video_frames",)
    FUNCTION = "generate_video"
    CATEGORY = "video/wan_alpha"
    
    def generate_video(
        self,
        first_frame: torch.Tensor,
        first_mask: torch.Tensor,
        last_frame: torch.Tensor,
        last_mask: torch.Tensor,
        text_prompt: str,
        frame_count: int,
        height: int,
        width: int,
        steps: int,
        guidance_scale: float,
        seed: int,
        use_fp16: bool = True,
        use_vae_guidance: bool = True,
        alpha_shift_mean: float = 0.05,
    ) -> Tuple[torch.Tensor,]:
        """
        Generate video frames with transparency using Wan-Alpha model.
        
        Args:
            first_frame: Starting frame as IMAGE tensor
            last_frame: Ending frame as IMAGE tensor
            text_prompt: Text description of video content
            frame_count: Number of frames to generate
            height: Output video height
            width: Output video width
            steps: Number of inference steps
            guidance_scale: Guidance scale for conditioning
            seed: Random seed for reproducibility
            use_fp16: Use half-precision for faster inference
            use_vae_guidance: Use VAE-based guidance
            alpha_shift_mean: Alpha shift parameter for transparency
            
        Returns:
            Tuple containing generated video frames as IMAGE tensor
        """
        
        import comfy.sd
        import comfy.sample
        import comfy.utils
        import comfy.model_management

        if not torch.cuda.is_available():
            raise RuntimeError("CUDA GPU is required for Wan-Alpha generation")

        # ── Load models (first call only) ──────────────────────────────────
        if WanAlphaVideoGenerator._wan_model is None:
            self._load_wan_models()

        model     = WanAlphaVideoGenerator._wan_model
        clip      = WanAlphaVideoGenerator._wan_clip
        vae_rgb   = WanAlphaVideoGenerator._wan_vae_rgb
        vae_alpha = WanAlphaVideoGenerator._wan_vae_alpha

        # ── Text conditioning ──────────────────────────────────────────────
        tokens_pos = clip.tokenize(text_prompt)
        cond_pos, pool_pos = clip.encode_from_tokens(tokens_pos, return_pooled=True)
        positive = [[cond_pos, {"pooled_output": pool_pos}]]

        tokens_neg = clip.tokenize("")
        cond_neg, pool_neg = clip.encode_from_tokens(tokens_neg, return_pooled=True)
        negative = [[cond_neg, {"pooled_output": pool_neg}]]

        # ── First + last frame conditioning (WanFirstLastFrameToVideo approach) ─
        sp = vae_rgb.spacial_compression_encode()   # typically 8
        lat_ch = vae_rgb.latent_channels            # typically 16
        T = ((frame_count - 1) // 4) + 1

        start = comfy.utils.common_upscale(
            first_frame.movedim(-1, 1), width, height, "bilinear", "center"
        ).movedim(1, -1)   # [1, H, W, 3]

        end = comfy.utils.common_upscale(
            last_frame.movedim(-1, 1), width, height, "bilinear", "center"
        ).movedim(1, -1)   # [1, H, W, 3]

        img_seq = torch.ones((frame_count, height, width, 3)) * 0.5
        img_seq[: start.shape[0]] = start           # anchor first frame
        img_seq[-end.shape[0]:] = end               # anchor last frame

        # Mask: temporal dimension at 4× resolution then fold back to latent T
        H8, W8 = height // sp, width // sp
        mask = torch.ones((1, 1, T * 4, H8, W8))
        mask[:, :, : start.shape[0] + 3] = 0.0     # unmask start region
        mask[:, :, -end.shape[0]:] = 0.0           # unmask end region
        # reshape to latent temporal dimension: [1, 4, T, H8, W8]
        mask = mask.view(1, T, 4, H8, W8).transpose(1, 2)   # [1, 4, T, H8, W8]

        concat_lat = vae_rgb.encode(img_seq[:, :, :, :3])    # [1, lat_ch, T, H8, W8]

        positive = node_helpers.conditioning_set_values(
            positive, {"concat_latent_image": concat_lat, "concat_mask": mask}
        )
        negative = node_helpers.conditioning_set_values(
            negative, {"concat_latent_image": concat_lat, "concat_mask": mask}
        )

        # ── Latent noise ───────────────────────────────────────────────────
        dev = comfy.model_management.intermediate_device()
        latent_samples = torch.zeros([1, lat_ch, T, H8, W8], device=dev)
        latent = {"samples": latent_samples}

        noise = comfy.sample.prepare_noise(latent_samples, seed, None)

        # ── Diffusion sampling ─────────────────────────────────────────────
        print(f"[wan_alpha] Sampling {frame_count} frames, steps={steps}, cfg={guidance_scale}")
        # comfy.sample.sample expects the raw latent tensor, not a dict, and returns a raw tensor
        latent_tensor = comfy.sample.sample(
            model, noise, steps, guidance_scale,
            "euler", "linear_quadratic",
            positive, negative, latent_samples,
            denoise=1.0, force_full_denoise=True,
            disable_pbar=False,
        )

        # ── Dual-VAE decode ────────────────────────────────────────────────
        print("[wan_alpha] Decoding RGB frames...")
        rgb_frames = vae_rgb.decode(latent_tensor)
        print(f"[wan_alpha] rgb_frames raw shape: {rgb_frames.shape}")
        print("[wan_alpha] Decoding alpha frames...")
        alpha_raw  = vae_alpha.decode(latent_tensor)
        print(f"[wan_alpha] alpha_raw raw shape: {alpha_raw.shape}")

        # Flatten to [N, H, W, C] regardless of what the VAE returned
        def to_nhwc(t):
            while t.ndim > 4:
                t = t.reshape(-1, *t.shape[-3:])
            if t.ndim == 3:
                t = t.unsqueeze(0)
            return t

        rgb_frames = to_nhwc(rgb_frames)
        alpha_raw  = to_nhwc(alpha_raw)
        print(f"[wan_alpha] after reshape — rgb: {rgb_frames.shape}  alpha: {alpha_raw.shape}")

        if alpha_raw.shape[-1] > 1:
            alpha_ch = alpha_raw.mean(dim=-1, keepdim=True)
        else:
            alpha_ch = alpha_raw
        alpha_ch = alpha_ch.clamp(0.0, 1.0)

        rgba = torch.cat([rgb_frames.clamp(0.0, 1.0), alpha_ch], dim=-1)
        print(f"[wan_alpha] Done. rgba shape={rgba.shape}, alpha range {alpha_ch.min():.3f}-{alpha_ch.max():.3f}")
        return (rgba,)

    @classmethod
    def _load_wan_models(cls):
        import comfy.sd, comfy.utils
        from comfy.sd import CLIPType

        print("[wan_alpha] Loading Wan-Alpha models (first run – this takes several minutes)...")

        # ── Wan 2.1 T2V base model ─────────────────────────────────────────
        model_path = folder_paths.get_full_path("diffusion_models", "wan2.1_t2v_14B_fp16.safetensors")
        if not model_path:
            raise RuntimeError("wan2.1_t2v_14B_fp16.safetensors not found in diffusion_models")
        print("[wan_alpha] Loading DiT model...")
        model = comfy.sd.load_diffusion_model(model_path)

        # ── RGBA LoRA ──────────────────────────────────────────────────────
        for lora_name in [
            "wan/wan_alpha_2.1_rgba_lora.safetensors",
            "wan/epoch-13-1500_changed.safetensors",
        ]:
            lora_path = folder_paths.get_full_path("loras", lora_name)
            if lora_path:
                print(f"[wan_alpha] Applying RGBA LoRA: {lora_name}")
                lora_data = comfy.utils.load_torch_file(lora_path)
                model, _ = comfy.sd.load_lora_for_models(model, None, lora_data, 1.0, 0.0)
                break
        else:
            print("[wan_alpha] WARNING: RGBA LoRA not found – output will be RGB only")

        # ── LightX2V step-distillation LoRA (enables CFG=1.0, 4-step generation) ──
        for lora_name in [
            "wan/lightx2v_T2V_14B_cfg_step_distill_v2_lora_rank64_bf16.safetensors",
            "wan/Wan21_T2V_14B_lightx2v_cfg_step_distill_lora_rank32.safetensors",
        ]:
            lora_path = folder_paths.get_full_path("loras", lora_name)
            if lora_path:
                print(f"[wan_alpha] Applying LightX2V LoRA: {lora_name}")
                lora_data = comfy.utils.load_torch_file(lora_path)
                model, _ = comfy.sd.load_lora_for_models(model, None, lora_data, 1.0, 0.0)
                break
        else:
            print("[wan_alpha] WARNING: LightX2V LoRA not found – increase steps to 20+ and cfg to 5.0")

        # ── UMT5 text encoder ──────────────────────────────────────────────
        for enc_name in ["umt5_xxl_fp8_e4m3fn_scaled.safetensors", "umt5_xxl_fp16.safetensors"]:
            clip_path = folder_paths.get_full_path("text_encoders", enc_name)
            if clip_path:
                break
        else:
            raise RuntimeError("UMT5 text encoder not found in text_encoders folder")
        print(f"[wan_alpha] Loading text encoder: {enc_name}")
        clip = comfy.sd.load_clip(
            ckpt_paths=[clip_path],
            embedding_directory=folder_paths.get_folder_paths("embeddings"),
            clip_type=CLIPType.WAN,
        )

        # ── RGB VAE decoder ────────────────────────────────────────────────
        vae_rgb_path = folder_paths.get_full_path(
            "vae", "wan_alpha_2.1_vae_rgb_channel.safetensors.safetensors"
        )
        if not vae_rgb_path:
            raise RuntimeError("wan_alpha_2.1_vae_rgb_channel VAE not found")
        sd_rgb, meta_rgb = comfy.utils.load_torch_file(vae_rgb_path, return_metadata=True)
        vae_rgb = comfy.sd.VAE(sd=sd_rgb, metadata=meta_rgb)

        # ── Alpha VAE decoder ──────────────────────────────────────────────
        vae_alpha_path = folder_paths.get_full_path(
            "vae", "wan_alpha_2.1_vae_alpha_channel.safetensors.safetensors"
        )
        if not vae_alpha_path:
            raise RuntimeError("wan_alpha_2.1_vae_alpha_channel VAE not found")
        sd_alp, meta_alp = comfy.utils.load_torch_file(vae_alpha_path, return_metadata=True)
        vae_alpha = comfy.sd.VAE(sd=sd_alp, metadata=meta_alp)

        cls._wan_model     = model
        cls._wan_clip      = clip
        cls._wan_vae_rgb   = vae_rgb
        cls._wan_vae_alpha = vae_alpha
        print("[wan_alpha] All models loaded.")


class FrameRateCalculator:
    """Calculate frame duration and playback parameters."""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "frame_count": ("INT", {"default": 24}),
                "frame_rate": ("INT", {
                    "default": 24,
                    "min": 1,
                    "max": 120,
                    "step": 1,
                }),
            }
        }
    
    RETURN_TYPES = ("INT", "INT", "FLOAT", "STRING")
    RETURN_NAMES = ("frame_rate", "duration_ms", "duration_seconds", "info_string")
    FUNCTION = "calculate"
    CATEGORY = "video/wan_alpha"

    def calculate(self, frame_count: int, frame_rate: int) -> Tuple[int, int, float, str]:
        """Calculate video duration parameters."""
        duration_seconds = frame_count / frame_rate
        duration_ms = int(duration_seconds * 1000)

        minutes = int(duration_seconds // 60)
        seconds = int(duration_seconds % 60)

        info = f"{frame_count} frames @ {frame_rate}fps = {minutes}m {seconds}s"

        return (frame_rate, duration_ms, duration_seconds, info)


class ImageLoaderForVideo:
    """Load RGBA image, returning IMAGE (RGB) and MASK (alpha) separately."""

    @classmethod
    def INPUT_TYPES(cls):
        import folder_paths
        input_dir = folder_paths.get_input_directory()
        files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
        return {
            "required": {
                "image": (sorted(files),),
            }
        }

    RETURN_TYPES = ("IMAGE", "MASK")
    RETURN_NAMES = ("image", "mask")
    FUNCTION = "load_image"
    CATEGORY = "video/wan_alpha"

    def load_image(self, image: str) -> Tuple[torch.Tensor, torch.Tensor]:
        import folder_paths

        image_path = folder_paths.get_annotated_filepath(image)
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")

        rgba = np.array(Image.open(image_path).convert("RGBA")).astype(np.float32) / 255.0
        # IMAGE: RGB [1, H, W, 3]
        rgb_tensor = torch.from_numpy(rgba[:, :, :3]).unsqueeze(0)
        # MASK: inverted alpha [1, H, W]  (ComfyUI convention: 0=opaque, 1=transparent)
        mask_tensor = torch.from_numpy(1.0 - rgba[:, :, 3]).unsqueeze(0)
        return (rgb_tensor, mask_tensor)


_FFMPEG_SEARCH_PATHS = [
    r"C:\Program Files\Virtual Desktop Streamer\ffmpeg.exe",
    r"C:\Program Files\Krita (x64)\bin\ffmpeg.exe",
    r"C:\ffmpeg\bin\ffmpeg.exe",
    r"C:\Program Files\ffmpeg\bin\ffmpeg.exe",
]

def _find_ffmpeg() -> str:
    """Return path to an ffmpeg binary that has libvpx-vp9 support."""
    import shutil, subprocess
    candidates = []
    # imageio-ffmpeg bundles a known-good FFmpeg — try it first
    try:
        import imageio_ffmpeg
        candidates.append(imageio_ffmpeg.get_ffmpeg_exe())
    except ImportError:
        pass
    which = shutil.which("ffmpeg")
    if which:
        candidates.append(which)
    candidates.extend(_FFMPEG_SEARCH_PATHS)
    for path in candidates:
        if not os.path.isfile(path):
            continue
        try:
            result = subprocess.run(
                [path, "-encoders"],
                capture_output=True, text=True, timeout=10
            )
            if "libvpx-vp9" in result.stdout or "libvpx-vp9" in result.stderr:
                return path
        except Exception:
            continue
    return ""


class SaveWebmWithAlpha:
    """Save RGBA video frames as VP9 WebM with alpha channel via FFmpeg."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video_frames": ("IMAGE",),
                "filename": ("STRING", {
                    "default": "video_with_alpha"
                }),
                "frame_rate": ("INT", {
                    "default": 24,
                    "min": 1,
                    "max": 120,
                    "step": 1,
                }),
                "codec": (["VP9", "VP8"],),
                "quality": ("INT", {
                    "default": 80,
                    "min": 1,
                    "max": 100,
                    "step": 1,
                }),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("filepath",)
    FUNCTION = "save_webm"
    CATEGORY = "video/wan_alpha"
    OUTPUT_NODE = True

    def save_webm(
        self,
        video_frames: torch.Tensor,
        filename: str,
        frame_rate: int,
        codec: str = "VP9",
        quality: int = 80,
    ) -> Tuple[str,]:
        import folder_paths, subprocess, tempfile, shutil
        from PIL import Image as PILImage

        ffmpeg = _find_ffmpeg()
        if not ffmpeg:
            raise RuntimeError(
                "FFmpeg with libvpx-vp9 not found. Install FFmpeg and add it to PATH, "
                "or place ffmpeg.exe in one of: " + ", ".join(_FFMPEG_SEARCH_PATHS)
            )

        output_dir = folder_paths.get_output_directory()
        for ext in (".webm", ".webp", ".png"):
            if filename.endswith(ext):
                filename = filename[: -len(ext)]
        output_path = os.path.join(output_dir, f"{filename}.webm")

        if isinstance(video_frames, torch.Tensor):
            frames_np = video_frames.cpu().numpy()
        else:
            frames_np = np.array(video_frames)

        if frames_np.max() <= 1.0:
            frames_np = (frames_np * 255).astype(np.uint8)
        else:
            frames_np = frames_np.astype(np.uint8)

        # Collapse any leading batch/temporal wrapper dims → [N, H, W, C]
        # VAE video decode can return [1, N, H, W, C] or [N, H, W, C] etc.
        while frames_np.ndim > 4:
            frames_np = frames_np.reshape(-1, *frames_np.shape[-3:])
        if frames_np.ndim == 3:
            frames_np = frames_np[np.newaxis]

        print(f"[wan_alpha] save_webm frames shape={frames_np.shape} dtype={frames_np.dtype}")
        if frames_np.shape[-1] == 4:
            a = frames_np[..., 3]
            print(f"[wan_alpha] alpha channel: min={a.min()} max={a.max()} transparent_px={(a < 128).sum()} total_px={a.size}")
        else:
            print(f"[wan_alpha] WARNING: only {frames_np.shape[-1]} channels - NO alpha channel present")

        # quality 1-100 -> crf 63-1  (lower crf = better quality)
        crf = max(1, int(63 - (quality / 100.0) * 62))

        tmp_dir = tempfile.mkdtemp(prefix="wan_alpha_")
        try:
            for i in range(frames_np.shape[0]):
                frame = frames_np[i]  # [H, W, C]
                if frame.ndim != 3:
                    frame = frame.reshape(*frame.shape[-3:])
                channels = frame.shape[-1]
                if channels == 4:
                    img = PILImage.fromarray(frame, "RGBA")
                elif channels == 3:
                    img = PILImage.fromarray(frame, "RGB").convert("RGBA")
                else:
                    raise ValueError(f"Unexpected channel count: {channels}")
                img.save(os.path.join(tmp_dir, f"frame_{i:06d}.png"))

            # Two-stream VP9 WebM alpha: stream 0 = color (yuv420p),
            # stream 1 = alpha matte (grayscale VP9) via alphaextract filter.
            # This is the only approach that produces a WebM browsers can decode
            # with transparency.
            cmd = [
                ffmpeg, "-y",
                "-framerate", str(frame_rate),
                "-i", os.path.join(tmp_dir, "frame_%06d.png"),
                "-filter_complex",
                "[0:v]split[c][tmp];[tmp]alphaextract[a]",
                "-map", "[c]", "-map", "[a]",
                "-c:v", "libvpx-vp9",
                "-auto-alt-ref", "0",
                "-b:v", "0",
                "-crf", str(crf),
                output_path,
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                raise RuntimeError(f"FFmpeg failed:\n{result.stderr[-2000:]}")
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)

        print(f"Saved {frames_np.shape[0]} RGBA frames @ {frame_rate}fps to {output_path}")
        return (output_path,)


class RembgBackgroundRemover:
    """Remove background from image/video frames using rembg AI, returning RGBA."""

    _session = None
    _session_model = None

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "model": (["u2net", "u2netp", "u2net_human_seg", "isnet-general-use", "isnet-anime"],),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("rgba_images",)
    FUNCTION = "remove_background"
    CATEGORY = "video/wan_alpha"

    def remove_background(self, images: torch.Tensor, model: str = "u2net") -> Tuple[torch.Tensor,]:
        from rembg import remove, new_session
        from PIL import Image as PILImage

        if RembgBackgroundRemover._session is None or RembgBackgroundRemover._session_model != model:
            print(f"[wan_alpha] rembg: loading session '{model}'...")
            RembgBackgroundRemover._session = new_session(model)
            RembgBackgroundRemover._session_model = model

        session = RembgBackgroundRemover._session
        frames_np = images.cpu().numpy()
        if frames_np.max() <= 1.0:
            frames_np = (frames_np * 255).astype(np.uint8)

        rgba_frames = []
        n = frames_np.shape[0]
        for i in range(n):
            if i % 10 == 0:
                print(f"[wan_alpha] rembg: frame {i+1}/{n}")
            frame = frames_np[i]
            pil_img = PILImage.fromarray(frame, "RGBA" if frame.shape[-1] == 4 else "RGB")
            rgba_pil = remove(pil_img, session=session)
            rgba_frames.append(np.array(rgba_pil).astype(np.float32) / 255.0)

        out = torch.from_numpy(np.stack(rgba_frames, axis=0))
        print(f"[wan_alpha] rembg: done — shape {out.shape}, alpha range {out[...,3].min():.3f}-{out[...,3].max():.3f}")
        return (out,)


# Node class mappings for ComfyUI
NODE_CLASS_MAPPINGS = {
    "WanAlphaVideoGenerator": WanAlphaVideoGenerator,
    "FrameRateCalculator": FrameRateCalculator,
    "ImageLoaderForVideo": ImageLoaderForVideo,
    "SaveWebmWithAlpha": SaveWebmWithAlpha,
    "RembgBackgroundRemover": RembgBackgroundRemover,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "WanAlphaVideoGenerator": "Wan-Alpha Video Generator",
    "FrameRateCalculator": "Frame Rate Calculator",
    "ImageLoaderForVideo": "Image Loader (Video)",
    "SaveWebmWithAlpha": "Save WebM with Alpha",
    "RembgBackgroundRemover": "Remove Background (rembg)",
}
