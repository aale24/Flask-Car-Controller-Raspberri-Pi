from flask import Flask, render_template, request
from camera import VideoCamera
import time
import threading
import os

pi_camera = VideoCamera(flip=False) # flip pi camera if upside down.

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
    return render_template('stop.html')

@app.route("/forward")
def forward():
    print ('forward')
    return render_template('forward.html')
    
@app.route("/backward")
def backward():
    print ('backward')
    return render_template('backward.html')

@app.route("/left")
def left():
    print ('left')
    return render_template('left.html')

@app.route("/right")
def right():
    print ('right')
    return render_template('right.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0")

