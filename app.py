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

#initialize stopFlags
stopFlagForward = 1
stopFlagBackward = 1
stopFlagRight = 1
stopFlagLeft = 1

# App Globals (do not edit)
app = Flask(__name__)
app.config['SECRET_KEY'] = '123456789'


def gen(camera):
    # Get camera frame
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    # function to output camera
    return Response(gen(pi_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/") # Flask webserver principal page
@app.route("/stop") 
def stop():
    # send request to stop movement
    carFunction('stop')
    return render_template('index.html')

@app.route("/drive") 
def forward():
    # send request to move the car forward
    carFunction('drive')
    while True:
        if (stopFlagForward == 1):
            break
        my_car.drive()
    
@app.route("/reverse") 
def backward():
    # send request to move the car backward
    carFunction('reverse')
    while True:
        if (stopFlagBackward == 1):
            break
        my_car.reverse()

@app.route("/left") 
def left():
    # send request to move the car to the left
    carFunction('left')
    while True:
        if (stopFlagLeft == 1):
            break
        my_car.left()

@app.route("/right") 
def right():
    # send request to move the car to the right
    carFunction('right')
    while True:
        if (stopFlagRight == 1):
            break
        my_car.right()


def carFunction(function): # this function is used to stop all processed before start the new process
    global stopFlagForward, stopFlagBackward, stopFlagRight, stopFlagLeft
    stopFlagForward = 1
    stopFlagBackward = 1
    stopFlagRight = 1
    stopFlagLeft = 1
    # if (function == 'stop'): #stop
        # keep the value of flags equal to 1
    if (function == 'drive'):
        stopFlagForward = 0 
    if (function == 'reverse'):
        stopFlagBackward = 0
    if (function == 'right'):
        stopFlagRight = 0
    if (function == 'left'):
        stopFlagLeft = 0
    time.sleep(0.5)


if __name__ == '__main__':
    app.run(host="0.0.0.0")