"""
Wan-Alpha Custom Nodes Package for ComfyUI
This package provides nodes for generating videos with transparency using Wan-Alpha.
"""

from .wan_alpha_nodes import (
    WanAlphaVideoGenerator,
    FrameRateCalculator,
    ImageLoaderForVideo,
    SaveWebmWithAlpha,
    NODE_CLASS_MAPPINGS,
    NODE_DISPLAY_NAME_MAPPINGS,
)

__all__ = [
    "WanAlphaVideoGenerator",
    "FrameRateCalculator", 
    "ImageLoaderForVideo",
    "SaveWebmWithAlpha",
    "NODE_CLASS_MAPPINGS",
    "NODE_DISPLAY_NAME_MAPPINGS",
]

# ComfyUI expects these exports
__nodes__ = NODE_CLASS_MAPPINGS
