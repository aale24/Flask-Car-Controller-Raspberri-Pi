from flask import Flask, render_template, request,Response
from app.camera import VideoCamera
import time
import threading
import os
import app.carActuation

my_car = app.carActuation.ControlCar()

pi_camera = VideoCamera(flip=False) # flip pi camera if upside down.

stopFlagFarward = 0
stopFlagBackward = 0
stopFlagRight = 0
stopFlagLeft = 0

# App Globals (do not edit)
app = Flask(__name__)
app.config['SECRET_KEY'] = 'sdfhsdj sdf23'


def gen(camera):
    #get camera frame
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(pi_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/")
@app.route("/stop")
def stop():
    print ('stop')
    stopFlagFarward = 1
    stopFlagBackward = 1
    stopFlagRight = 1
    stopFlagLeft = 1
    return render_template('stop.html')

@app.route("/forward")
def forward():
    print ('forward')
    stopFlagFarward = 0
    stopFlagBackward = 1
    stopFlagRight = 1
    stopFlagLeft = 1
    while True:
        if (stopFlagFarward == 1):
            stopFlagFarward = 0
            break
        my_car.drive()
    return render_template('forward.html')
    
@app.route("/backward")
def backward():
    print ('backward')
    stopFlagBackward = 0
    stopFlagFarward = 1
    stopFlagRight = 1
    stopFlagLeft = 1
    while True:
        if (stopFlagBackward == 1):
            stopFlagBackward = 0
            break
        my_car.reverse()
    return render_template('backward.html')

@app.route("/left")
def left():
    print ('left')
    stopFlagLeft = 0
    stopFlagFarward = 1
    stopFlagBackward = 1
    stopFlagRight = 1
    while True:
        if (stopFlagLeft == 1):
            stopFlagLeft = 0
            break
        my_car.left()
    return render_template('left.html')

@app.route("/right")
def right():
    print ('right')
    stopFlagRight = 0
    stopFlagFarward = 1
    stopFlagBackward = 1
    stopFlagLeft = 1
    while True:
        if (stopFlagRight == 1):
            stopFlagRight = 0
            break
        my_car.right()
    return render_template('right.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0")

