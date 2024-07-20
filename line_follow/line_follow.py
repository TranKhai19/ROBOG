import cv2
import numpy as np


# Hàm để điều khiển động cơ dựa trên vị trí đường kẻ
def control_motors(direction):
    if direction == "left":
        print("Turn Left")
        # Điều khiển động cơ để quay trái
    elif direction == "right":
        print("Turn Right")
        # Điều khiển động cơ để quay phải
    elif direction == "straight":
        print("Go Straight")
        # Điều khiển động cơ để đi thẳng


# Hàm để phát hiện và theo dõi đường kẻ
def track_line(frame):
    # Chuyển đổi hình ảnh sang thang độ xám
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Áp dụng GaussianBlur để giảm nhiễu
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Áp dụng ngưỡng để phân đoạn đường kẻ
    _, threshold = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY_INV)

    # Tìm các đường viền trong hình ảnh
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Lấy đường viền lớn nhất
        c = max(contours, key=cv2.contourArea)

        # Tính toán khoảnh khắc để tìm tâm của đường kẻ
        M = cv2.moments(c)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            # Vẽ đường kẻ và tâm điểm lên khung hình
            cv2.line(frame, (cx, 0), (cx, frame.shape[0]), (255, 0, 0), 1)
            cv2.line(frame, (0, cy), (frame.shape[1], cy), (255, 0, 0), 1)
            cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)

            # Xác định hướng di chuyển của robot
            frame_center = frame.shape[1] // 2
            if cx < frame_center - 10:
                control_motors("left")
            elif cx > frame_center + 10:
                control_motors("right")
            else:
                control_motors("straight")
        else:
            control_motors("straight")
    else:
        control_motors("straight")

    return frame, threshold


# Khởi tạo camera
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Gọi hàm theo dõi đường kẻ
    frame, threshold = track_line(frame)

    # Hiển thị khung hình
    cv2.imshow("Frame", frame)
    cv2.imshow("Threshold", threshold)

    # Nhấn 'q' để thoát
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
