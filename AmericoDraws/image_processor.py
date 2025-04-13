"""
Main image processing module for robotic drawing.

This module provides the core functionality to process 
images for robotic drawing applications.
"""

import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

from .contour_extraction import remove_background_ai, extract_contours
from .path_planning import process_image, create_points_array
from .visualization import visualization_3d, save_robot_commands


def process_image_for_robot(
    input_path,
    output_dir="output",
    process_cell_size=1,
    points_cell_width=1,
    upper_left_edge=None,
    bottom_right_edge=None,
    z_up=-10,
    save_intermediate_steps=False
):
    """
    Process an image and generate robot arm drawing paths.
    
    Args:
        input_path (str): Path to the input image
        output_dir (str): Directory to save outputs
        process_cell_size (int): Cell size for image processing
        points_cell_width (int): Cell width for point array generation
        upper_left_edge (list): Upper left edge coordinates [x, y, z, a, e, r]
        bottom_right_edge (list): Bottom right edge coordinates [x, y, z, a, e, r]
        z_up (int): Z-axis value for pen-up movement
        save_intermediate_steps (bool): Whether to save intermediate processing images
        
    Returns:
        list: List of points representing the robot path
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Set default parameters if not provided
    if upper_left_edge is None:
        upper_left_edge = [170, 65, -118, -3, 88, -2]
    if bottom_right_edge is None:
        bottom_right_edge = [601, 403, -118, -3, 88, -2]
    
    # Define paths for intermediate files
    bg_removed_path = os.path.join(output_dir, "background_removed.png")
    contour_path = os.path.join(output_dir, "contour.png")
    sketch_path = os.path.join(output_dir, "sketch.png")
    path_3d_path = os.path.join(output_dir, "3d_path.png")
    robot_commands_path = os.path.join(output_dir, "robot_commands.txt")
    
    # Step 1: Remove background and save if requested
    bg_removed_path = remove_background_ai(input_path, bg_removed_path if save_intermediate_steps else None)
    
    # Step 2: Extract contours
    image, edges, contours, contour_image = extract_contours(
        bg_removed_path, 
        threshold1=120, 
        threshold2=191, 
        blur_size=3
    )
    
    if save_intermediate_steps:
        plt.imsave(contour_path, contour_image, cmap='gray')
    
    # Step 3: Convert to matrix
    matrix = process_image(bg_removed_path, process_cell_size)
    
    # Step 4: Create optimized points array
    points = create_points_array(
        matrix,
        points_cell_width,
        upper_left_edge,
        bottom_right_edge,
        z_up=z_up
    )
    
    # Step 5: Visualize and save results
    if save_intermediate_steps:
        visualization_3d(points, path_3d_path, sketch_path)
        save_robot_commands(points, robot_commands_path)
    
    return points