import sys
import os
from unittest.mock import MagicMock

for mod in ['folder_paths', 'node_helpers', 'comfy', 'comfy.sd',
            'comfy.sample', 'comfy.utils', 'comfy.model_management']:
    sys.modules[mod] = MagicMock()

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from wan_alpha_nodes import _build_vp9_cmd, _build_vp8_cmd


def test_vp9_cmd_contains_quality_flags():
    cmd = _build_vp9_cmd("/usr/bin/ffmpeg", "/tmp/frames", 24, 13, "/out/video.webm")
    assert cmd[0] == "/usr/bin/ffmpeg"
    assert cmd[-1] == "/out/video.webm"
    assert "-deadline" in cmd
    assert cmd[cmd.index("-deadline") + 1] == "best"
    assert "-cpu-used" in cmd
    assert cmd[cmd.index("-cpu-used") + 1] == "0"
    assert "-pix_fmt" in cmd
    assert cmd[cmd.index("-pix_fmt") + 1] == "yuva420p"
    assert "-c:v" in cmd
    assert cmd[cmd.index("-c:v") + 1] == "libvpx-vp9"
    assert "-b:v" in cmd
    assert cmd[cmd.index("-b:v") + 1] == "0"
    assert "-crf" in cmd
    assert cmd[cmd.index("-crf") + 1] == "13"
    assert "-auto-alt-ref" in cmd
    assert cmd[cmd.index("-auto-alt-ref") + 1] == "0"


def test_vp9_cmd_crf_value_is_passed_through():
    cmd_high = _build_vp9_cmd("/ffmpeg", "/tmp", 24, 1, "/out.webm")
    cmd_low  = _build_vp9_cmd("/ffmpeg", "/tmp", 24, 62, "/out.webm")
    assert cmd_high[cmd_high.index("-crf") + 1] == "1"
    assert cmd_low[cmd_low.index("-crf") + 1] == "62"


def test_vp8_cmd_contains_quality_flags():
    cmd = _build_vp8_cmd("/usr/bin/ffmpeg", "/tmp/frames", 24, 13, "/out/video.webm")
    assert cmd[0] == "/usr/bin/ffmpeg"
    assert cmd[-1] == "/out/video.webm"
    assert "-filter_complex" in cmd
    assert "alphaextract" in cmd[cmd.index("-filter_complex") + 1]
    assert "-c:v" in cmd
    assert cmd[cmd.index("-c:v") + 1] == "libvpx"
    assert "-quality" in cmd
    assert cmd[cmd.index("-quality") + 1] == "best"
    assert "-cpu-used" in cmd
    assert cmd[cmd.index("-cpu-used") + 1] == "0"
    assert "-crf" in cmd
    assert cmd[cmd.index("-crf") + 1] == "13"
    assert "-b:v" in cmd
    assert cmd[cmd.index("-b:v") + 1] == "50M"
    assert "-qmin" not in cmd
    assert "-qmax" not in cmd
    assert "-auto-alt-ref" in cmd
    assert cmd[cmd.index("-auto-alt-ref") + 1] == "0"


def test_vp8_cmd_maps_both_streams():
    cmd = _build_vp8_cmd("/ffmpeg", "/tmp", 24, 20, "/out.webm")
    map_positions = [i for i, v in enumerate(cmd) if v == "-map"]
    assert len(map_positions) == 2, "Both color and alpha streams must be mapped"


def test_vp8_cmd_crf_value_is_passed_through():
    cmd = _build_vp8_cmd("/ffmpeg", "/tmp", 24, 50, "/out.webm")
    assert cmd[cmd.index("-crf") + 1] == "50"


def test_vp9_quality_to_crf_formula():
    def q_to_crf(q):
        return max(1, int(63 - (q / 100.0) * 62))
    assert q_to_crf(100) == 1
    assert q_to_crf(80)  == 13
    assert q_to_crf(50)  == 32
    assert q_to_crf(1)   == 62


def test_vp8_quality_to_crf_formula():
    def q_to_crf(q):
        return max(1, int(63 - (q / 100.0) * 62))
    assert q_to_crf(100) == 1
    assert q_to_crf(80)  == 13
    assert q_to_crf(50)  == 32
    assert q_to_crf(1)   == 62
