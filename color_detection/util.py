import numpy as np
import cv2

def get_limits(color):
    c = np.uint8([[color]])
    hsvC = cv2.cvtColor(c, cv2.COLOR_RGB2HSV)
    hue = hsvC[0][0][0]
    if hue >= 165:
        lowerlimit = np.array([hue - 10, 100, 100], dtype=np.uint8)
        upperlimit = np.array([100,255,255],dtype=np.uint8)
    elif hue <= 15:
        lowerlimit = np.array([0, 100, 100], dtype=np.uint8)
        upperlimit = np.array([hue + 10, 255, 255], dtype=np.uint8)
    else:
        lowerlimit = np.array([hue - 10, 100, 100], dtype=np.uint8)
        upperlimit = np.array([hue + 10, 255, 255], dtype=np.uint8)

    return lowerlimit,upperlimit

