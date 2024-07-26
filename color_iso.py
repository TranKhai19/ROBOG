# import matplotlib.pyplot as plt
# from skimage.io import imshow, imread
# from skimage.color import rgb2hsv, hsv2rgb

import numpy as np
import cv2
from PIL import Image

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print('Webcam is not connected!')
    exit()

while True:
    ret, frame = cap.read()

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(frame_rgb)

    pixels = image.load()

    w, h = image.size
    for x in range(w):
        for y in range(h):
            r, g, b = pixels[x, y]
            if r > 30 or g > 30 or b > 30:
                pixels[x, y] = (255, 255, 255)
    modified_frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    cv2.imshow('Modified Frame', modified_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyWindow()





