import cv2

cap = cv2.VideoCapture(0)

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
center_frame = frame_width // 2

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Chuyển đổi khung hình sang màu xám
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Áp dụng Gaussian Blur để giảm nhiễu
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Sử dụng ngưỡng để phát hiện đường màu đen
    _, threshold = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY_INV)

    # Tìm các đường viền (contours)
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        max_contour = max(contours, key=cv2.contourArea)

        cv2.drawContours(frame, [max_contour], -1, (0, 255, 0), 3)

        M = cv2.moments(max_contour)
        if M['m00'] != 0:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])

            cv2.circle(frame, (cx, cy), 5, (255, 0, 0), -1)

            deviation = cx - center_frame
            direction = "Center"
            if deviation < 0:
                direction = "Left"
            elif deviation > 0:
                direction = "Right"

            cv2.putText(frame, f'Center: ({cx}, {cy})', (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(frame, f'Deviation: {deviation} ({direction})', (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            print(f"Center: ({cx}, {cy})")
            print(f"Deviation: {deviation} ({direction})")
        else:
            cx, cy = 0, 0

    cv2.imshow('Line Follower', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
