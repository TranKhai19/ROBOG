import time
import cv2
import numpy as np
from pyzbar.pyzbar import decode
from robomaster import robot


def main():
    # Initialize the robot
    ep_robot = robot.Robot()

    try:
        print("Initializing robot...")
        ep_robot.initialize(conn_type="sta")
        print("Robot initialized successfully!")
    except Exception as e:
        print(f"Failed to initialize robot: {e}")
        return

    # Start the video stream
    ep_camera = ep_robot.camera

    try:
        print("Starting video stream...")
        ep_camera.start_video_stream(display=False)
        print("Video stream started successfully!")
    except Exception as e:
        print(f"Failed to start video stream: {e}")
        ep_robot.close()
        return

    previousTime = time.time()

    def process_frame(frame):
        global previousTime

        # Decode QR codes in the frame
        for code in decode(frame):
            decode_data = code.data.decode("utf-8")
            rect_pts = code.rect

            if decode_data:
                pts = np.array([code.polygon], np.int32)
                cv2.polylines(frame, [pts], True, (255, 0, 0), 3)
                cv2.putText(frame, str(decode_data), (rect_pts[0], rect_pts[1]), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                            (0, 255, 0), 2)
            print(decode_data)

        currentTime = time.time()
        fps = 1 / (currentTime - previousTime)
        previousTime = currentTime

        # Displaying FPS on the image
        cv2.putText(frame, f'{int(fps)} FPS', (10, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

        # Display the resulting frame
        cv2.imshow("Frame", frame)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return False
        return True

    try:
        while True:
            frame = ep_camera.read_cv2_image(strategy="newest", timeout=3.0)
            if frame is not None:
                if not process_frame(frame):
                    break
    finally:
        ep_camera.stop_video_stream()
        ep_robot.close()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
