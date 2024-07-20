import speech_recognition as sr
import os
from datetime import datetime
import pyaudio


def list_microphones():
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    num_devices = info.get('deviceCount')

    for i in range(num_devices):
        device_info = p.get_device_info_by_host_api_device_index(0, i)
        if device_info.get('maxInputChannels') > 0:
            print(f"ID {i}: {device_info.get('name')}")
    p.terminate()


def get_microphone_index():
    list_microphones()
    while True:
        try:
            index = int(input("Nhap ID cua Microphone: "))
            return index
        except ValueError:
            print("Vui lòng chon ID hop le.")


mic_index = get_microphone_index()

r = sr.Recognizer()

sentences = []

print("Bat dau nghe. Noi 'stop' de dung va luu.")

while True:
    with sr.Microphone(device_index=mic_index) as source:
        print("Dang lang nghe...")
        # r.adjust_for_ambient_noise(source)  # Điều chỉnh cho tiếng ồn xung quanh
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio, language="en-US")
        print("Ban da noi:", text)
        sentences.append(text)

        if "stop" in text.lower():
            break
    except sr.UnknownValueError:
        print("Khong the nhan dien giong noi")
    except sr.RequestError as e:
        print("Loi khi yeu cau ket qua; {0}".format(e))

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"D:/AnhTuan/CODE/SpeechReco/save_text/en-US/speech_recognition_{timestamp}.txt"

with open(filename, "w", encoding="utf-8") as f:
    for sentence in sentences:
        f.write(sentence + "\n")

print(f"Da luu vao file {filename}")
print(f"Da luu file tai duong dan: {os.path.abspath(filename)}")