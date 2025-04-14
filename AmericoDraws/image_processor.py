
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

def independencia_ou_morte(
    input_path,
    output_dir="output",
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
    epsilon=0.25
):
    """
    Process an image and generate robot arm drawing paths.
    Always saves intermediate processing steps for visualization and debugging.
    
    Args:
        input_path (str): Path to the input image
        output_dir (str): Directory to save outputs
        process_cell_size (int): Cell size for image processing
        points_cell_width (int): Cell width for point array generation
        upper_left_edge (list): Upper left edge coordinates [x, y, z, a, e, r]
        bottom_right_edge (list): Bottom right edge coordinates [x, y, z, a, e, r]
        z_up (int): Z-axis value for pen-up movement
        remove_background (bool): Whether to remove the background from the image
        bg_threshold (int): Threshold for cleaning alpha edges during background removal
        bg_erode_pixels (int): Number of pixels to erode from alpha channel
        threshold1 (int): First threshold for Canny edge detection
        threshold2 (int): Second threshold for Canny edge detection
        blur_size (int): Size of Gaussian blur kernel for edge detection
        distance_threshold (int): Threshold for filtering points based on distance
        epsilon (float): Epsilon value for Douglas-Peucker algorithm for path simplification
        
    Returns:
        list: List of points representing the robot path
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Set default parameters if not provided
    if upper_left_edge is None:
        upper_left_edge = [0, 1000, 0, 0, 0, 0]
    if bottom_right_edge is None:
        bottom_right_edge = [1000, 0, 0, 0, 0, 0]
    
    # Define paths for intermediate files
    bg_removed_path = os.path.join(output_dir, "background_removed.png")
    contour_path = os.path.join(output_dir, "contour.png")
    sketch_path = os.path.join(output_dir, "final_result.png")
    path_3d_path = os.path.join(output_dir, "3d_path.png")
    robot_commands_path = os.path.join(output_dir, "robot_commands.txt")
    
    # Step 1: Remove background if requested, otherwise use original image
    if remove_background:
        processing_image_path = remove_background_ai(
            input_path, 
            bg_removed_path,  # Always save background removal result
            threshold=bg_threshold,
            erode_pixels=bg_erode_pixels
        )
    else:
        processing_image_path = input_path
        # Always save a copy of the original image
        img = Image.open(input_path)
        img.save(bg_removed_path)
    
    # Step 2: Extract contours
    image, edges, contours, contour_image = extract_contours(
        processing_image_path, 
        threshold1=threshold1, 
        threshold2=threshold2, 
        blur_size=blur_size
    )
    
    # Always save contour image
    plt.imsave(contour_path, contour_image, cmap='gray')
    
    # Step 3: Convert to matrix
    matrix = process_image(contour_path, process_cell_size)
    
    # Step 4: Create optimized points array
    points = create_points_array(
        matrix,
        points_cell_width,
        upper_left_edge,
        bottom_right_edge,
        z_up=z_up,
        distance_threshold=distance_threshold,
        epsilon=epsilon
    )
    
    # Step 5: Always visualize and save results
    visualization_3d(points, upper_left_edge, bottom_right_edge, path_3d_path, sketch_path)
    save_robot_commands(points, robot_commands_path)
    
    return points