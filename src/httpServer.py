import time
import socket
import json
import os


from flask import Flask, render_template, Response, request,make_response
from werkzeug.serving import make_server
import cv2 as cv

from motors import MotorMood
from config import conf

mm = MotorMood()



pi_camera = None

app = Flask(__name__,static_url_path='/static')
server = make_server(conf.server.host, conf.server.port, app)

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
    while True:
        frame = None
        
        if conf.objectDetectorFrame:
            frame = camera.MobileNetStart()
            if frame is not None:    
                ret, jpeg = cv.imencode(camera.file_type, frame)
                frame = jpeg.tobytes()
            else:
                frame = camera.get_frame_byte()
                
  
        
        elif conf.QrReaderFrame:
            frame = camera.check_barcodes()
            ret, jpeg = cv.imencode(camera.file_type, frame)
            frame = jpeg.tobytes()
        
        else :
            frame = camera.get_frame_byte()

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


@app.route('/login')
def login():
    return render_template('login.html') 


@app.route('/CheckPassword',methods = ['POST'])
def CheckPassword():
    
    username_client = request.form.get('username')
    password_client = request.form.get('password')
    
    file = open(f"{conf.pathToProject}/Files/localStorage.json")
    data = json.load(file)
    
    httpPassword = data["httpPassword"]
    httpUsername = data["httpUsername"]
    
    if username_client == httpUsername and password_client == conf.getUserHttpPassword():
        res = make_response("1")
        res.set_cookie('password', httpPassword, max_age=60*60*24*365*2)
        return res
        
    else :
        return Response("0", status=200, mimetype='application/json')

@app.route('/CheckEncryptPassword',methods = ['POST'])
def CheckEncryptPassword():
    
    password = request.form.get("password")
        
    file = open(f"{conf.pathToProject}/Files/localStorage.json")
    data = json.load(file)
    
    clientPassword = data["httpPassword"]
    
    if conf.disable_web_authentication:
        return Response("1", status=200, mimetype='application/json')
    
    if password == clientPassword:
        return Response("1", status=200, mimetype='application/json')
    else : 
        return Response("0", status=401, mimetype='application/json')

     
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
    
    server.serve_forever()

    
    

@app.route('/EnableAnalizator',methods = ['POST'])
def EnableAnalizator():

    
    if conf.faceRecognationFrame != True:
        
        if conf.objectDetectorFrame != True:
            conf.objectDetectorFrame = True
        else :
            conf.objectDetectorFrame = False
    
    else:
        print("одновремено вкючать нельзя выключите сначало face Detector")
        
        
    
    return Response("{'a':'b'}", status=200, mimetype='application/json') 


@app.route('/EnableFaceRecognation',methods = ['POST'])
def EnableFaceRecognation():
    
    
    if conf.objectDetectorFrame != True:
    
        if conf.faceRecognationFrame != True:
            conf.faceRecognationFrame = True
        else :
            conf.faceRecognationFrame = False
    
    else:        
        print("одновремено вкючать нельзя выключите сначало object Detector")
        
        
    return Response("{'a':'b'}", status=200, mimetype='application/json') 

    
    


def set_camera(cap):
    global pi_camera
    pi_camera = cap

def SetPort(myport):
    global port
    port = myport





def GetLocalIp():

    dns =  os.popen('cat /etc/resolv.conf').read().split("\n")[1]
    dns = dns.split(" ")[1]

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((dns, 80))
    local_ip = s.getsockname()[0]
    s.close()

    return local_ip
