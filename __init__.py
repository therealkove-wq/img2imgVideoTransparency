"""
Wan-Alpha Custom Nodes Package for ComfyUI
This package provides nodes for generating videos with transparency using Wan-Alpha.
"""

try:
    from .wan_alpha_nodes import (
        WanAlphaVideoGenerator,
        FrameRateCalculator,
        ImageLoaderForVideo,
        SaveWebmWithAlpha,
        NODE_CLASS_MAPPINGS,
        NODE_DISPLAY_NAME_MAPPINGS,
    )
except ImportError:
    pass  # standalone import (e.g. pytest); ComfyUI always imports as a package

__all__ = [
    "WanAlphaVideoGenerator",
    "FrameRateCalculator", 
    "ImageLoaderForVideo",
    "SaveWebmWithAlpha",
    "NODE_CLASS_MAPPINGS",
    "NODE_DISPLAY_NAME_MAPPINGS",
]

# ComfyUI expects these exports
try:
    __nodes__ = NODE_CLASS_MAPPINGS
except NameError:
    pass
