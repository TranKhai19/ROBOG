import numpy as np
import matplotlib.pyplot as plt
from skimage.io import imshow, imread
from skimage.color import rgb2hsv, hsv2rgb
import cv2
from PIL import Image

with Image.open('R.jpg') as img:
    img = img.convert("RGB")
    pixels = img.load()

    w, h = img.size
    for x in range(w):
        for y in range(h):
            r,g,b = pixels[x, y]
            if r > 30 or g > 30 or b > 30:
                pixels[x, y] = (255,255,255)

    img.show()






