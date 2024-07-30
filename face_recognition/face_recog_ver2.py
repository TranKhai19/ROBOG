'''
Khi trong khung hình xuất hiện khuôn mặt thì video sẽ tạm dừng khoảng vài giây, chụp lại khung hình đó và tiến hành
nhận diện rồi lưu ảnh đã nhận diện vào thư mục chỉ định

Thư mục:
know: các gương mặt dùng để nhận diện
unknown: các khung hình có gương mặt chụp từ camera
processed: các khung hình đã nhận diện gương mặt
'''

import sys
import os
import time
from datetime import datetime

import face_recognition
import cv2
import numpy as np

known_face_encodings = []
known_face_names = []
known_dir = 'know'
unknown_dir = 'unknown'

def read_img(path):
    img = cv2.imread(path)
    (h, w) = img.shape[:2]
    width = 500
    ratio = width / float(w)
    height = int(h * ratio)
    return cv2.resize(img, (width, height))

def cvt2RGB(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB) if len(img.shape) == 3 and img.shape[2] == 3 else img

#Lấy ảnh mẫu
for file in os.listdir(known_dir):
    path = known_dir + '/' + file
    face_img = cvt2RGB(read_img(path))

    face_encodings = face_recognition.face_encodings(face_img)[0]
    known_face_encodings.append(face_encodings)

    known_face_names.append(file.split('.')[0])

#Bắt đầu video
video_capture = cv2.VideoCapture(1)

if not video_capture.isOpened():
    print("Error to connect camera!")
    sys.exit()

frame_idx = 1
process_dir = 'processed'
#So sánh và nhận diện
def compare_face(face_img):
    face_encodings = face_recognition.face_encodings(face_img)[0]

    compare = face_recognition.compare_faces(known_face_encodings, face_encodings)
    now = datetime.now()
    time_string = now.strftime("%Y%m%d%H%M%S")

    for i in range(len(compare)):
        if compare[i]:
            name = known_face_names[i]
            (top, right, bottom, left) = face_recognition.face_locations(face_img)[0]
            cv2.rectangle(face_img, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.putText(face_img, name, (left + 2, bottom + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 1)

        img_path = f'{process_dir}/face_recognition_{time_string}.jpg'
        cv2.imwrite(img_path, face_img)

#Đọc khung hình
while True:
    ret, frame = video_capture.read()

    if not ret:
        print('Error to display video!')
        sys.exit()

    rgb_frame = frame[:, :, ::-1]

    face_locations = face_recognition.face_locations(rgb_frame)
    if len(face_locations) != 0:
        time.sleep(5)
        img_path = f'{unknown_dir}/unknown_{frame_idx}.jpg'
        cv2.imwrite(img_path, frame)
        face_img = cvt2RGB(read_img(img_path))
        compare_face(face_img)
        frame_idx += 1

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()









