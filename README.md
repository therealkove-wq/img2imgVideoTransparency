# img2img Transparent Video — ComfyUI Workflow

Generates videos with a transparent background (WEBM + alpha channel) from a start and end frame using **Wan 2.2 I2V** with **LightX2V LoRAs** and **rembg AI** background removal.

---

## How it works

1. You provide a start frame and an end frame (PNG images)
2. The model generates the in-between frames
3. rembg AI strips the background from every frame
4. Output is a WEBM file with a real alpha channel, ready for compositing

---

## Required Models

All models are from [Comfy-Org/Wan_2.2_ComfyUI_Repackaged](https://huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged) on HuggingFace.

| File | Destination folder |
|------|--------------------|
| `wan2.2_i2v_high_noise_14B_fp8_scaled.safetensors` | `ComfyUI/models/diffusion_models/` |
| `wan2.2_i2v_low_noise_14B_fp8_scaled.safetensors` | `ComfyUI/models/diffusion_models/` |
| `wan2.2_i2v_lightx2v_4steps_lora_v1_high_noise.safetensors` | `ComfyUI/models/loras/wan/` |
| `wan2.2_i2v_lightx2v_4steps_lora_v1_low_noise.safetensors` | `ComfyUI/models/loras/wan/` |
| `umt5_xxl_fp8_e4m3fn_scaled.safetensors` | `ComfyUI/models/text_encoders/` |
| `wan_2.1_vae.safetensors` | `ComfyUI/models/vae/` |

> The workflow will show download buttons for missing models directly in ComfyUI.

---

## Custom Node Setup

Two custom node packages are required.

### 1. wan_alpha_nodes (this repo)

Provides the `SaveWebmWithAlpha` node used to export the final video.

Copy the two files from this repo into ComfyUI:

```
ComfyUI/custom_nodes/wan_alpha_nodes/
├── wan_alpha_nodes.py
└── __init__.py
```

### 2. ComfyUI-rembg

Provides the `RembgBackgroundRemover` node used for AI background removal. Install it via ComfyUI Manager or clone it into `ComfyUI/custom_nodes/`.

---

## Using the Workflow

1. Open ComfyUI and load `kove_img_to_img_transparent.json`
2. In the **Start Frame** node, upload your starting image
3. In the **End Frame** node, upload your ending image
4. Edit the **Positive Prompt** (see Prompting section below)
5. In the **WAN I2V Conditioning** node, set **width**, **height**, and **length** (frame count)
6. In the **Save** node, set your output **filename** and **frame rate**
7. Click Queue

The output WEBM file will appear in `ComfyUI/output/`.

---

## Key Parameters

| Parameter | Node | Notes |
|-----------|------|-------|
| Width / Height | WAN I2V Conditioning | Resolution of the output video. Default: 1024×1024 |
| Length | WAN I2V Conditioning | Number of frames. 61 frames @ 30 FPS ≈ 2 seconds |
| Filename | Save | Output file name. **Existing files with the same name are overwritten without warning.** |
| Frame Rate | Save | Playback FPS of the output WEBM |
| Codec | Save | VP8 (faster) or VP9 (better compression) |
| Quality | Save | 0–100. Default 20 is a good starting point |

---

## Prompting

Always include this phrase in the positive prompt:

> **"The character is isolated against a transparent background."**

Without it, rembg has less context and background removal quality drops.

The negative prompt is pre-filled with `blurry, distorted, low quality, static, no motion` — leave it as-is unless you have a specific reason to change it.

### Example prompts

**Idle character animation**
```
The character is isolated against a transparent background.
The lighting is constant and even throughout the sequence.
The character breathes gently and sways slightly from side to side.
Hair and clothing move subtly with the sway.
The character does not speak. Slow movements. Idle animation.
```

**Floating object**
```
The character is isolated against a transparent background.
A glowing orb floats gently up and down. Soft pulsing light. Smooth looping motion.
```

**Abstract effect**
```
The character is isolated against a transparent background.
Colorful particles swirl and drift slowly. Ethereal. Cinematic quality.
```

---

## Troubleshooting

**Nodes missing after loading the workflow**
- Confirm both custom node packages are installed and ComfyUI has been restarted
- Check the ComfyUI console for import errors

**Background not fully removed**
- Make sure the transparent background phrase is in your positive prompt
- Try a different rembg model in the `RembgBackgroundRemover` node (e.g. `isnet-anime` for illustrated characters)

**CUDA out of memory**
- Reduce width/height or frame count
- The two diffusion models are large (14B fp8); 16GB+ VRAM recommended

**Output file is overwritten unexpectedly**
- Change the filename in the Save node before each run

**WEBM won't play in browser/editor**
- Switch codec to VP9 in the Save node for broader compatibility
