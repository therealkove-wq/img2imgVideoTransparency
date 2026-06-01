# Wan-Alpha ComfyUI Workflow - Setup Guide

## Overview
This workflow generates videos with transparency (alpha channel) using Wan-Alpha, a state-of-the-art model for text-to-video with stable transparency support. It's designed for CVPR 2026.

**Key Features:**
- Text-to-video generation with alpha channel
- Image-to-video interpolation
- RGBA output (WebM format with transparency)
- Customizable frame count and frame rate
- Text-conditioned video generation

---

## Prerequisites

### Hardware Requirements
- **GPU:** NVIDIA GPU with at least 16GB VRAM (recommended: 24GB+ for best quality)
- **Disk Space:** ~100GB for models and outputs
- **RAM:** 32GB system RAM recommended

### Software Requirements
- ComfyUI (already installed at `C:\Kove\AI_gen\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable`)
- Python 3.11+ (included with ComfyUI)
- CUDA 11.8+ (included with ComfyUI)

---

## Installation Steps

### Step 1: Install Required Models

Download the following models from the **Official Wan-Alpha ComfyUI Version** and place them in the ComfyUI models directories:

**Main Source**: https://huggingface.co/htdong/Wan-Alpha_ComfyUI

#### 1a. Wan DiT Base Model (Wan2.1-T2V-14B)
```
Location: ComfyUI\models\diffusion_models\

Source: https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged
File: wan2.1_t2v_14B_fp16.safetensors (from diffusion_models/ folder)
Size: ~7-8GB
```

#### 1b. Text Encoder (UMT5-XXL)
```
Location: ComfyUI\models\text_encoders\

Source: https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged
File: umt5_xxl_fp8_e4m3fn_scaled.safetensors (from text_encoders/ folder)
Size: ~3GB
```

#### 1c. Wan-Alpha LoRA and VAE Weights
```
Location: ComfyUI\models\loras\ and ComfyUI\models\vae\

Source: https://huggingface.co/htdong/Wan-Alpha_ComfyUI
Files: 
- epoch-13-1500_changed.safetensors (→ models\loras\)
- wan_alpha_2.1_vae_rgb_channel.safetensors.safetensors (→ models\vae\)
- wan_alpha_2.1_vae_alpha_channel.safetensors.safetensors (→ models\vae\)
Total Size: ~5GB
```

#### 1d. LightX2V (Optional - for faster inference)
```
Location: ComfyUI\models\loras\

Source: https://huggingface.co/Kijai/WanVideo_comfy
File: lightx2v_T2V_14B_cfg_step_distill_v2_lora_rank64_bf16.safetensors
Size: ~2GB
```

### Step 2: Install Custom Node Dependencies

The custom nodes require additional Python packages. Run in the ComfyUI directory:

```bash
cd C:\Kove\AI_gen\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable
python -m pip install -r requirements.txt
python -m pip install diffusers transformers omegaconf accelerate einops timm pillow numpy opencv-python
```

### Step 3: Install Custom Nodes

Copy the `wan_alpha_nodes` folder to:
```
C:\Kove\AI_gen\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\ComfyUI\custom_nodes\wan_alpha_nodes
```

### Step 4: Create Required Directories

```
C:\Kove\AI_gen\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\ComfyUI\input\
C:\Kove\AI_gen\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\ComfyUI\output\
C:\Kove\AI_gen\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\ComfyUI\models\diffusion_models\
C:\Kove\AI_gen\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\ComfyUI\models\loras\
C:\Kove\AI_gen\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\ComfyUI\models\vae\
```

---

## Usage Guide

### Step 1: Prepare Input Images
1. Create two images:
   - **First Frame:** Starting image for interpolation
   - **Last Frame:** Ending image for interpolation
2. Place them in the `input` folder
3. Supported formats: PNG, JPG (PNG recommended for transparency)

### Step 2: Load Workflow
1. Open ComfyUI in your browser (typically `http://localhost:8188`)
2. Load the workflow file: `wan_alpha_workflow.json`

### Step 3: Configure Parameters
In the workflow, set:
- **First Frame Image:** Select your starting image
- **Last Frame Image:** Select your ending image
- **Movie Length:** Number of frames to generate (e.g., 120 for 5 seconds at 24fps)
- **Frame Rate:** Frames per second (e.g., 24, 30, 60)
- **Text Prompt:** Describe the video content with transparency:
  - Example: "The background of this video is transparent. A red ball bouncing. Realistic style. Medium shot."
  - **Important:** Always specify "transparent background" in your prompt for best results

### Step 4: Generate Video
1. Click "Queue" to start generation
2. Monitor progress in the console
3. Output will be saved in the `output` folder as WebM with alpha channel

---

## Prompt Writing Tips

For best results with transparent backgrounds:

```
"This video has a transparent background. [shot type]. [main subject]. [action/style]. [visual description]."
```

Examples:
- "This video has a transparent background. Close-up shot. A colorful parrot flying. Realistic style."
- "The background is transparent. Wide shot. A crystal spinning in light. Cinematic quality."
- "Transparent background. Medium shot. A pen writing on white paper. Realistic."

**Key elements:**
- Always mention transparency/transparent background
- Specify shot type (close-up, wide, medium)
- Describe main subject and action
- Include style preference (realistic, artistic, cinematic, etc.)

---

## Troubleshooting

### Out of Memory (OOM) Errors
- Reduce movie length or frame count
- Reduce resolution (modify in workflow)
- Enable memory-efficient attention

### Slow Generation
- Use LightX2V for faster inference
- Reduce number of frames
- Enable half-precision (fp16) mode

### Poor Transparency Quality
- Update prompt to emphasize transparency
- Use Wan-Alpha v2.0 (better transparency)
- Ensure input images have clear silhouettes

### Model Download Issues
- Use HuggingFace CLI: `huggingface-cli download model-name`
- Check internet connection
- Verify disk space (100GB+ free space recommended)

---

## Model Architecture

```
Input Images → Wan-Alpha Video Generator → RGBA Video → SaveWebm Node → WebM Output
   (first)
   (last)
   
Text Prompt → T5 Encoder → Video Generation Process
Frame Rate  → Frame Scheduler
Frame Count → Duration Calculator
```

---

## Output Format

The workflow outputs WebM files with:
- **Format:** VP9 codec (supports alpha)
- **Color Space:** RGBA (with transparency)
- **Customizable:** Frame rate and duration

Files are saved in: `C:\Kove\AI_gen\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\ComfyUI\output\`

---

## Next Steps

1. Complete the model downloads (Step 1)
2. Install dependencies (Step 2)
3. Copy custom nodes (Step 3)
4. Load the workflow and configure inputs
5. Generate your first transparent video!

---

## References

- [Wan-Alpha Paper](https://arxiv.org/pdf/2509.24979)
- [Project Page](https://donghaotian123.github.io/Wan-Alpha/)
- [HuggingFace Models](https://huggingface.co/htdong/Wan-Alpha)
- [GitHub Repository](https://github.com/WeChatCV/Wan-Alpha)

---

## Support

For issues or questions:
- Check the Wan-Alpha GitHub Issues
- Review ComfyUI documentation
- Check model compatibility and versions
