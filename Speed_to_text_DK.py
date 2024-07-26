import cv2
import numpy as np
import speech_recognition as sr

# Tạo đối tượng recognizer cho nhận dạng giọng nói
recognizer = sr.Recognizer()

# Hàm callback để lấy màu sắc tại vị trí nhấp chuột
def call_back_function(event, x, y, flags, param):
    global b, g, r, clicked
    if event == cv2.EVENT_LBUTTONDBLCLK:
        clicked = True
        b, g, r = frame[y, x]
        b = int(b)
        g = int(g)
        r = int(r)

# Hàm tìm tên màu sắc
def get_Color_Name(R, G, B):
    color = "Unknown"
    if R > 100 and G < 60 and B < 60:
        color = "Red"
    elif R < 60 and G > 100 and B < 60:
        color = "Green"
    elif R < 60 and G < 60 and B > 100:
        color = "Blue"
    return color

# Hàm nhận dạng giọng nói
def recognize_speech():
    with sr.Microphone() as source:
        print("Điều chỉnh nhiễu")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Đang ghi âm, xin hãy nói tên màu sắc (đỏ, xanh lá, xanh dương, tất cả)")
        audio = recognizer.listen(source, timeout=10)
        print("Hoàn thành ghi âm")
    try:
        print("Đang nhận dạng văn bản")
        text = recognizer.recognize_google(audio, language="vi-VN")
        print("Văn bản được giải mã: {}".format(text))
        return text.lower()
    except Exception as ex:
        print(ex)
        return None

# Khởi động camera
cap = cv2.VideoCapture(0)
cv2.namedWindow("Color Detection Window")
cv2.setMouseCallback("Color Detection Window", call_back_function)

color_to_detect = 'all'

def detect_color(color):
    global color_to_detect
    color_to_detect = color

while True:
    ret, frame = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Định nghĩa màu cần phát hiện
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
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(frame, 'Red', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
    if color_to_detect == 'green' or color_to_detect == 'all':
        for cnt in contours_green:
            contour_area = cv2.contourArea(cnt)
            if contour_area > 1000:
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, 'Green', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    if color_to_detect == 'blue' or color_to_detect == 'all':
        for cnt in contours_blue:
            contour_area = cv2.contourArea(cnt)
            if contour_area > 1000:
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(frame, 'Blue', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

    # Nhận diện giọng nói
    command = recognize_speech()
    if command:
        if "đỏ" in command:
            detect_color('red')
        elif "xanh lá" in command or "xanh lục" in command:
            detect_color('green')
        elif "xanh dương" in command or "xanh nước biển" in command:
            detect_color('blue')
        elif "tất cả" in command:
            detect_color('all')
        else:
            print("Không nhận dạng được màu sắc, xin thử lại")
            continue

    cv2.imshow("Color Detection Window", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
