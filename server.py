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


@app.route("/")
def index():
    return flask.render_template("index.html")


@app.route("/record_video")
def video_record():
    global save_video
    save_video = True
    print("Video kaydı başlatılıyor (6)")
    # time.sleep(6)

    def stop():
        global save_video
        save_video = False

    Timer(6, stop).start()

    print("Video kaydı bitti (6)")
    return "tamam."


@socketio.on("image")
def send_data(image):
    global save_video
    presentDate = datetime.datetime.now()
    unix_timestamp = datetime.datetime.timestamp(presentDate) * 1000

    print(save_video)

    if save_video:
        with open(f"./video/frame-{unix_timestamp}.png", "wb") as fh:
            fh.write(base64.decodebytes(image))

    socketio.emit("show image", image.decode("UTF-8").strip())


socketio.run(app, host="0.0.0.0", port=5005)
