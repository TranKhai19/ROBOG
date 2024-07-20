
import speech_recognition as sr
import cv2

def color_recognition():
  r = sr.Recognizer()
  with sr.Microphone() as source:
    print("Hãy nói màu sắc bạn muốn tìm kiếm (đỏ, xanh lá cây, xanh dương):")
    audio = r.listen(source)

  try:
    color = r.recognize_google(audio, language="vi-VN")
    print("Bạn đã nói: " + color)

    # Mở camera
    cap = cv2.VideoCapture(0)

    while True:
      ret, frame = cap.read()

      # Chuyển đổi sang không gian màu HSV
      hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

      # Xác định ngưỡng màu
      if color == "đỏ":
        lower_color = (0, 100, 100)
        upper_color = (10, 255, 255)
      elif color == "xanh lá cây":
        lower_color = (36, 25, 25)
        upper_color = (70, 255, 255)
      elif color == "xanh dương":
        lower_color = (100, 100, 100)
        upper_color = (130, 255, 255)
      else:
        print("Màu sắc không hợp lệ!")
        break

      # Tạo mặt nạ
      mask = cv2.inRange(hsv, lower_color, upper_color)

      # Hiển thị kết quả
      cv2.imshow('Frame', frame)
      cv2.imshow('Mask', mask)

      if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    cap.release()
    cv2.destroyAllWindows()

  except sr.UnknownValueError:
    print("Không thể hiểu được âm thanh.")
  except sr.RequestError as e:
    print("Không thể yêu cầu kết quả từ dịch vụ Google Speech Recognition; {0}".format(e))

color_recognition()