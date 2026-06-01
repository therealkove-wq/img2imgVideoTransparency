# ✅ Model Download - Corrected Links

## 🔧 What Was Fixed

The original installation guide pointed to model files that weren't easily accessible. I've updated it to use the **Official Wan-Alpha ComfyUI Version** which has all files pre-organized and ready to use.

---

## 📥 Download These Files

### Location: Official Wan-Alpha ComfyUI Repository
**Main URL**: https://huggingface.co/htdong/Wan-Alpha_ComfyUI

### Required Downloads

| File | Size | Where to Save |
|------|------|---------------|
| [wan2.1_t2v_14B_fp16.safetensors](https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged) | 7-8GB | `ComfyUI\models\diffusion_models\` |
| [umt5_xxl_fp8_e4m3fn_scaled.safetensors](https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged) | 3GB | `ComfyUI\models\text_encoders\` |
| [epoch-13-1500_changed.safetensors](https://huggingface.co/htdong/Wan-Alpha_ComfyUI) | 1GB | `ComfyUI\models\loras\` |
| [wan_alpha_2.1_vae_rgb_channel.safetensors.safetensors](https://huggingface.co/htdong/Wan-Alpha_ComfyUI) | 2GB | `ComfyUI\models\vae\` |
| [wan_alpha_2.1_vae_alpha_channel.safetensors.safetensors](https://huggingface.co/htdong/Wan-Alpha_ComfyUI) | 2GB | `ComfyUI\models\vae\` |

**Optional:**
| [lightx2v_T2V_14B_cfg_step_distill_v2_lora_rank64_bf16.safetensors](https://huggingface.co/Kijai/WanVideo_comfy) | 2GB | `ComfyUI\models\loras\` |

**Total Required**: ~15GB (22GB with optional LightX2V)

---

## 📍 Exact Folder Structure After Download

```
ComfyUI/models/
├── diffusion_models/
│   └── wan2.1_t2v_14B_fp16.safetensors                    ✅ 7-8GB
├── text_encoders/
│   └── umt5_xxl_fp8_e4m3fn_scaled.safetensors             ✅ 3GB
├── loras/
│   ├── epoch-13-1500_changed.safetensors                  ✅ 1GB
│   └── lightx2v_T2V_14B_cfg_step_distill_v2_lora_rank64_bf16.safetensors  (optional, 2GB)
└── vae/
    ├── wan_alpha_2.1_vae_rgb_channel.safetensors.safetensors           ✅ 2GB
    └── wan_alpha_2.1_vae_alpha_channel.safetensors.safetensors         ✅ 2GB
```

---

## 🚀 How to Download

### Option 1: Manual Download (Easiest)

1. Go to: https://huggingface.co/htdong/Wan-Alpha_ComfyUI
2. Click "Files and versions"
3. Download each `.safetensors` file
4. Save to appropriate folder (see table above)

For the base model and text encoder:
1. Go to: https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged
2. Navigate to `split_files/diffusion_models/` for the base model
3. Navigate to `split_files/text_encoders/` for the text encoder
4. Download and save

### Option 2: HuggingFace CLI (For Large Files)

```bash
# Install CLI (if not already installed)
pip install huggingface-hub

# Download individual files
huggingface-cli download htdong/Wan-Alpha_ComfyUI epoch-13-1500_changed.safetensors --local-dir "C:\path\to\ComfyUI\models\loras"

huggingface-cli download htdong/Wan-Alpha_ComfyUI wan_alpha_2.1_vae_rgb_channel.safetensors.safetensors --local-dir "C:\path\to\ComfyUI\models\vae"

huggingface-cli download htdong/Wan-Alpha_ComfyUI wan_alpha_2.1_vae_alpha_channel.safetensors.safetensors --local-dir "C:\path\to\ComfyUI\models\vae"
```

---

## ✅ Verification Checklist

After downloading, verify:

- [ ] `diffusion_models/wan2.1_t2v_14B_fp16.safetensors` exists (7-8GB)
- [ ] `text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors` exists (3GB)
- [ ] `loras/epoch-13-1500_changed.safetensors` exists (1GB)
- [ ] `vae/wan_alpha_2.1_vae_rgb_channel.safetensors.safetensors` exists (2GB)
- [ ] `vae/wan_alpha_2.1_vae_alpha_channel.safetensors.safetensors` exists (2GB)

Run in Windows Explorer or PowerShell:
```powershell
# Check if all files exist
dir "C:\Kove\AI_gen\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\ComfyUI\models\diffusion_models\"
dir "C:\Kove\AI_gen\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\ComfyUI\models\text_encoders\"
dir "C:\Kove\AI_gen\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\ComfyUI\models\loras\"
dir "C:\Kove\AI_gen\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\ComfyUI\models\vae\"
```

---

## 🎯 Next Steps

1. ✅ Download all required files (use links above)
2. ✅ Verify folder structure
3. ✅ Continue with Phase 3 of INSTALLATION_GUIDE.md (Dependencies Installation)

---

## 📝 Updates Made

- ✅ INSTALLATION_GUIDE.md - Updated to use official ComfyUI version
- ✅ SETUP_GUIDE.md - Updated with correct download links
- ✅ Created this guide for reference

---

## ❓ Troubleshooting

**Q: I can't find a specific file on HuggingFace**
- A: Try searching for it on: https://huggingface.co/htdong/Wan-Alpha_ComfyUI
- Or check: https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged

**Q: The file is too large to download**
- A: Use the HuggingFace CLI option above, or try a different browser/manager
- Connection may have timed out - retry or use a download manager

**Q: Files won't download from HuggingFace**
- A: You may need to accept the model license first
- Go to the HuggingFace model page and click "Accept" license

**Q: I'm still having trouble**
- A: Check the updated [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md) Phase 2

---

**Good luck with your downloads!** 🚀
