import cv2
import numpy as np

cap = cv2.VideoCapture(0)

color_to_detect = 'all'

while True:
    read_ok, img = cap.read()
    img_bcp = img.copy()

    img = cv2.resize(img, (640, 480))
    input_image_cpy = img.copy()

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_red = np.array([0, 50, 50])
    upper_red = np.array([10, 255, 255])

    lower_green = np.array([40, 20, 50])
    upper_green = np.array([90, 255, 255])

    lower_blue = np.array([100, 50, 50])
    upper_blue = np.array([130, 255, 255])

    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_green, _ = cv2.findContours(mask_green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if color_to_detect == 'red' or color_to_detect == 'all':
        for cnt in contours_red:
            contour_area = cv2.contourArea(cnt)
            if contour_area > 1000:
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(img, 'Red', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    if color_to_detect == 'green' or color_to_detect == 'all':
        for cnt in contours_green:
            contour_area = cv2.contourArea(cnt)
            if contour_area > 1000:
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(img, 'Green', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    if color_to_detect == 'blue' or color_to_detect == 'all':
        for cnt in contours_blue:
            contour_area = cv2.contourArea(cnt)
            if contour_area > 1000:
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(img, 'Blue', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

    cv2.imshow("Color Detection", img)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('r'):
        color_to_detect = 'red'
    elif key == ord('g'):
        color_to_detect = 'green'
    elif key == ord('b'):
        color_to_detect = 'blue'
    elif key == ord('a'):
        color_to_detect = 'all'

cap.release()
cv2.destroyAllWindows()
