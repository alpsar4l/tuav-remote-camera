import os

import flask
from flask import Flask
import serial
import time
import cv2
import numpy as np
import base64
import datetime

from engineio.payload import Payload
from threading import Timer
from flask_socketio import SocketIO, emit


Payload.max_decode_packets = 1000
app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
app.config["DEBUG"] = True
socketio = SocketIO(app, ping_timeout=100000, ping_interval=5000)
save_video = False
count = 0
new_folder_name = "hey"


@app.route("/")
def index():
    return flask.render_template("index.html")


@app.route("/record_video")
def video_record():
    global save_video
    global new_folder_name
    global count

    def stop_record():
        global save_video
        save_video = False
        
    save_video = True
    new_folder_name = datetime.datetime.now()
    os.makedirs(f"video/{new_folder_name}/")

    print("Video kaydı başlatılıyor (6 saniye)")
    count = 0
    Timer(6, stop_record).start()
    print("Video kaydı bitti (6 saniye)")

    return "tamam."


@socketio.on("image")
def send_data(image):
    global save_video
    global count
    presentDate = datetime.datetime.now()
    unix_timestamp = datetime.datetime.timestamp(presentDate) * 1000

    if save_video:
        count = count + 1
        with open(f"./video/{new_folder_name}/frame-{count}-{unix_timestamp}.png", "wb") as fh:
            fh.write(base64.decodebytes(image))

    socketio.emit("show image", image.decode("UTF-8").strip())


socketio.run(app, host="0.0.0.0", port=5005)
