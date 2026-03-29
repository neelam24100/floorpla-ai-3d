import cv2
import numpy as np

image = cv2.imread("test.png")

if image is None:
    print("Error loading image")
else:
    print("Image loaded successfully")