"""Machine features for gear parts (bore, keyway)."""

from __future__ import annotations

from build123d import Align, Box, Cylinder, Part, Pos


def add_bore(part: Part, diameter: float) -> Part:
    """Add a bore (cylindrical hole) to the center of the part."""
    if diameter <= 0:
        raise ValueError("diameter must be positive")
    bbox = part.bounding_box()
    margin = 1.0  # 上下に少しはみ出す
    height = (bbox.max.Z - bbox.min.Z) + 2 * margin  # 確実に貫通させる
    bore = Cylinder(
        radius=diameter / 2, height=height, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    bore = Pos(0, 0, bbox.min.Z - margin) * bore  # 中心に配置+Z調整
    return part - bore


def add_keyway(part: Part, bore_diameter: float, width: float, depth: float) -> Part:
    """Cut a rectangular keyway extendeding outward from the bore edge."""
    if bore_diameter <= 0:
        raise ValueError("bore_diameter must be positive")
    if width <= 0 or depth <= 0:
        raise ValueError("width and depth must be positive")
    r = bore_diameter / 2
    key_len = r + depth  # 軸穴中心から外線まで
    bbox = part.bounding_box()
    margin = 1.0  # 上下に少しはみ出す
    height = (bbox.max.Z - bbox.min.Z) + 2 * margin  # 確実に貫通させる
    keyway = Box(width, key_len, height, align=(Align.CENTER, Align.CENTER, Align.MIN))
    keyway = Pos(0, key_len / 2, bbox.min.Z - margin) * keyway  # 縁に配置+Z調整
    return part - keyway
