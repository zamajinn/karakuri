from build123d import *
from pathlib import Path

# Create output directory if it doesn't exist
script_dir = Path(__file__).parent
output_dir = script_dir.parent / "output"
output_dir.mkdir(exist_ok=True)

cyl = Cylinder(radius=10, height=5)
hole = Cylinder(radius=3, height=5)
result = cyl - hole
export_stl(result, output_dir / "cyl_with_hole.stl") 