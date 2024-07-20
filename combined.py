import cv2
import time
import itertools
import spacy
import Levenshtein
import numpy as np

# Initialize camera
cap = cv2.VideoCapture(0)

# Initialize QR code detector
detector = cv2.QRCodeDetector()

# Initialize spaCy model
nlp = spacy.load("en_core_web_lg")

# Initialize variables
previousTime = 0
currentTime = 0
last_detect_time = 0
cooldown = 2
scanned_data = []
enable = True  # Variable to control scanning process


# Function to process scanned data
def process_scanned_data(data):
    scanned_data.append(data)
    print("Scanned characters: ", scanned_data)


# Function to check if a word is valid using spaCy
def is_valid_word(word):
    if not word:  # Check if the word is not empty
        return False
    doc = nlp(word)
    return doc[0].is_alpha and (doc[0].is_oov == False or doc[0].ent_type_)


# Function to find meaningful words from scanned characters
def find_meaningful_words(scanned_chars):
    scanned_chars = ''.join(scanned_chars).lower()
    meaningful_words = set()
    for combo in itertools.permutations(scanned_chars, len(scanned_chars)):
        word = ''.join(combo)
        if is_valid_word(word):
            meaningful_words.add(word)
    return list(meaningful_words)


# Function to reduce similar words based on Levenshtein distance
def reduce_similar_words(words, threshold=2):
    reduced_words = []
    for word in words:
        if not any(Levenshtein.distance(word, rw) <= threshold for rw in reduced_words):
            reduced_words.append(word)
    return reduced_words


# Function to control motors based on line position
def control_motors(direction):
    if direction == "left":
        print("Turn Left")
    elif direction == "right":
        print("Turn Right")
    elif direction == "straight":
        print("Go Straight")


# Function to track line
def track_line(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, threshold = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            cv2.line(frame, (cx, 0), (cx, frame.shape[0]), (255, 0, 0), 1)
            cv2.line(frame, (0, cy), (frame.shape[1], cy), (255, 0, 0), 1)
            cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
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


# Main loop
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Track line
    frame, threshold = track_line(frame)

    # Detect QR code
    cur_time = time.time()
    if enable or (cur_time - last_detect_time > cooldown):
        data, bbox, _ = detector.detectAndDecode(frame)
        if data:
            process_scanned_data(data)
            enable = False
            last_detect_time = cur_time
            if bbox is not None:
                bbox = bbox.astype(int)
                for i in range(len(bbox[0])):
                    cv2.line(frame, tuple(bbox[0][i]), tuple(bbox[0][(i + 1) % len(bbox[0])]), color=(255, 0, 0),
                             thickness=2)
                cv2.putText(frame, data, (bbox[0][0][0], bbox[0][0][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (0, 255, 0), 2)
        else:
            enable = True

    currentTime = time.time()
    fps = 1 / (currentTime - previousTime)
    previousTime = currentTime

    cv2.putText(frame, f'{int(fps)} FPS', (10, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Frame", frame)
    cv2.imshow("Threshold", threshold)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Post-processing scanned data
all_words = find_meaningful_words(scanned_data)
reduced_words = reduce_similar_words(all_words)
lib_scanned = ["duytan", "ubtech"]
meaningful_word = ""
for word in all_words:
    if word in lib_scanned:
        meaningful_word = word

print("Correct word: ", meaningful_word)
print("Reduced similar words: ", reduced_words)
