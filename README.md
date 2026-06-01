# Wan-Alpha ComfyUI Workflow - Complete Guide

## 🎬 Overview

This project enables you to generate **videos with transparent backgrounds (alpha channel)** using **Wan-Alpha**, a state-of-the-art model for text-to-video generation with stable transparency.

Perfect for:
- Creating transparent video overlays
- Generating animated objects with transparency
- Making video elements for compositing
- Creating looping animations
- Producing transparent background videos for web/streaming

---

## 📋 Quick Start (5 Minutes)

### 1. **Install Custom Nodes**
```bash
# Copy the custom nodes to ComfyUI
copy "c:\Kove\AI_gen\transparency workflow\wan_alpha_nodes.py" "C:\Kove\AI_gen\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\ComfyUI\custom_nodes\wan_alpha_nodes\"
copy "c:\Kove\AI_gen\transparency workflow\__init__.py" "C:\Kove\AI_gen\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\ComfyUI\custom_nodes\wan_alpha_nodes\"
```

### 2. **Download Models**
See [SETUP_GUIDE.md](SETUP_GUIDE.md#step-1-install-required-models) for detailed model download instructions.

### 3. **Load Workflow**
1. Open ComfyUI in your browser (http://localhost:8188)
2. Load: `wan_alpha_workflow.json`
3. Configure inputs (see below)

### 4. **Generate Video**
1. Prepare first and last frame images
2. Set parameters (frame count, FPS, text prompt)
3. Click "Queue" and wait

---

## 🎯 Workflow Parameters

The workflow accepts these inputs:

### **Image Inputs**
- **First Frame**: Starting image (PNG recommended)
- **Last Frame**: Ending image (PNG recommended)

### **Video Parameters**
- **Frame Count**: Number of frames (8-256, step by 8)
  - 24 frames @ 24 FPS = 1 second
  - 120 frames @ 24 FPS = 5 seconds
  - 240 frames @ 30 FPS = 8 seconds

- **Frame Rate**: Frames per second (1-120)
  - 24 FPS: cinematic/film
  - 30 FPS: standard video
  - 60 FPS: smooth motion

- **Height/Width**: Resolution (256-1024)
  - Default: 480x832 (good balance)
  - Options: 256, 320, 384, 448, 512, 576, 640, 704, 768, 832, 896, 960, 1024

### **Text Prompt**
Describe what happens in the video (see [PROMPT_EXAMPLES.md](PROMPT_EXAMPLES.md))

Example:
```
This video has a transparent background. Medium shot. A red ball bouncing. 
Realistic style. Smooth animation.
```

### **Generation Parameters**
- **Steps**: Inference quality (1-50, default 4)
  - 4 steps: fast, decent quality
  - 8 steps: balanced
  - 16+ steps: high quality (slower)

- **Guidance Scale**: Prompt strength (0.0-10.0, default 1.0)
  - Lower (0.5-1.0): more creative freedom
  - Higher (2.0-5.0): follows prompt more strictly

- **Seed**: Random seed for reproducibility
  - Same seed + settings = same output
  - Different seed = different variation

- **Use FP16**: Memory-efficient mode (faster, uses less VRAM)

---

## 📁 Project Structure

```
c:\Kove\AI_gen\transparency workflow\
│
├── README.md                        ← You are here
├── SETUP_GUIDE.md                   ← Complete setup instructions
├── CUSTOM_NODES_INSTALL.md          ← Custom nodes installation
├── PROMPT_EXAMPLES.md               ← Example prompts
│
├── wan_alpha_workflow.json          ← Main workflow (load in ComfyUI)
├── wan_alpha_nodes.py               ← Core node implementations
├── __init__.py                      ← Package initialization
│
└── ComfyUI Custom Nodes Install Path:
    C:\Kove\AI_gen\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\ComfyUI\custom_nodes\wan_alpha_nodes\
    ├── wan_alpha_nodes.py
    └── __init__.py
```

---

## 🔧 Setup Checklist

- [ ] **Read SETUP_GUIDE.md** - Detailed environment setup
- [ ] **Install custom nodes** - Copy files to ComfyUI
- [ ] **Download models** - Get Wan-Alpha weights (100GB+)
- [ ] **Prepare input images** - Create first/last frame images
- [ ] **Load workflow** - Open wan_alpha_workflow.json
- [ ] **Configure parameters** - Set frame count, FPS, prompt
- [ ] **Generate video** - Queue and run
- [ ] **Review output** - Check output folder

---

## 🎨 Custom Nodes Overview

### **Wan-Alpha Video Generator**
Main node for generating transparent videos
- Inputs: First frame, last frame, text prompt, parameters
- Outputs: Video frames with alpha channel

### **Image Loader (Video)**
Loads images from the input folder
- Inputs: Image filename
- Outputs: IMAGE tensor

### **Frame Rate Calculator**
Calculates video duration and timing
- Inputs: Frame count, frame rate
- Outputs: Duration info

### **Save WebM with Alpha**
Exports video with transparency support
- Inputs: Video frames, filename, codec, quality
- Outputs: WebM file path

---

## 📝 Example Prompts

### Simple Objects
```
This video has a transparent background. Medium shot. A spinning golden cube. 
Realistic lighting. Cinematic quality.
```

### Living Subjects
```
Transparent background. Close-up. A blue butterfly flying gracefully. 
Detailed wings. Natural sunlight. Realistic style.
```

### Special Effects
```
The background is transparent. Wide shot. Colorful particles swirling and forming 
a sphere shape. Neon colors. Glowing effect. Futuristic style.
```

See [PROMPT_EXAMPLES.md](PROMPT_EXAMPLES.md) for more examples.

---

## ⚙️ Advanced Configuration

### Performance Tuning
- **Low VRAM** (12GB): Reduce resolution, lower steps, enable FP16
- **Medium VRAM** (16GB): Default settings work well
- **High VRAM** (24GB+): Increase resolution, more steps, higher quality

### Quality Settings
- **Draft Quality**: steps=4, guidance=0.8, FP16=true (fast)
- **Standard Quality**: steps=4, guidance=1.0, FP16=true (balanced)
- **High Quality**: steps=8, guidance=2.0, FP16=false (slow)

### Output Options
- **VP9 Codec**: Better compression, slower encoding
- **VP8 Codec**: Faster encoding, larger file size
- **Quality**: 0-100 (higher = better quality, larger file)

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'custom_nodes'"
- Make sure you're in the ComfyUI directory
- Check that `__init__.py` exists in custom_nodes folder

### CUDA Out of Memory
- Reduce frame count
- Reduce resolution (640x480 instead of 832x480)
- Enable FP16 mode
- Use fewer steps

### Nodes Not Showing in UI
- Restart ComfyUI completely
- Check Python syntax: `python -m py_compile wan_alpha_nodes.py`
- Check console for import errors

### Poor Transparency Quality
- Update text prompt to explicitly mention transparency
- Use Wan-Alpha v2.0 (better transparency than v1.0)
- Increase step count (8-16 steps)
- Try different seeds

### WebM File Won't Play
- Use VP9 codec for better compatibility
- Try reducing quality setting
- Check that frame count matches duration
- Verify output file size (should be multiple MB)

---

## 📊 Performance Expectations

| Setting | VRAM Used | Time/Frame | FPS |
|---------|-----------|-----------|-----|
| 480p, steps=4, FP16 | ~14GB | 45-60s | 0.017 |
| 480p, steps=8 | ~16GB | 90-120s | 0.008 |
| 640p, steps=4 | ~18GB | 60-90s | 0.011 |
| 640p, steps=8 | ~20GB | 120-180s | 0.006 |

*Approximate values; varies by GPU and system*

---

## 🚀 Getting Started

### Minimum Quick Start
1. Copy custom nodes folder
2. Download Wan-Alpha weights only (skip other models for now)
3. Place 2 test images in `input/` folder
4. Load `wan_alpha_workflow.json`
5. Modify text prompt and click Generate

### Full Professional Setup
1. Complete SETUP_GUIDE.md entirely
2. Download all models (Wan2.1, VAE, LightX2V)
3. Set up input/output folder structure
4. Test with sample images
5. Create your own prompts
6. Generate production videos

---

## 🎓 Learning Resources

### Official Wan-Alpha Resources
- **Paper**: [arXiv:2509.24979](https://arxiv.org/pdf/2509.24979)
- **Project**: https://donghaotian123.github.io/Wan-Alpha/
- **HuggingFace**: https://huggingface.co/htdong/Wan-Alpha
- **GitHub**: https://github.com/WeChatCV/Wan-Alpha

### ComfyUI Resources
- **ComfyUI GitHub**: https://github.com/comfyui/comfyui
- **Custom Nodes**: https://github.com/comfyui/comfyui/wiki/Custom-Node-Tutorial
- **Community Workflows**: https://civitai.com/tag/comfyui

---

## 🎬 Workflow Tips

### Best Practices
1. **Start with simple prompts** - Single object/action works best
2. **Use high-contrast images** - Better subject extraction
3. **Keep frame count reasonable** - 24-120 frames optimal
4. **Test different seeds** - Find best variation
5. **Monitor VRAM usage** - Adjust parameters if needed

### Common Issues & Solutions
| Issue | Solution |
|-------|----------|
| Background not transparent | Add "transparent background" to prompt |
| Jerky animation | Increase frame count, reduce step size |
| Low quality output | Increase steps to 8-16 |
| Slow generation | Enable FP16, reduce resolution |
| Artifacts in video | Try different seed, adjust guidance |

---

## 📞 Support & Feedback

### Getting Help
1. Check [SETUP_GUIDE.md](SETUP_GUIDE.md) troubleshooting section
2. Review error messages in ComfyUI console
3. Check [PROMPT_EXAMPLES.md](PROMPT_EXAMPLES.md) for prompt tips
4. Verify model downloads are complete

### Reporting Issues
- Wan-Alpha issues: GitHub https://github.com/WeChatCV/Wan-Alpha/issues
- ComfyUI issues: GitHub https://github.com/comfyui/comfyui/issues
- Custom node issues: Include error message, workflow JSON, and settings

---

## 📄 License

- **Wan-Alpha**: Research paper & weights (see original repository)
- **Custom Nodes**: Available for use and modification
- **ComfyUI**: Open source (see ComfyUI repository)

---

## 🎯 Next Steps

1. **Start Here** → [SETUP_GUIDE.md](SETUP_GUIDE.md)
2. **Install Nodes** → [CUSTOM_NODES_INSTALL.md](CUSTOM_NODES_INSTALL.md)
3. **Learn Prompts** → [PROMPT_EXAMPLES.md](PROMPT_EXAMPLES.md)
4. **Load Workflow** → `wan_alpha_workflow.json`
5. **Generate Video** → Click Queue!

---

Happy video generation! 🎬✨
