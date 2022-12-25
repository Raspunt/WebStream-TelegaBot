import os
import time
import threading

from flask import Flask, render_template, Response, request,redirect
import cv2 as cv

from motors import MotorMood
from config import conf

mm = MotorMood()
pi_camera = None


app = Flask(__name__,static_url_path='/static')



@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



@app.route('/')
def index():
    return render_template('index.html',resolution=pi_camera.resolution) 




def gen(camera):
    # camera.start()

    while True:
        frame = camera.get_frame()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(pi_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/stopCamera',methods = ['POST'])
def stopCamera():
    pi_camera.stop()
    return "None"



@app.route('/motor_command',methods = ['POST'])
def motorCommand():
    
    motorSig = request.form.get('mc')


    if motorSig == "V":
        mm.motorV()
        time.sleep(0.3)
        mm.motorS()
    
    elif motorSig == "R":
        mm.motorR()
        time.sleep(0.1)
        mm.motorS()

    elif motorSig == "L":
        mm.motorL()
        time.sleep(0.1)
        mm.motorS()

    elif motorSig == "NAZ":
        mm.motorNAZ()
        time.sleep(0.3)
        mm.motorS()

    return "1"



def RunHttpServer():
    app.run(host=conf.server.host,port=conf.server.port, debug=False)



def SetCamera(cap):
    global pi_camera
    pi_camera = cap

def SetPort(myport):
    global port
    port = myport


def DropHttpServer():
    pass


