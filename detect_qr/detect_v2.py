import cv2
import time

cap = cv2.VideoCapture(0)
detector = cv2.QRCodeDetector()

previousTime = 0
currentTime = 0
last_detect_time = 0
cooldown = 2

scanned_data = []
enable = True  # Biến để kiểm soát quá trình quét

def process_scanned_data(data):
    scanned_data.append(data)
    print("Các ký tự đã được quét: ", scanned_data)

while True:
    success, img = cap.read()
    if not success:
        break

    cur_time = time.time()

    if enable or (cur_time - last_detect_time > cooldown):  # Chỉ quét khi biến enable là True
        data, bbox, _ = detector.detectAndDecode(img)
        if data:
            process_scanned_data(data)
            enable = False  # Sau khi quét xong, tắt enable để chỉ quét 1 lần
            last_detect_time = cur_time

            if bbox is not None:
                # Đảm bảo bbox là một danh sách các điểm
                bbox = bbox.astype(int)
                for i in range(len(bbox[0])):
                    cv2.line(img, tuple(bbox[0][i]), tuple(bbox[0][(i+1) % len(bbox[0])]), color=(255, 0, 0), thickness=2)
                cv2.putText(img, data, (bbox[0][0][0], bbox[0][0][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        else:
            enable = True

    # Hiển thị hình ảnh kết quả
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

import itertools
import spacy
import Levenshtein
from collections import Counter

# Tải mô hình ngôn ngữ spaCy lớn hơn
nlp = spacy.load("en_core_web_lg")

# Hàm kiểm tra tính hợp lệ của từ với spaCy
def is_valid_word(word):
    doc = nlp(word)
    return doc[0].is_alpha and (doc[0].is_oov == False or doc[0].ent_type_)

# Hàm sắp xếp các ký tự thành các từ có nghĩa và trả về từ gần đúng nhất
def find_meaningful_words(scanned_chars):
    scanned_chars = ''.join(scanned_chars).lower()  # Chuyển ký tự đã quét thành chuỗi và đổi thành chữ thường
    meaningful_words = set()

    # Chỉ tạo các tổ hợp có độ dài đúng bằng số lượng ký tự đã quét
    for combo in itertools.permutations(scanned_chars, len(scanned_chars)):
        word = ''.join(combo)
        if is_valid_word(word):
            meaningful_words.add(word)

    return list(meaningful_words)

# Hàm rút gọn các từ gần đúng dựa trên khoảng cách Levenshtein
def reduce_similar_words(words, threshold=2):
    reduced_words = []
    for word in words:
        if not any(Levenshtein.distance(word, rw) <= threshold for rw in reduced_words):
            reduced_words.append(word)
    return reduced_words

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
