import speech_recognition as sr

recognizer = sr.Recognizer()

# Liệt kê các thiết bị microphone
print(sr.Microphone.list_microphone_names())

with sr.Microphone() as source:
    print("Điều chỉnh nhiễu")
    recognizer.adjust_for_ambient_noise(source, duration=1)
    print("Đang ghi âm trong 4 giây")
    recorded_audio = recognizer.listen(source, timeout=4)
    print("Hoàn thành ghi âm")

try:
    print("Đang nhận dạng văn bản")
    text = recognizer.recognize_google(
        recorded_audio,
        language="vi-VN"
    )

    print("Văn bản được giải mã: {}".format(text))

except Exception as ex:
    print(ex)
