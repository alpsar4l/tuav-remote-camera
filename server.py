import flask
from flask import Flask
import serial
import time
import cv2
import numpy as np
import base64
import datetime

from threading import Timer
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
app.config["DEBUG"] = True
socketio = SocketIO(app)
save_video = False
count = 0


@app.route("/")
def index():
    return flask.render_template("index.html")


@app.route("/record_video")
def video_record():
    global save_video
    global count

    def stop_record():
        global save_video
        save_video = False
        
    save_video = True

    print("Video kaydı başlatılıyor (6)")
    count = 0
    Timer(6, stop_record).start()
    print("Video kaydı bitti (6)")

    return "tamam."


@socketio.on("image")
def send_data(image):
    global save_video
    global count
    presentDate = datetime.datetime.now()
    unix_timestamp = datetime.datetime.timestamp(presentDate) * 1000

    print(save_video)

    if save_video:
        count = count + 1
        with open(f"./video/frame-{count}-{unix_timestamp}.png", "wb") as fh:
            fh.write(base64.decodebytes(image))


    socketio.emit("show image", image.decode("UTF-8").strip())


socketio.run(app, host="0.0.0.0", port=5005)
