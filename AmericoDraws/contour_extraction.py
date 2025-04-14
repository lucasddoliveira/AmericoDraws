"""
Contour extraction module for robotic drawing.

This module contains functions for extracting contours from images.
"""

import cv2
import numpy as np
from PIL import Image
import io
from rembg import remove as rembg_remove


def clean_alpha_edges(image, threshold=10):
    """
    Clean partially transparent edges of an image.
    
    Args:
        image (PIL.Image): Input image with alpha channel
        threshold (int): Alpha threshold below which pixels become fully transparent
        
    Returns:
        PIL.Image: Cleaned image
    """
    # Convert to RGBA if not already
    image = image.convert("RGBA")
    data = np.array(image)

    # Extract alpha channel
    r, g, b, a = data.T

    # Replace partially transparent pixels with full transparency
    mask = a < threshold
    data[..., :-1][mask.T] = (255, 255, 255)  # Make transparent pixels white
    data[..., -1][mask.T] = 0  # Fully transparent

    return Image.fromarray(data)


def erode_alpha(image, pixels=1):
    """
    Erode the alpha channel of an image.
    
    Args:
        image (PIL.Image): Input image with alpha channel
        pixels (int): Number of pixels to erode
        
    Returns:
        PIL.Image: Image with eroded alpha channel
    """
    image = image.convert("RGBA")
    data = np.array(image)
    alpha = data[..., 3]
    kernel = np.ones((3, 3), np.uint8)
    eroded_alpha = cv2.erode(alpha, kernel, iterations=pixels)
    data[..., 3] = eroded_alpha
    return Image.fromarray(data)


def remove_background_ai(input_path, output_path=None, threshold=10, erode_pixels=1):
    """
    Remove background from an image using AI.
    
    Args:
        input_path (str): Path to input image
        output_path (str, optional): Path to save background-removed image
        threshold (int): Threshold for cleaning alpha edges
        erode_pixels (int): Number of pixels to erode from alpha channel
        
    Returns:
        str: Path to the background-removed image
    """
    with open(input_path, "rb") as inp_file:
        img = Image.open(io.BytesIO(inp_file.read()))
        img_no_bg = rembg_remove(img)
        img_no_bg = clean_alpha_edges(img_no_bg, threshold=threshold)
        img_no_bg = erode_alpha(img_no_bg, pixels=erode_pixels)
        
        if output_path:
            img_no_bg.save(output_path, "PNG")
            return output_path
        
        # If no output path, create a temporary file
        temp_path = "temp_bg_removed.png"
        img_no_bg.save(temp_path, "PNG")
        return temp_path


def extract_contours(image_path, threshold1=120, threshold2=191, blur_size=3):
    """
    Extract contours from an image using Canny edge detection.
    
    Args:
        image_path (str): Path to input image
        threshold1 (int): First threshold for Canny edge detector
        threshold2 (int): Second threshold for Canny edge detector
        blur_size (int): Size of Gaussian blur kernel
        
    Returns:
        tuple: Original image, edges, contours, and contour image
    """
    # Load the image in grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        
    # Check image orientation
    height, width = image.shape
    #if height > width:  # If the image is vertical, rotate it 90 degrees
    #    image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)

    # Flood fill from top-left corner to unify background
    flood_filled = image.copy()
    h, w = flood_filled.shape[:2]
    mask = np.zeros((h + 2, w + 2), np.uint8)  # Mask needs to be 2 pixels larger than the image
    cv2.floodFill(flood_filled, mask, seedPoint=(0, 0), newVal=255)  # Flood with white
    cv2.floodFill(flood_filled, mask, seedPoint=(0, 0), newVal=0)    # Then flood with black

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(flood_filled, (blur_size, blur_size), 0)

    # Detect edges using Canny
    edges = cv2.Canny(blurred, threshold1, threshold2)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Create a blank white image
    contour_image = np.ones_like(image) * 255

    # Draw contours with a single pixel width
    cv2.drawContours(contour_image, contours, -1, (0,), 1)

    # Save result
    return image, edges, contours, contour_image
