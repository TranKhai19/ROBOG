from robomaster import robot, camera
import time
ep_robot = robot.Robot()
ep_robot .initialize(conn_type="sta")

ep_cam = ep_robot.camera
ep_cam.start_video_stream(display=False)

def scan_and_process_qr():
    while True:
        img = ep_cam.read_cv2_image(strategy="newest", timeout=2)
        qr_code = ep_cam.read_qr_code(img)
        if qr_code:
            print("QR Code Detected: ", qr_code)
            process_qr_code(qr_code)
            break

def process_qr_code(qr_code):
    commands = qr_code.split(",")
    for command  in commands:
        if command.startswitch("move"):
            _, distance = command.split(":")
            move_forward(float(distance))
        elif command.startswitch("rotate"):
            _,angle = command.split(":")
            rotate_gimbal(float(angle))

def move_forward(distance):
    print(f"Moving forward {distance} meters...")
    time.sleep(distance/0.1)

def rotate_gimbal(angle):
    print(f"Rotating gimbal {angle} degress...")
    ep_robot.gimbal.rotate(yaw_angle=angle)

scan_and_process_qr()
ep_robot.close()