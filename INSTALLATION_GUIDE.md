# 🚀 Installation & First Run - Step by Step

## Pre-flight Checklist

Before starting, verify you have:
- [ ] ComfyUI installed at `C:\Kove\AI_gen\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable`
- [ ] NVIDIA GPU with at least 12GB VRAM
- [ ] ~100GB free disk space
- [ ] All files from this project copied to `c:\Kove\AI_gen\transparency workflow`

---

## Phase 1: Custom Node Installation (5 minutes)

### Step 1.1: Prepare Custom Node Folder

Create the custom nodes directory:
```
C:\Kove\AI_gen\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\ComfyUI\custom_nodes\wan_alpha_nodes\
```

### Step 1.2: Copy Node Files

Copy from `c:\Kove\AI_gen\transparency workflow`:
1. `wan_alpha_nodes.py` → paste to custom_nodes/wan_alpha_nodes/
2. `__init__.py` → paste to custom_nodes/wan_alpha_nodes/

**Result**: You should have:
```
ComfyUI\custom_nodes\wan_alpha_nodes\
├── wan_alpha_nodes.py
└── __init__.py
```

### Step 1.3: Verify Installation

Open ComfyUI directory and check:
```bash
cd C:\Kove\AI_gen\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\ComfyUI\custom_nodes\wan_alpha_nodes

# Should list two files:
dir
```

---

## Phase 2: Model Download (30-60 minutes)

### ⭐ IMPORTANT: Use the Official ComfyUI Version

This guide uses the **Official Wan-Alpha ComfyUI Version**, which has files pre-organized for ComfyUI.

**Main Repository**: https://huggingface.co/htdong/Wan-Alpha_ComfyUI

This includes all necessary models, LoRAs, VAE decoders, and a custom save tool - everything organized for ComfyUI!

### Important: HuggingFace Account Required
1. Go to https://huggingface.co
2. Create free account
3. Accept model licenses on HuggingFace pages

### Step 2.1: Download Wan DiT Base Model

**Source**: https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged

1. Go to the Files section
2. Download: `diffusion_models/wan2.1_t2v_14B_fp16.safetensors`
3. Save to:
```
C:\Kove\AI_gen\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\ComfyUI\models\diffusion_models\
```

**File**: ~7-8GB

### Step 2.2: Download Text Encoder

**Source**: https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged

1. Download: `text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors`
2. Save to:
```
C:\Kove\AI_gen\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\ComfyUI\models\text_encoders\
```

**File**: ~3GB

### Step 2.3: Download Wan-Alpha LoRA and VAE Decoders

**Source**: https://huggingface.co/htdong/Wan-Alpha_ComfyUI

Download these files:

1. **RGBA DoRA** - `epoch-13-1500_changed.safetensors`
   Save to: `ComfyUI\models\loras\`
   Size: ~1GB

2. **RGB VAE Decoder** - `wan_alpha_2.1_vae_rgb_channel.safetensors.safetensors`
   Save to: `ComfyUI\models\vae\`
   Size: ~2GB

3. **Alpha VAE Decoder** - `wan_alpha_2.1_vae_alpha_channel.safetensors.safetensors`
   Save to: `ComfyUI\models\vae\`
   Size: ~2GB

### Step 2.4: Download LightX2V (Optional - for faster inference)

**Source**: https://huggingface.co/Kijai/WanVideo_comfy

1. Download: `Lightx2v/lightx2v_T2V_14B_cfg_step_distill_v2_lora_rank64_bf16.safetensors`
2. Save to:
```
C:\Kove\AI_gen\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\ComfyUI\models\loras\
```

**File**: ~2GB

### Step 2.5: Create Model Directories (if needed)

```bash
mkdir "C:\Kove\AI_gen\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\ComfyUI\models\diffusion_models"
mkdir "C:\Kove\AI_gen\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\ComfyUI\models\text_encoders"
mkdir "C:\Kove\AI_gen\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\ComfyUI\models\loras"
mkdir "C:\Kove\AI_gen\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\ComfyUI\models\vae"
```

### Step 2.6: Final Model Structure

After downloading all files, your models folder should look like:

```
ComfyUI\models\
├── diffusion_models\
│   └── wan2.1_t2v_14B_fp16.safetensors
├── text_encoders\
│   └── umt5_xxl_fp8_e4m3fn_scaled.safetensors
├── loras\
│   ├── epoch-13-1500_changed.safetensors
│   └── lightx2v_T2V_14B_cfg_step_distill_v2_lora_rank64_bf16.safetensors (optional)
└── vae\
    ├── wan_alpha_2.1_vae_rgb_channel.safetensors.safetensors
    └── wan_alpha_2.1_vae_alpha_channel.safetensors.safetensors
```

**Note**: If any files are missing or downloads fail, check the [HuggingFace ComfyUI version](https://huggingface.co/htdong/Wan-Alpha_ComfyUI) for alternative download links.

---

## Phase 3: Dependencies Installation (10 minutes)
> Note: Use the portable ComfyUI Python located in `python_embeded`, not the system Python. The system Python may be CPU-only and will report `CUDA Available: False`.
### Step 3.1: Install Required Packages

Open Windows Terminal/PowerShell in the ComfyUI root directory:

```bash
cd C:\Kove\AI_gen\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\ComfyUI

# Use the embedded ComfyUI Python executable
..\python_embeded\python.exe -m pip install --upgrade pip

# Install core packages
..\python_embeded\python.exe -m pip install opencv-python diffusers transformers omegaconf accelerate einops timm

# Verify torch/cuda using embedded Python
..\python_embeded\python.exe -c "import torch; print(f'CUDA Available: {torch.cuda.is_available()}')"
```

**Expected output**: `CUDA Available: True`

### Step 3.2: Verify Installations

```bash
# Test imports
python -c "import cv2; import diffusers; import transformers; print('All packages installed!')"
```

---

## Phase 4: Prepare Test Images (5 minutes)

### Step 4.1: Create Test Images

Create two simple PNG images:

**Image 1: first_frame.png** (e.g., 512x512)
- Simple object (e.g., red ball)
- Clear background
- Centered subject

**Image 2: last_frame.png** (e.g., 512x512)
- Same object in different position
- Same background
- Shows end state of animation

### Step 4.2: Place Images

Copy both images to:
```
C:\Kove\AI_gen\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\ComfyUI\input\
```

**Naming**: Use simple names like:
- `first_frame.png`
- `last_frame.png`

**Format**: PNG with transparency recommended

---

## Phase 5: Start ComfyUI (2 minutes)

### Step 5.1: Launch ComfyUI

Run the appropriate startup script:

**For NVIDIA GPU (Recommended)**:
```bash
cd C:\Kove\AI_gen\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable
run_nvidia_gpu_fast_fp16_accumulation.bat
```

Or run directly:
```bash
cd ComfyUI
python main.py
```

### Step 5.2: Wait for Startup

Console should show:
```
Loading custom nodes...
Loaded 4 nodes from wan_alpha_nodes
Starting server on 127.0.0.1:8188
Use Ctrl+C to stop the server
```

### Step 5.3: Open in Browser

Go to: http://localhost:8188

You should see ComfyUI web interface.

---

## Phase 6: Load Workflow (2 minutes)

### Step 6.1: Load Workflow File

1. Click "Load" button (top menu)
2. Navigate to: `c:\Kove\AI_gen\transparency workflow\wan_alpha_workflow.json`
3. Click "Open"

**Result**: Workflow loads with 5 nodes visible

### Step 6.2: Verify Nodes Loaded

You should see:
1. Load First Frame (Node 1)
2. Load Last Frame (Node 2)
3. Wan-Alpha Video Generator (Node 3)
4. Calculate Frame Rate (Node 4)
5. Save WebM with Alpha (Node 5)

If nodes not visible:
- Try refreshing browser (Ctrl+R)
- Check ComfyUI console for errors
- Verify `__init__.py` exists in custom_nodes folder

---

## Phase 7: Configure & Generate (5 minutes)

### Step 7.1: Configure Input Images

In Node 1 (Load First Frame):
1. Click image dropdown
2. Select: `first_frame.png`

In Node 2 (Load Last Frame):
1. Click image dropdown
2. Select: `last_frame.png`

### Step 7.2: Set Generation Parameters

In Node 3 (Wan-Alpha Video Generator):

**Basic Settings:**
- **frame_count**: 24 (for 1 second @ 24fps)
- **height**: 480
- **width**: 832
- **text_prompt**: "This video has a transparent background. A bouncing ball. Realistic style. Medium shot."
- **steps**: 4 (for fast generation)
- **seed**: 0 (or pick random number)

**Advanced (leave default):**
- guidance_scale: 1.0
- use_fp16: true
- alpha_shift_mean: 0.05

### Step 7.3: Set Output Parameters

In Node 4 (Frame Rate Calculator):
- **frame_rate**: 24

In Node 5 (Save WebM with Alpha):
- **filename**: test_video
- **codec**: VP9
- **quality**: 50

### Step 7.4: Queue Generation

1. Click red **"Queue"** button (bottom right)
2. Watch console for progress
3. Wait for completion

**Timeline:**
- Steps 4 + 24 frames = ~30-40 minutes total

---

## Phase 8: Verify Output (2 minutes)

### Step 8.1: Check Output

Open folder:
```
C:\Kove\AI_gen\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\ComfyUI\output\
```

Should contain:
- `test_video.webm` (file size 50-200MB)

### Step 8.2: Play Video

1. Right-click file
2. Open with → Media Player or Browser
3. Verify:
   - ✅ Video plays
   - ✅ Transparent background (checkerboard pattern)
   - ✅ Duration matches expectations
   - ✅ Quality is acceptable

**Common Issues:**
- Player doesn't support transparency → Try Firefox or Chrome
- File too large → Reduce quality setting
- No transparency → Update prompt to include "transparent"

---

## Troubleshooting First Run

### Issue: Nodes Not Showing

**Solution**:
1. Check browser console (F12) for JavaScript errors
2. Check ComfyUI console for Python import errors
3. Verify both files in `custom_nodes/wan_alpha_nodes/`:
   ```bash
   dir "C:\Kove\AI_gen\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\ComfyUI\custom_nodes\wan_alpha_nodes"
   ```
4. Restart ComfyUI completely

### Issue: CUDA Out of Memory

**Solution**:
1. Reduce frame_count to 12 or 16
2. Reduce resolution to 384x384
3. Enable use_fp16 = true
4. Reduce steps to 2 or 3
5. Close other applications

### Issue: Generation Hangs

**Solution**:
1. Check ComfyUI console for progress messages
2. Monitor GPU usage (NVIDIA Control Panel)
3. First generation is slower (loading models)
4. Subsequent generations faster

### Issue: Video Has No Transparency

**Solutions**:
1. Update prompt to include "transparent background"
2. Verify WebM player supports transparency
3. Try different seed
4. Increase steps to 8
5. Check video in browser (has transparency display)

---

## Next Steps After First Success

1. **Experiment with Different Prompts**
   - See [PROMPT_EXAMPLES.md](PROMPT_EXAMPLES.md)

2. **Try Different Settings**
   - Increase steps for better quality
   - Try higher guidance_scale (1.5-3.0)
   - Experiment with different seeds

3. **Create Production Videos**
   - Prepare better first/last frame images
   - Write detailed prompts
   - Use higher step count for quality

4. **Optimize for Your Needs**
   - See [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for settings templates
   - Adjust resolution based on output use
   - Fine-tune frame rates for smoothness

---

## Quick Command Reference

```bash
# Start ComfyUI
cd C:\Kove\AI_gen\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\ComfyUI
python main.py

# Check CUDA
python -c "import torch; print(torch.cuda.is_available())"

# Install packages
python -m pip install opencv-python diffusers transformers

# List models
dir "C:\Kove\AI_gen\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\ComfyUI\models"

# Check custom nodes
dir "C:\Kove\AI_gen\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\ComfyUI\custom_nodes\wan_alpha_nodes"
```

---

## File Locations Quick Reference

```
ComfyUI Root:
C:\Kove\AI_gen\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\ComfyUI\

Custom Nodes:
ComfyUI\custom_nodes\wan_alpha_nodes\

Models:
ComfyUI\models\loras\
ComfyUI\models\vae\
ComfyUI\models\diffusion_models\

Input Images:
ComfyUI\input\

Output Videos:
ComfyUI\output\

Workflow Files:
c:\Kove\AI_gen\transparency workflow\
```

---

## Getting Help

| Issue | Reference |
|-------|-----------|
| Setup Problems | [SETUP_GUIDE.md](SETUP_GUIDE.md) |
| Node Installation | [CUSTOM_NODES_INSTALL.md](CUSTOM_NODES_INSTALL.md) |
| Prompt Help | [PROMPT_EXAMPLES.md](PROMPT_EXAMPLES.md) |
| Quick Lookup | [QUICK_REFERENCE.md](QUICK_REFERENCE.md) |
| Technical Details | [TECHNICAL_DOCUMENTATION.md](TECHNICAL_DOCUMENTATION.md) |
| General Info | [README.md](README.md) |

---

## Estimated Timeline

| Phase | Time | Status |
|-------|------|--------|
| 1. Custom Nodes | 5 min | ⚡ Quick |
| 2. Models Download | 30-60 min | ⏳ Depends on connection |
| 3. Dependencies | 10 min | ⚡ Quick |
| 4. Test Images | 5 min | ⚡ Quick |
| 5. Start ComfyUI | 2 min | ⚡ Quick |
| 6. Load Workflow | 2 min | ⚡ Quick |
| 7. Configure | 5 min | ⚡ Quick |
| 8. First Generation | 30-40 min | ⏳ First run slower |
| 9. Verify Output | 2 min | ⚡ Quick |
| **TOTAL** | **90-120 min** | ⏳ Mostly downloads |

---

**You're ready to create amazing transparent videos!** 🎬✨

Start with Phase 1 and progress through each phase. Each phase must be complete before moving to the next.

Good luck! 🚀
