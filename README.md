# AmericoDraws

A Python library for processing images and converting them into robotic arm drawing paths.

## Installation

```bash
pip install robotic-drawer
```

Or install from source:

```bash
git clone https://github.com/yourusername/robotic_drawer.git
cd robotic_drawer
pip install -e .
```

## Dependencies

- Python 3.7+
- NumPy
- Matplotlib
- OpenCV
- Pillow
- scikit-learn
- NetworkX
- rembg (for background removal)

## Usage

### Basic Usage

```python
from robotic_drawer.image_processor import process_image_for_robot

# Process an image and get robot movement points
points = process_image_for_robot(
    "input_image.jpg",
    output_dir="output",
    save_intermediate_steps=True
)

# The points can be used to control a robotic arm
# Each point is [x, y, z, a, e, r] for position and orientation
```

### Command Line Example

The library includes a simple command-line example:

```bash
python -m examples.simple_drawing input_image.jpg --output-dir output --scale 1.2
```

## Features

- **Background Removal**: Automatically removes background from images
- **Contour Extraction**: Detects edges and extracts contours
- **Path Optimization**: Optimizes drawing paths for efficiency
- **3D Visualization**: Visualizes the robot path in 3D
- **Pen Up/Down Control**: Intelligently controls pen movements

## Documentation

For detailed documentation of all functions and classes, refer to the docstrings in the code.

## License

This project is licensed under the MIT License - see the LICENSE file for details.