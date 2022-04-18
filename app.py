from flask import Flask, render_template, request, Response
import sys
sys.path.append('app')
from camera import VideoCamera
import time
import threading
import os
import carActuation

my_car = carActuation.ControlCar()

pi_camera = VideoCamera(flip=False) # flip pi camera if upside down.

#initialize flags
stopFlagForward = 1
stopFlagBackward = 1
stopFlagRight = 1
stopFlagLeft = 1

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
    stopFunction('stop')
    time.sleep(1)
    print('Stop')
    return render_template('stop.html')

@app.route("/forward")
def forward():
    print ('forward')
    carFunction('drive')
    time.sleep(1)
    while True:
        if (stopFlagForward == 1):
            break
        print('Drive')
        # my_car.drive()
    return render_template('forward.html')
    
@app.route("/backward")
def backward():
    print ('backward')
    carFunction('back')
    time.sleep(1)
    while True:
        if (stopFlagBackward == 1):
            break
        print('Reverse')
        # my_car.reverse()
    return render_template('backward.html')

@app.route("/left")
def left():
    print ('left')
    carFunction('left')
    time.sleep(1)
    while True:
        if (stopFlagLeft == 1):
            break
        print('Left')
        # my_car.left()
    return render_template('left.html')

@app.route("/right")
def right():
    print ('right')
    carFunction('right')
    time.sleep(1)
    while True:
        if (stopFlagRight == 1):
            break
        print('Right')
        # my_car.right()
    return render_template('right.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0")



def carFunction(function):
    global stopFlagForward, stopFlagBackward, stopFlagRight, stopFlagLeft
    if (function == 'stop'): #stop
        stopFlagLeft = 1
        stopFlagForward = 1
        stopFlagBackward = 1
        stopFlagRight = 1
    if (function == 'drive'): # drive
        stopFlagLeft = 1
        stopFlagForward = 0
        stopFlagBackward = 1
        stopFlagRight = 1
    if (function == 'back'): #back
        stopFlagLeft = 1
        stopFlagForward = 1
        stopFlagBackward = 0
        stopFlagRight = 1
    if (function == 'right'): #right
        stopFlagLeft = 1
        stopFlagForward = 1
        stopFlagBackward = 1
        stopFlagRight = 0
    if (function == 'left'): #left
        stopFlagLeft = 0
        stopFlagForward = 1
        stopFlagBackward = 1
        stopFlagRight = 1