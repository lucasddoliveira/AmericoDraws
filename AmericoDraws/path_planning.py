"""
Path planning module for robotic drawing.

This module handles conversion of contours to robot paths.
"""

import numpy as np
from PIL import Image


def process_image(input_path, cell_size=1):
    """
    Process an image into a binary matrix.
    
    Args:
        input_path (str): Path to input image
        cell_size (int): Size of each cell in the grid
        
    Returns:
        list: 2D binary matrix where 1 represents black pixels
    """
    img = Image.open(input_path).convert("L")
    width, height = img.size
    img_array = np.array(img)
    
    grid_rows = height // cell_size
    grid_cols = width // cell_size
    matrix = np.zeros((grid_rows, grid_cols), dtype=int)
    for i in range(grid_rows):
        for j in range(grid_cols):
            # For cell_size=1, each cell is a single pixel
            matrix[i, j] = 1 if img_array[i, j] < 128 else 0

    return matrix.tolist()


def create_points_array(matrix, cell_width, upper_left_edge, bottom_right_edge, 
                        z_up=10, z_down=0, distance_threshold=3, epsilon=0.25):
    """
    Create optimized points array for robotic arm movement.
    
    Args:
        matrix (list): 2D binary matrix
        cell_width (int): Width of each cell
        upper_left_edge (list): Upper left edge coordinates [x, y, z, a, e, r]
        bottom_right_edge (list): Bottom right edge coordinates [x, y, z, a, e, r]
        z_up (int): Z-axis value for pen-up movement
        z_down (int): Z-axis value for pen-down movement
        distance_threshold (float): Distance threshold for pen up/down decisions
        epsilon (float): Simplification tolerance for Douglas-Peucker algorithm
        
    Returns:
        list: Optimized list of points for robotic arm movement
    """
    import numpy as np
    
    height = len(matrix)
    width = len(matrix[0]) if height > 0 else 0

    total_width = bottom_right_edge[0] - upper_left_edge[0]
    total_height = bottom_right_edge[1] - upper_left_edge[1]
    
    step_x = total_width / width
    step_y = total_height / height
    
    # Prepare to collect points.
    points = []
    visited = set()
    
    def get_neighbors(i, j):
        # Only consider direct neighbors (up, down, left, right)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        return [(i+di, j+dj) for di, dj in directions if 0 <= i+di < height and 0 <= j+dj < width]
    
    def trace_sequence(i, j):
        # Use BFS instead of DFS to ensure connected components stay together
        queue = [(i, j)]
        sequence = []
        local_visited = set([(i, j)])  # Track visited cells for this sequence
        
        while queue:
            ci, cj = queue.pop(0)  # BFS uses queue (FIFO)
            if (ci, cj) in visited:
                continue
            visited.add((ci, cj))
            
            # Convert to physical coordinates
            x = round(upper_left_edge[0] + cj * step_x + cell_width/2)
            y = round(upper_left_edge[1] + ci * step_y + cell_width/2)
            z = round(upper_left_edge[2])
            a = round(upper_left_edge[3])
            e = round(upper_left_edge[4])
            r = round(upper_left_edge[5])
            
            sequence.append([x, y, z, a, e, r])
            
            for ni, nj in get_neighbors(ci, cj):
                if matrix[ni][nj] == 1 and (ni, nj) not in visited and (ni, nj) not in local_visited:
                    queue.append((ni, nj))
                    local_visited.add((ni, nj))  # Mark as to-be-visited
        
        return sequence
    
    # Douglas-Peucker line simplification algorithm
    def simplify_line(points, epsilon):
        if len(points) <= 2:
            return points
        
        # Find the point with the maximum distance from line between start and end
        max_dist = 0
        index = 0
        start, end = points[0], points[-1]
        
        # Line equation: ax + by + c = 0
        if end[0] == start[0]:  # Vertical line
            for i in range(1, len(points) - 1):
                dist = abs(points[i][0] - start[0])
                if dist > max_dist:
                    max_dist = dist
                    index = i
        else:
            a = (end[1] - start[1]) / (end[0] - start[0])
            b = -1
            c = start[1] - a * start[0]
            
            for i in range(1, len(points) - 1):
                dist = abs(a * points[i][0] + b * points[i][1] + c) / np.sqrt(a**2 + b**2)
                if dist > max_dist:
                    max_dist = dist
                    index = i
        
        # If max distance is greater than epsilon, recursively simplify
        if max_dist > epsilon:
            # Recursive call
            first_segment = simplify_line(points[:index + 1], epsilon)
            second_segment = simplify_line(points[index:], epsilon)
            
            # Build the result (avoid duplicating the connection point)
            return first_segment[:-1] + second_segment
        else:
            # All points are within epsilon distance from the line
            return [points[0], points[-1]]
    
    # Collect all sequences
    sequences = []
    for i in range(height):
        for j in range(width):
            if matrix[i][j] == 1 and (i, j) not in visited:
                sequences.append(trace_sequence(i, j))
    
    # Apply line simplification to each sequence
    simplified_sequences = []
    for seq in sequences:
        points_only = [p[:2] for p in seq]  # Extract x,y coordinates
        simplified_points = simplify_line(points_only, epsilon)
        
        # Reconstruct full 6D points with original z,a,e,r values
        simplified_seq = []
        for x, y in simplified_points:
            # Find the closest original point to get its z,a,e,r values
            min_dist = float('inf')
            best_match = None
            for orig_point in seq:
                dist = (orig_point[0] - x)**2 + (orig_point[1] - y)**2
                if dist < min_dist:
                    min_dist = dist
                    best_match = orig_point
            
            simplified_seq.append([x, y, best_match[2], best_match[3], best_match[4], best_match[5]])
        
        simplified_sequences.append(simplified_seq)
    
    # Optimize sequence order to minimize travel distance
    optimized_sequences = []
    current_pos = None
    remaining_sequences = list(range(len(simplified_sequences)))
    
    while remaining_sequences:
        if current_pos is None:
            # Start with the first sequence
            next_seq = 0
            # Add the first sequence as is
            optimized_sequences.append(simplified_sequences[next_seq])
            current_pos = simplified_sequences[next_seq][-1][:2]  # Just need x, y coords
            remaining_sequences.remove(next_seq)
        else:
            # Find the closest sequence
            min_dist = float('inf')
            next_seq = None
            seq_should_reverse = False
            
            for i in remaining_sequences:
                # Check distance to the start of the sequence
                start_dist = np.sqrt((current_pos[0] - simplified_sequences[i][0][0])**2 + 
                                    (current_pos[1] - simplified_sequences[i][0][1])**2)
                
                # Check distance to the end of the sequence
                end_dist = np.sqrt((current_pos[0] - simplified_sequences[i][-1][0])**2 + 
                                  (current_pos[1] - simplified_sequences[i][-1][1])**2)
                
                # Choose the closest end of the sequence
                if start_dist < min_dist:
                    min_dist = start_dist
                    next_seq = i
                    seq_should_reverse = False
                
                if end_dist < min_dist:
                    min_dist = end_dist
                    next_seq = i
                    seq_should_reverse = True
            
            # Reverse the sequence if needed to start from the closest end
            if seq_should_reverse:
                optimized_sequences.append(simplified_sequences[next_seq][::-1])
            else:
                optimized_sequences.append(simplified_sequences[next_seq])
            
            # Update current position to the last point of the added sequence
            current_pos = optimized_sequences[-1][-1][:2]
            remaining_sequences.remove(next_seq)
    
    # Now optimize points within each sequence
    for i in range(len(optimized_sequences)):
        # Skip sequences with less than 3 points (no reordering needed)
        if len(optimized_sequences[i]) < 3:
            continue
        
        # Extract first and last point - they should remain first and last
        first_point = optimized_sequences[i][0]
        remaining_points = optimized_sequences[i][1:]
        
        # Create optimized path starting from the first point
        optimized_path = [first_point]
        remaining_indices = list(range(len(remaining_points)))
        
        current_point = first_point
        while remaining_indices:
            # Find closest remaining point
            min_dist = float('inf')
            closest_idx = None
            
            for idx in remaining_indices:
                point = remaining_points[idx]
                dist = np.sqrt((current_point[0] - point[0])**2 + (current_point[1] - point[1])**2)
                
                if dist < min_dist:
                    min_dist = dist
                    closest_idx = idx
            
            # Add closest point to optimized path
            closest_point = remaining_points[closest_idx]
            optimized_path.append(closest_point)
            
            # Update current point and remove added point from remaining
            current_point = closest_point
            remaining_indices.remove(closest_idx)
        
        # Replace original sequence with optimized one
        optimized_sequences[i] = optimized_path
    
    # Create the final path with pen up/down movements
    path = []
    for seq in optimized_sequences:
        if path:
            # Get the last point's coordinates
            last_x, last_y, last_z, last_a, last_e, last_r = path[-1]
            new_x, new_y = seq[0][0], seq[0][1]
            
            # Calculate distance to the new sequence
            dist = np.sqrt((new_x - last_x)**2 + (new_y - last_y)**2)
            
            # If distance is large, add pen up/down movements
            if dist > distance_threshold:
                # Lift the pen at current position
                path.append([last_x, last_y, last_z + z_up, last_a, last_e, last_r])
                # Move to new sequence start (pen up)
                path.append([new_x, new_y, seq[0][2] + z_up, seq[0][3], seq[0][4], seq[0][5]])
                # Lower the pen at new position
                path.append([new_x, new_y, seq[0][2], seq[0][3], seq[0][4], seq[0][5]])
            else:
                # Direct movement to the next sequence (pen down)
                path.append([new_x, new_y, seq[0][2], seq[0][3], seq[0][4], seq[0][5]])
        
        # Add the current sequence
        path.extend(seq)
    
    # Make sure we end with pen up
    if path:
        last_point = path[-1]
        path.append([last_point[0], last_point[1], last_point[2] + z_up, 
                    last_point[3], last_point[4], last_point[5]])
    
    # Remove duplicate consecutive points
    result = []
    for item in path:
        if not result or item != result[-1]:
            result.append(item)

    return result