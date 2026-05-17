"""Generate an involute spur gear 3D model with build123d."""

from __future__ import annotations

import argparse
import math
from pathlib import Path

from build123d import (
    BuildLine,
    BuildSketch,
    Circle,
    Line,
    PolarLocations,
    Spline,
    ThreePointArc,
    Part,
    add,
    export_stl,
    extrude,
    make_face,
)


def _involute_xy(rb: float, t: float) -> tuple[float, float]:
    # Involute of the base circle, parameterized so that increasing t
    # spirals clockwise (polar angle decreases from the +x axis).
    # Used as the +y-side (upper) flank of a tooth whose centerline
    # lies on +x; the -y-side flank is its mirror across the x axis.
    return (
        rb * (math.cos(t) + t * math.sin(t)),
        rb * (t * math.cos(t) - math.sin(t)),
    )


def _rotate(p: tuple[float, float], angle: float) -> tuple[float, float]:
    c, s = math.cos(angle), math.sin(angle)
    return (p[0] * c - p[1] * s, p[0] * s + p[1] * c)


def make_spur_gear(
    teeth: int,
    module: float,
    pressure_angle: float = 20.0,
    tooth_height_factor: float = 2.25,
    thickness: float = 10.0,
    flank_segments: int = 24,
) -> Part:
    """Build a spur gear with an involute tooth profile.

    Args:
        teeth: Number of teeth (z), must be >= 4.
        module: Module m in mm; pitch diameter = m * z.
        pressure_angle: Pressure angle in degrees (standard 20).
        tooth_height_factor: Total tooth-height coefficient. The standard
            value 2.25 corresponds to addendum 1.0*m and dedendum 1.25*m;
            other values are split using the same 1.0 : 1.25 ratio.
        thickness: Gear face width (extrusion length) in mm.
        flank_segments: Number of sample points per involute flank.

    Returns:
        A build123d Part representing the gear.
    """
    if teeth < 4:
        raise ValueError("teeth must be >= 4")
    if module <= 0:
        raise ValueError("module must be positive")
    if thickness <= 0:
        raise ValueError("thickness must be positive")

    addendum_factor = tooth_height_factor * (1.0 / 2.25)
    dedendum_factor = tooth_height_factor * (1.25 / 2.25)

    alpha = math.radians(pressure_angle)
    z = teeth
    m = module

    rp = m * z / 2.0
    rb = rp * math.cos(alpha)
    ra = rp + addendum_factor * m
    rf = rp - dedendum_factor * m

    if rf <= 0:
        raise ValueError("root radius is non-positive; check parameters")

    inv_alpha = math.tan(alpha) - alpha
    # Rotate the involute so that the upper-flank pitch point sits at +pi/(2z)
    # relative to the tooth centerline. With the CW-spiral _involute_xy,
    # the pitch point's unrotated polar angle is -inv(alpha), so we add
    # inv(alpha) to land it at +pi/(2z) after rotation.
    flank_rot = math.pi / (2 * z) + inv_alpha

    r_inv_start = max(rb, rf)
    t_start = (
        math.sqrt((r_inv_start / rb) ** 2 - 1) if r_inv_start > rb else 0.0
    )
    t_tip = math.sqrt((ra / rb) ** 2 - 1)

    upper = [
        _rotate(
            _involute_xy(rb, t_start + (t_tip - t_start) * i / flank_segments),
            flank_rot,
        )
        for i in range(flank_segments + 1)
    ]
    lower = [(x, -y) for (x, y) in upper]

    needs_root_extension = rf < rb
    if needs_root_extension:
        upper_root_pt = (rf * math.cos(flank_rot), rf * math.sin(flank_rot))
    else:
        upper_root_pt = upper[0]
    lower_root_pt = (upper_root_pt[0], -upper_root_pt[1])

    # Single tooth: a closed region bounded by both flanks, the tip arc,
    # and a short arc along the root circle. The tooth centerline lies on +x.
    # Wire is traced so the tooth interior sits on its left (CCW for OCCT).
    with BuildSketch() as tooth_sk:
        with BuildLine():
            if needs_root_extension:
                Line(upper_root_pt, upper[0])
                Spline(*upper)
            else:
                Spline(*upper)
            ThreePointArc(upper[-1], (ra, 0.0), lower[-1])
            Spline(*list(reversed(lower)))
            if needs_root_extension:
                Line(lower[0], lower_root_pt)
            ThreePointArc(lower_root_pt, (rf, 0.0), upper_root_pt)
        make_face()

    # Base disk + z copies of the tooth arranged around the axis.
    with BuildSketch() as gear_sk:
        Circle(rf)
        with PolarLocations(0, z):
            add(tooth_sk.sketch)

    return extrude(gear_sk.sketch, amount=thickness)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate an involute spur gear STL with build123d."
    )
    parser.add_argument("--teeth", "-z", type=int, required=True,
                        help="number of teeth")
    parser.add_argument("--module", "-m", type=float, required=True,
                        help="module in mm")
    parser.add_argument("--pressure-angle", type=float, default=20.0,
                        help="pressure angle in degrees (default 20)")
    parser.add_argument("--tooth-height-factor", type=float, default=2.25,
                        help="total tooth-height coefficient (default 2.25)")
    parser.add_argument("--thickness", type=float, default=10.0,
                        help="gear face width in mm (default 10)")
    parser.add_argument("--output", "-o", type=str, default=None,
                        help="output STL path (default: ../output/spur_gear_z*_m*.stl)")
    args = parser.parse_args()

    gear = make_spur_gear(
        teeth=args.teeth,
        module=args.module,
        pressure_angle=args.pressure_angle,
        tooth_height_factor=args.tooth_height_factor,
        thickness=args.thickness,
    )

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
    else:
        out_dir = Path(__file__).parents[2] / "output"
        out_dir.mkdir(exist_ok=True)
        out_path = out_dir / f"spur_gear_z{args.teeth}_m{args.module}.stl"

    export_stl(gear, str(out_path))
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
