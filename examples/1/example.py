import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Define your input/output paths
input_image = "examples/1/input.png"
output_directory = "examples/1/output"

from AmericoDraws import independencia_ou_morte

# Call the function
points = independencia_ou_morte(
    input_image,
    output_directory,
    process_cell_size=1,
    points_cell_width=1,
    upper_left_edge=None,
    bottom_right_edge=None,
    z_up=10,
    remove_background=True,
    # Background removal parameters
    bg_threshold=10,
    bg_erode_pixels=1,
    # Contour extraction parameters
    threshold1=120,
    threshold2=191,
    blur_size=3,
    # Path optimization parameters
    distance_threshold=3,
    epsilon=1
)

print(f"Generated {len(points)} points for robot drawing path")