import time
import socketio
import cv2
import base64
import datetime


camera_way = 0
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
camera = cv2.VideoCapture(camera_way)
sio = socketio.Client()


@sio.event
def connect():
    global camera
    camera = cv2.VideoCapture(camera_way)
    print("bağlantı kuruldu")


@sio.event
def disconnect():
    print("bağlantı uçtu")
    camera.release()


def connect_server():
    # sio.connect('http://89.19.24.170:5005')
    sio.connect("http://127.0.0.1:5005")


connect_server()

while True:
    success, frame = camera.read()

    if success:
        height = frame.shape[0]
        width = frame.shape[1]

        scale_factor = 0.5
        new_height = int(height * scale_factor)
        new_width = int(width * scale_factor)

        frame = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_AREA)
        frame = cv2.flip(frame, 1, 0)

        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        for (x, y, w, h) in faces:
           cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        """

        result, frame = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 20])
        data = base64.b64encode(frame)
        sio.emit("image", data)
        print(datetime.datetime.now())