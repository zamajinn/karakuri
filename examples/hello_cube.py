from pathlib import Path

from build123d import Box, export_stl

# Create output directory if it doesn't exist
script_dir = Path(__file__).parent
output_dir = script_dir.parent / "output"
output_dir.mkdir(exist_ok=True)

# make a box
cube = Box(10, 10, 10)

# output stl file
export_stl(cube, output_dir / "hello.stl")
