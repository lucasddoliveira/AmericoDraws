from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="AmericoDraws",
    version="0.1.5",
    author="Lucas Dantas",
    author_email="lucasddoliveira1@gmail.com",
    description="Convert images into 3D drawing paths suitable for robotic arms.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lucasddoliveira/AmericoDraws",
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
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # or whatever you use
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Image Recognition",
    ],
)
