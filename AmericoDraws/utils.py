"""
Utility functions for the robotic drawer library.
"""

import os
import shutil
import numpy as np


def ensure_directory(directory):
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        directory (str): Directory path
    """
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)


def clean_output_directory(directory):
    """
    Clean an output directory, removing all files.
    
    Args:
        directory (str): Directory path to clean
    """
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory, exist_ok=True)


def scale_coordinates(points, scale_factor):
    """
    Scale the x, y coordinates of points by a factor.
    
    Args:
        points (list): List of points to scale
        scale_factor (float): Scale factor
        
    Returns:
        list: Scaled points
    """
    scaled_points = []
    for point in points:
        scaled_point = point.copy()
        scaled_point[0] *= scale_factor
        scaled_point[1] *= scale_factor
        scaled_points.append(scaled_point)
    return scaled_points


def rotate_coordinates(points, angle_degrees):
    """
    Rotate the x, y coordinates of points by an angle.
    
    Args:
        points (list): List of points to rotate
        angle_degrees (float): Rotation angle in degrees
        
    Returns:
        list: Rotated points
    """
    angle_radians = np.radians(angle_degrees)
    cos_theta = np.cos(angle_radians)
    sin_theta = np.sin(angle_radians)
    
    rotated_points = []
    for point in points:
        x, y = point[0], point[1]
        new_x = x * cos_theta - y * sin_theta
        new_y = x * sin_theta + y * cos_theta
        
        rotated_point = point.copy()
        rotated_point[0] = new_x
        rotated_point[1] = new_y
        rotated_points.append(rotated_point)
    
    return rotated_points


def translate_coordinates(points, dx, dy, dz=0):
    """
    Translate the coordinates of points.
    
    Args:
        points (list): List of points to translate
        dx (float): X-axis translation
        dy (float): Y-axis translation
        dz (float, optional): Z-axis translation
        
    Returns:
        list: Translated points
    """
    translated_points = []
    for point in points:
        translated_point = point.copy()
        translated_point[0] += dx
        translated_point[1] += dy
        if dz != 0:
            translated_point[2] += dz
        translated_points.append(translated_point)
    
    return translated_points


def merge_paths(paths_list):
    """
    Merge multiple paths into a single path with pen-up movements between them.
    
    Args:
        paths_list (list): List of path lists to merge
        
    Returns:
        list: Merged path
    """
    if not paths_list:
        return []
    
    merged_path = []
    for path in paths_list:
        if not path:
            continue
            
        if merged_path:
            # Get last point from current merged path
            last_point = merged_path[-1]
            # Get first point from new path
            first_point = path[0]
            
            # Add pen-up movement
            z_up = 10  # Pen-up distance, might need to be configurable
            pen_up_point = last_point.copy()
            pen_up_point[2] += z_up
            merged_path.append(pen_up_point)
            
            # Move to new path start (pen up)
            travel_point = first_point.copy()
            travel_point[2] += z_up
            merged_path.append(travel_point)
            
            # Lower pen at new position
            merged_path.append(first_point.copy())
            
            # Add the rest of the new path
            merged_path.extend(path[1:])
        else:
            merged_path.extend(path)
    
    return merged_path


def optimize_path(points, simplification_epsilon=0.1):
    """
    Optimize a path by removing redundant points.
    
    Args:
        points (list): List of points to optimize
        simplification_epsilon (float): Simplification epsilon for Douglas-Peucker
        
    Returns:
        list: Optimized path
    """
    if len(points) <= 2:
        return points
    
    # Use Douglas-Peucker algorithm for line simplification
    def simplify_line(pts, epsilon):
        if len(pts) <= 2:
            return pts
            
        # Find point with max distance from line between first and last
        max_dist = 0
        index = 0
        start, end = pts[0], pts[-1]
        
        # Calculate distances for all points to the line
        for i in range(1, len(pts) - 1):
            # Calculate perpendicular distance
            if end[0] == start[0]:  # Vertical line
                dist = abs(pts[i][0] - start[0])
            else:
                # Line equation: ax + by + c = 0
                a = (end[1] - start[1]) / (end[0] - start[0])
                b = -1
                c = start[1] - a * start[0]
                dist = abs(a * pts[i][0] + b * pts[i][1] + c) / np.sqrt(a**2 + b**2)
                
            if dist > max_dist:
                max_dist = dist
                index = i
        
        # If max distance > epsilon, recursively simplify
        if max_dist > epsilon:
            first_segment = simplify_line(pts[:index + 1], epsilon)
            second_segment = simplify_line(pts[index:], epsilon)
            return first_segment[:-1] + second_segment
        else:
            return [pts[0], pts[-1]]
    
    # Extract points with pen up/down information
    pen_states = []
    grouped_points = []
    current_group = []
    current_pen_state = None
    
    # Group points by pen state
    for i, point in enumerate(points):
        # Determine pen state based on z-coordinate relative to base z
        pen_state = 'up' if i > 0 and point[2] > points[0][2] else 'down'
        
        if current_pen_state is None:
            current_pen_state = pen_state
            
        if pen_state != current_pen_state:
            # Pen state changed, save current group
            if current_group:
                grouped_points.append(current_group)
                pen_states.append(current_pen_state)
            current_group = [point]
            current_pen_state = pen_state
        else:
            current_group.append(point)
    
    # Add the last group
    if current_group:
        grouped_points.append(current_group)
        pen_states.append(current_pen_state)
    
    # Simplify only pen-down segments
    optimized_groups = []
    for group, state in zip(grouped_points, pen_states):
        if state == 'down' and len(group) > 2:
            # Simplify the pen-down path
            xy_points = [p[:2] for p in group]  # Extract X,Y coordinates
            simplified_xy = simplify_line(xy_points, simplification_epsilon)
            
            # Reconstruct full points with original z,a,e,r values
            simplified_group = []
            for x, y in simplified_xy:
                # Find closest original point
                min_dist = float('inf')
                best_match = None
                for orig_point in group:
                    dist = (orig_point[0] - x)**2 + (orig_point[1] - y)**2
                    if dist < min_dist:
                        min_dist = dist
                        best_match = orig_point
                simplified_group.append(best_match)
            
            optimized_groups.append(simplified_group)
        else:
            # Keep pen-up movements as is
            optimized_groups.append(group)
    
    # Concatenate all groups back together
    optimized_path = []
    for group in optimized_groups:
        optimized_path.extend(group)
    
    return optimized_path