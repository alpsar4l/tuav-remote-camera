import time
import socketio
import cv2
import base64


camera = cv2.VideoCapture(0)
sio = socketio.Client()


@sio.event
def connect():
    print("bağlantı kuruldu")


@sio.event
def disconnect():
    print("bağlantı uçtu")
    # camera.release()


def connect_server():
    # sio.connect('http://89.19.24.170:5005')
    sio.connect("http://127.0.0.1:5005")


connect_server()

while True:
    success, frame = camera.read()

    if success:
        # frame = cv2.resize(frame, (640, 350), interpolation=cv2.INTER_AREA)
        frame = cv2.flip(frame, 1, 0)
        result, frame = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 20])
        data = base64.b64encode(frame)
        sio.emit("image", data)
        print("kamera okunuyor")