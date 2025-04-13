"""
Visualization module for robotic drawing.

This module provides visualization tools for robotic drawing paths.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.lines import Line2D


def visualization_3d(points, path_3d_filename=None, sketch_filename=None):
    """
    Visualize the 3D path with color-coded pen up/down movements.
    
    Args:
        points (list): List of points for robotic arm movement
        path_3d_filename (str, optional): Filename to save 3D visualization
        sketch_filename (str, optional): Filename to save 2D sketch visualization
    """
    if not points:
        return
        
    # Extract x, y, z coordinates
    xs = [point[0] for point in points]
    ys = [point[1] for point in points]
    zs = [point[2] for point in points]
    
    # Determine pen state for each point (up/down)
    base_z = points[0][2]
    pen_states = ['up' if point[2] > base_z else 'down' for point in points]
    
    # Create colormap: blue for pen down, red for pen up
    colors = ['b' if state == 'down' else 'r' for state in pen_states]
    
    # Create the 3D visualization
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot the path
    for i in range(1, len(points)):
        x_line = [xs[i-1], xs[i]]
        y_line = [ys[i-1], ys[i]]
        z_line = [zs[i-1], zs[i]]
        ax.plot(x_line, y_line, z_line, color=colors[i], linewidth=1)
    
    # Plot points
    ax.scatter(xs, ys, zs, c=colors, marker='o', s=20, edgecolors='none')
    
    # Add start and end markers
    ax.scatter([xs[0]], [ys[0]], [zs[0]], c='g', marker='o', s=100, label='Start')
    ax.scatter([xs[-1]], [ys[-1]], [zs[-1]], c='y', marker='o', s=100, label='End')
    
    # Set labels and title
    ax.set_xlabel('X (mm)')
    ax.set_ylabel('Y (mm)')
    ax.set_zlabel('Z (mm)')
    ax.set_title('Robotic Arm Path')
    
    # Add legend
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor='b', markersize=10, label='Pen Down'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='r', markersize=10, label='Pen Up'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='g', markersize=10, label='Start'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='y', markersize=10, label='End')
    ]
    ax.legend(handles=legend_elements, loc='upper right')
    
    # Save the figure if filename provided
    if path_3d_filename:
        plt.savefig(path_3d_filename, bbox_inches='tight', dpi=300)
    
    # Create a top-down view for the 2D sketch
    if sketch_filename:
        fig2 = plt.figure(figsize=(10, 10))
        ax2 = fig2.add_subplot(111)
        
        # Plot only pen-down segments for the sketch
        for i in range(1, len(points)):
            if pen_states[i] == 'down' and pen_states[i-1] == 'down':
                ax2.plot([xs[i-1], xs[i]], [ys[i-1], ys[i]], 'b-', linewidth=1.0)
        
        ax2.set_xlabel('X (mm)')
        ax2.set_ylabel('Y (mm)')
        ax2.set_title('Drawing Path (Top View)')
        ax2.set_aspect('equal')
        ax2.invert_yaxis()  # Correct orientation
        
        plt.savefig(sketch_filename, bbox_inches='tight', dpi=600)
        plt.close(fig2)
    
    plt.close(fig)


def save_robot_commands(commands, filename):
    """
    Save the robot commands to a file.
    
    Args:
        commands (list): List of robot movement commands
        filename (str): Path to save the commands
    """
    with open(filename, 'w') as f:
        for cmd in commands:
            f.write(f"{cmd[0]:.2f},{cmd[1]:.2f},{cmd[2]:.2f},{cmd[3]:.2f},{cmd[4]:.2f},{cmd[5]:.2f}\n")
    print(f"Saved {len(commands)} robot commands to {filename}")