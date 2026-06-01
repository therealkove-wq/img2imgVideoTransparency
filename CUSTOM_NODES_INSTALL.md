# Wan-Alpha ComfyUI Custom Nodes Installation

## Quick Setup

### Option 1: Automatic Installation (Recommended)

1. Copy the entire `wan_alpha_nodes` folder to ComfyUI custom_nodes:
```bash
copy /Y "c:\Kove\AI_gen\transparency workflow\wan_alpha_nodes" "C:\Kove\AI_gen\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\ComfyUI\custom_nodes\"
```

2. Restart ComfyUI

3. Check the UI - you should see new nodes under "video/wan_alpha" category

### Option 2: Manual Installation

1. Create folder structure:
```
C:\Kove\AI_gen\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\ComfyUI\custom_nodes\wan_alpha_nodes\
```

2. Copy these files into that folder:
   - `wan_alpha_nodes.py` (the main nodes file)
   - `__init__.py` (package init file)

3. Create `__init__.py` with content:
```python
from .wan_alpha_nodes import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
```

4. Restart ComfyUI

## Installation Verification

After installation, verify the nodes are loaded:

1. Open ComfyUI in your browser (http://localhost:8188)
2. Click "Add Node" (Shift+A or drag to add)
3. Look for "video/wan_alpha" category
4. You should see:
   - Wan-Alpha Video Generator
   - Frame Rate Calculator
   - Image Loader (Video)
   - Save WebM with Alpha

If nodes don't appear:
- Check ComfyUI console for errors
- Verify file paths are correct
- Make sure `__init__.py` is present
- Check Python syntax in wan_alpha_nodes.py

## File Structure

```
c:\Kove\AI_gen\transparency workflow\
├── SETUP_GUIDE.md                  # Main setup instructions
├── CUSTOM_NODES_INSTALL.md         # This file
├── wan_alpha_nodes.py              # Core node implementations
├── __init__.py                     # Package initialization
├── wan_alpha_workflow.json         # Example workflow
├── prompt_examples.txt             # Prompt templates
├── advanced_config.yaml            # Advanced settings (optional)
└── README.md                       # Overview

ComfyUI\custom_nodes\wan_alpha_nodes\
├── __init__.py                     # Copy from root
└── wan_alpha_nodes.py              # Copy from root
```

## Dependencies

The custom nodes depend on:

```
torch                    # PyTorch (included with ComfyUI)
torchvision            # Vision utilities
numpy                  # Numerical arrays
Pillow                 # Image processing
opencv-python          # WebM saving
diffusers              # Diffusion models
transformers           # Transformer models (T5, CLIP)
omegaconf              # Configuration
accelerate             # Distributed computing
einops                 # Tensor operations
timm                   # Vision models
```

Most are already included with ComfyUI. To install missing ones:

```bash
cd C:\Kove\AI_gen\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable
python -m pip install opencv-python diffusers transformers omegaconf accelerate einops timm
```

## Updating Nodes

To update the nodes:

1. Replace `wan_alpha_nodes.py` in the custom_nodes folder
2. Restart ComfyUI
3. Clear browser cache if issues persist

## Troubleshooting

### Nodes Not Appearing

**Check 1:** Verify Python syntax
```bash
python -m py_compile "C:\Kove\AI_gen\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\ComfyUI\custom_nodes\wan_alpha_nodes\wan_alpha_nodes.py"
```

**Check 2:** Look at ComfyUI console for import errors

**Check 3:** Verify `__init__.py` exists and has correct content

**Check 4:** Check file permissions (should be readable)

### Import Errors

If you see "ImportError: No module named 'folder_paths'":
- This is expected - it means the nodes are being loaded outside of ComfyUI
- The error disappears when nodes are used in ComfyUI

### Memory Issues During Loading

If ComfyUI crashes when loading nodes:
1. Check that `use_fp16=true` in workflow (uses less memory)
2. Reduce image resolution in the Wan-Alpha Video Generator node
3. Increase system page file / virtual memory

## Next Steps

1. ✅ Install custom nodes (this file)
2. 📥 Download models (see SETUP_GUIDE.md)
3. 🔧 Load the workflow (wan_alpha_workflow.json)
4. ✨ Generate your first transparent video!

## Support

For detailed setup instructions, see **SETUP_GUIDE.md**

For workflow usage, see **README.md**

For prompt examples, see **prompt_examples.txt**
