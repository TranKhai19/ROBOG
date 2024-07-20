import cv2
import numpy as np
from pyzbar.pyzbar import decode
import time

cap = cv2.VideoCapture(0)
previousTime = 0
currentTime = 0

scanned_data = []
enable = True

def process_scanned_data(data):
    scanned_data.append(data)
    print("Các ký tự đã được quét: ", scanned_data)

while True:
    success, img = cap.read()
    if not success:
        break

    if enable:  # Chỉ quét khi biến enable là True
        for code in decode(img):
            decode_data = code.data.decode("utf-8")

            rect_pts = code.rect

            if decode_data:
                pts = np.array([code.polygon], np.int32)
                cv2.polylines(img, [pts], True, (255, 0, 0), 3)
                cv2.putText(img, str(decode_data), (rect_pts[0], rect_pts[1]), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 2)
                process_scanned_data(decode_data)
                enable = False  # Sau khi quét xong, tắt enable để chỉ quét 1 lần

    currentTime = time.time()
    fps = 1 / (currentTime - previousTime)
    previousTime = currentTime

    # Hiển thị FPS lên hình ảnh
    cv2.putText(img, f'{int(fps)} FPS', (10, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

    # Hiển thị hình ảnh kết quả
    cv2.imshow("img", img)

    # Nhấn phím 'q' để thoát vòng lặp
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
