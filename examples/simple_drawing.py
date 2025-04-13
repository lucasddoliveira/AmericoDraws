"""
Simple example of using the robotic_drawer library.
"""

import os
import argparse
from AmericoDraws.image_processor import process_image_for_robot
from AmericoDraws.visualization import visualization_3d, save_robot_commands
from AmericoDraws.utils import scale_coordinates, rotate_coordinates


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Process an image for robotic drawing.')
    parser.add_argument('image_path', type=str, help='Path to the input image')
    parser.add_argument('--output-dir', type=str, default='output', help='Directory to save outputs')
    parser.add_argument('--scale', type=float, default=1.0, help='Scale factor for the drawing')
    parser.add_argument('--rotate', type=float, default=0.0, help='Rotation angle in degrees')
    parser.add_argument('--z-up', type=int, default=-10, help='Z-axis value for pen-up movement')
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    print(f"Processing image: {args.image_path}")
    print(f"Output directory: {args.output_dir}")
    
    # Process the image
    points = process_image_for_robot(
        args.image_path,
        output_dir=args.output_dir,
        z_up=args.z_up,
        save_intermediate_steps=True
    )
    
    # Apply transformations if needed
    if args.scale != 1.0:
        print(f"Scaling drawing by factor of {args.scale}")
        points = scale_coordinates(points, args.scale)
    
    if args.rotate != 0.0:
        print(f"Rotating drawing by {args.rotate} degrees")
        points = rotate_coordinates(points, args.rotate)
    
    # Visualize the results
    visualization_3d(
        points, 
        path_3d_filename=os.path.join(args.output_dir, "3d_path_final.png"),
        sketch_filename=os.path.join(args.output_dir, "sketch_final.png")
    )
    
    # Save robot commands
    save_robot_commands(
        points, 
        os.path.join(args.output_dir, "robot_commands_final.txt")
    )
    
    print(f"Generated {len(points)} robot movement points")
    print(f"Results saved to {args.output_dir}")


if __name__ == "__main__":
    main()