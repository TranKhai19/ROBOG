import cv2
import time
import itertools
import spacy
import Levenshtein
import numpy as np

cap = cv2.VideoCapture(0)
detector = cv2.QRCodeDetector()
nlp = spacy.load("en_core_web_lg")

previousTime = 0
currentTime = 0
last_detect_time = 0
cooldown = 2

scanned_data = []
enable = True
qr_scanned = 0

def process_scanned_data(data):
    scanned_data.append(data)
    print("Các kí tự đã được quét: ", scanned_data)

def is_valid_word(word):
    doc = nlp(word)
    return doc[0].is_alpha and (doc[0].is_oov == False or doc[0].ent_type_)

def find_meaningful_words(scanned_chars):
    scanned_chars = ''.join(scanned_chars).lower()
    meaningful_words = set()

    for combo in itertools.permutations(scanned_chars, len(scanned_chars)):
        word = ''.join(combo)
        if is_valid_word(word):
            meaningful_words.add(word)

    return list(meaningful_words)

def reduce_similar_words(words, threshold=2):
    reduced_words = []
    for word in words:
        if not any (Levenshtein.distance(word,rw) <= threshold for rw in reduced_words):
            reduced_words.append(word)
    return reduced_words
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


while True:
    success,img = cap.read()
    if not success:
        break

    img, threshold = track_line(img)
    cur_time = time.time()

    if enable or (cur_time - last_detect_time > cooldown):
        data,bbox,_ = detector.detectAndDecode(img)
        if data:
            process_scanned_data(data)
            qr_scanned += 1
            enable = False
            last_detect_time = cur_time

            if bbox is not None:
                bbox = bbox.astype(int)
                for i in range(len(bbox[0])):
                    cv2.line(img, tuple(bbox[0][i]), tuple(bbox[0][(i + 1) % len(bbox[0])]), color=(255, 0, 0),
                             thickness=2)
                cv2.putText(img, data, (bbox[0][0][0], bbox[0][0][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (0, 255, 0), 2)
        else:
            enable = True
    currentTime = time.time()
    fps = 1 / (currentTime - previousTime)
    previousTime = currentTime

    # Hiển thị FPS lên hình ảnh
    cv2.putText(img, f'QR Codes: {qr_scanned}', (10, 100), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(img, f'{int(fps)} FPS', (10, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

    # Hiển thị hình ảnh kết quả
    cv2.imshow("img", img)
    cv2.imshow("Threshold", threshold)

    # Nhấn phím 'q' để thoát vòng lặp
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

scanned_chars = scanned_data
all_words = find_meaningful_words(scanned_chars)
reduced_words = reduce_similar_words(all_words)
lib_scanned = ["duytan", "ubtech"]
meaningful_word =""
for word in all_words:
    if word in lib_scanned:
        meaningful_word = word

print("Từ đúng: ",meaningful_word)
print("Các từ gần đúng đã rút gọn: ", reduced_words)
