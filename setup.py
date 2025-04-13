from setuptools import setup, find_packages

setup(
    name="AmericoDraws",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.19.0",
        "matplotlib>=3.3.0",
        "opencv-python>=4.5.0",
        "Pillow>=8.0.0",
        "scikit-learn>=0.24.0",
        "networkx>=2.5.0",
        "rembg>=2.0.0",
    ],
    python_requires=">=3.7",
)