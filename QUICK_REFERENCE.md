# Quick Reference Guide

## 🚀 30-Second Quick Start

1. **Install nodes**: Copy `wan_alpha_nodes` folder to ComfyUI custom_nodes
2. **Download models**: Get Wan-Alpha weights from HuggingFace
3. **Load workflow**: Open `wan_alpha_workflow.json` in ComfyUI
4. **Set images**: Select first_frame.png and last_frame.png
5. **Write prompt**: "This video has a transparent background. [description]"
6. **Generate**: Click Queue button

---

## ⌨️ Common Commands

### ComfyUI Navigation
| Action | How |
|--------|-----|
| Add Node | Shift+A or drag from sidebar |
| Delete Node | Right-click → Delete |
| Connect Nodes | Drag output → input |
| Save Workflow | Ctrl+S (auto-saves) |
| Load Workflow | Click Load button |
| Queue Generation | Click Queue button |
| View Output | Check output/ folder |

---

## 📸 Input Image Specs

| Parameter | Recommended | Min | Max |
|-----------|-------------|-----|-----|
| Format | PNG | JPG, PNG, BMP | Any common format |
| Dimensions | 512x512 | 256x256 | 1024x1024 |
| Color Space | RGBA | RGB, RGBA | - |
| File Size | < 5MB | - | - |
| Subject | Clear silhouette | - | - |

---

## 🎯 Workflow Parameters Quick Reference

| Parameter | Default | Range | Notes |
|-----------|---------|-------|-------|
| Frame Count | 24 | 8-256 | Step by 8 |
| Frame Rate | 24 | 1-120 | FPS (24=cinematic) |
| Height | 480 | 256-1024 | Step by 64 |
| Width | 832 | 256-1024 | Step by 64 |
| Steps | 4 | 1-50 | Higher = better quality |
| Guidance | 1.0 | 0.0-10.0 | Prompt adherence |
| Seed | 0 | 0-2^64 | Reproducibility |

---

## 📊 Duration Calculation

```
Duration = Frame Count / Frame Rate

Examples:
24 frames @ 24 FPS = 1 second
120 frames @ 24 FPS = 5 seconds
240 frames @ 30 FPS = 8 seconds
360 frames @ 60 FPS = 6 seconds
```

---

## 🎨 Prompt Formula

```
[TRANSPARENCY] [SHOT TYPE] [SUBJECT] [ACTION] [STYLE] [DETAILS]

Example:
"This video has a transparent background. Medium shot. A golden sphere rotating. 
Realistic style. Cinematic lighting."
```

### Transparency Options (Pick One)
- This video has a transparent background
- The background is transparent
- Transparent background
- Background should be transparent

### Shot Types
- **Close-up**: Extreme detail, fills frame
- **Medium shot**: Balanced view, shows upper portion
- **Wide shot**: Full scene, zoomed out
- **Full body**: For characters, head to toe
- **Pan**: Camera movement across scene

### Style Examples
- Realistic / Photorealistic
- Cinematic / Movie-like
- Artistic / Painted
- Cartoon / Animated
- 3D Rendered
- Minimal / Sketch
- Fantasy / Magical
- Futuristic / Sci-fi

---

## 🔧 Settings for Different Use Cases

### Social Media (Quick & Small)
```
Frame Rate: 30 FPS
Frame Count: 120 (4 seconds)
Resolution: 480x480
Steps: 4
Guidance: 1.0
FP16: Yes
Codec: VP8
```

### Streaming (Smooth Motion)
```
Frame Rate: 60 FPS
Frame Count: 240 (4 seconds)
Resolution: 640x480
Steps: 8
Guidance: 2.0
FP16: No
Codec: VP9
```

### Professional (High Quality)
```
Frame Rate: 24 FPS
Frame Count: 240 (10 seconds)
Resolution: 832x480
Steps: 16
Guidance: 2.5
FP16: No
Codec: VP9
Quality: 80
```

### Low GPU (Budget Mode)
```
Frame Rate: 24 FPS
Frame Count: 48 (2 seconds)
Resolution: 384x384
Steps: 4
Guidance: 0.8
FP16: Yes
Codec: VP8
Quality: 40
```

---

## 🆘 Quick Troubleshooting

| Problem | Quick Fix |
|---------|-----------|
| Background not transparent | Add "transparent" to prompt |
| Out of memory | Lower resolution, reduce frames, enable FP16 |
| Slow generation | Enable FP16, reduce steps, smaller resolution |
| Nodes not showing | Restart ComfyUI, check __init__.py exists |
| Poor quality | Increase steps to 8-16, improve prompt |
| Video won't play | Use VP9 codec, check frame rate |

---

## 📁 File Locations

```
Main Workflow:
C:\Kove\AI_gen\transparency workflow\wan_alpha_workflow.json

Custom Nodes:
C:\Kove\AI_gen\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\ComfyUI\custom_nodes\wan_alpha_nodes\

Input Images:
C:\Kove\AI_gen\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\ComfyUI\input\

Output Videos:
C:\Kove\AI_gen\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\ComfyUI\output\

Models:
C:\Kove\AI_gen\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\ComfyUI\models\
```

---

## 🎬 Generation Workflow

```
1. Prepare Images
   ↓
2. Open ComfyUI (localhost:8188)
   ↓
3. Load wan_alpha_workflow.json
   ↓
4. Configure All Parameters
   ├─ Select first frame image
   ├─ Select last frame image
   ├─ Set frame count & rate
   ├─ Write text prompt
   ├─ Adjust steps & guidance
   └─ Set seed
   ↓
5. Queue Generation
   ↓
6. Wait for Completion
   ├─ Monitor console for progress
   └─ Check memory usage
   ↓
7. Review Output
   ├─ Check output/ folder
   ├─ Play WebM file
   └─ Verify transparency
   ↓
8. Export or Iterate
   ├─ Use video as-is
   ├─ Adjust prompt & regenerate
   └─ Or export for further editing
```

---

## 💡 Pro Tips

1. **Test with short videos first** (24-48 frames) before generating long ones
2. **Save different seeds** - Same prompt with different seeds yields variety
3. **Use clear images** - High contrast first/last frames work better
4. **Be specific in prompts** - More detail = better results
5. **Monitor VRAM** - Stop if using >95% to avoid crashes
6. **Back up output** - Copy generated videos before new runs
7. **Experiment with steps** - 4 is fast, 8-16 is higher quality
8. **Use descriptive filenames** - Track what settings produced best results

---

## 📞 Getting Help

| Issue Type | Where to Look |
|-----------|---------------|
| Setup/Installation | SETUP_GUIDE.md |
| Using nodes | CUSTOM_NODES_INSTALL.md |
| Prompt tips | PROMPT_EXAMPLES.md |
| Workflow usage | README.md |
| Wan-Alpha model | https://github.com/WeChatCV/Wan-Alpha |
| ComfyUI issues | https://github.com/comfyui/comfyui |

---

## ✅ Checklist Before Generating

- [ ] Custom nodes installed and showing in UI
- [ ] All models downloaded (check file sizes)
- [ ] Input images placed in input/ folder
- [ ] Workflow JSON loaded and visible
- [ ] First frame image selected
- [ ] Last frame image selected
- [ ] Frame count set (8-256)
- [ ] Frame rate set (1-120)
- [ ] Text prompt includes "transparent"
- [ ] Steps set appropriately
- [ ] Seed value chosen (or use 0 for random)
- [ ] GPU has enough VRAM
- [ ] Output folder exists and is writable

---

**Ready to generate? Click "Queue" and create amazing transparent videos!** 🎬✨
