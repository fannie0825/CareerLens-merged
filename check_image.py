import os
from PIL import Image

try:
    img = Image.open("CareerLens_Logo.png")
    print(f"Successfully opened image. Format: {img.format}, Size: {img.size}, Mode: {img.mode}")
except Exception as e:
    print(f"Failed to open image: {e}")
