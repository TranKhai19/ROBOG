import numpy as np
import subprocess as sp
import time
import sys
import cv2
import atexit

# Khởi tạo webcam
cap = cv2.VideoCapture(0)

# Kiểm tra xem webcam có mở được không
if not cap.isOpened():
    print("Không thể mở webcam")
    exit()

# Đặt độ phân giải và tốc độ khung hình
w, h = 640, 240
bytesPerFrame = w * h
fps = 40
cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
cap.set(cv2.CAP_PROP_FPS, fps)

# Hàm dọn dẹp để giải phóng webcam khi kết thúc chương trình
def cleanup():
    cap.release()
    cv2.destroyAllWindows()

atexit.register(cleanup)

lateral_search = 20 # number of pixels to search the line border
start_height = h - 5 # Scan index row 235

no_points_count = 0

start_time = time.perf_counter()

# Đọc và hiển thị khung hình
while True:
    ret, frame = cap.read()
    if not ret:
        print("Không thể đọc khung hình từ webcam")
        break

    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    thresh = cv2.adaptiveThreshold(frame_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    signed_thresh = thresh[start_height].astype(np.int16) # select only one row
    diff = np.diff(signed_thresh)   #The derivative of the start_height line

    points = np.where(np.logical_or(diff > 200, diff < -200))[0] #maximums and minimums of derivative
    cv2.line(frame, (0, start_height), (640, start_height), (0, 255, 0), 1) # draw horizontal line where scanning

    if len(points) > 1: # if finds something like a black line
        middle = (points[0] + points[1]) / 2

        cv2.circle(frame, (points[0], start_height), 2, (255, 0, 0), -1)
        cv2.circle(frame, (points[1], start_height), 2, (255, 0, 0), -1)
        cv2.circle(frame, (int(middle), start_height), 2, (0, 0, 255), -1)

        print(int((middle - 320) / int(sys.argv[1])))
    else:
        start_height -= 5
        start_height = start_height % h
        no_points_count += 1

    current_time = time.perf_counter()
    print("Loop took:", str((current_time - start_time) * 1000), 'ms')
    start_time = current_time

    if no_points_count > 50:
        print("Line lost")
        break

    # Hiển thị khung hình
    cv2.imshow('Webcam', frame)

    # Nhấn 'q' để thoát
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Giải phóng webcam và đóng cửa sổ
cleanup()
