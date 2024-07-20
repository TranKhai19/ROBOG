import cv2
import numpy as np


# Đường Line Follow
def follow_line(image):
    # Chuyển đổi ảnh sang độ sáng xám
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Ứng dụng Canny để phát hiện cạnh
    edges = cv2.Canny(gray, 50, 150)

    # Tìm đường thẳng bằng Hough Transform
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=50, maxLineGap=10)

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

    return image


if __name__ == '__main__':
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        if ret:
            line_followed_image = follow_line(frame)

            cv2.imshow('Line Followed', line_followed_image)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()