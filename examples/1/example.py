import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from AmericoDraws import independencia_ou_morte

# Call the function
points = independencia_ou_morte(
    input_path = "examples/1/input.png",
    output_dir="examples/1/output",
    process_cell_size=1,
    points_cell_width=1,
    upper_left_edge=[170, 65, -118, -3, 88, -2],
    bottom_right_edge=[601, 403, -118, -3, 88, -2],
    z_up=-10,
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
    epsilon=5,
    # Final Result Image
    linewidth=1
)

print(f"Generated {len(points)} points for robot drawing path")