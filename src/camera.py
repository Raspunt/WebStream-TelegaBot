import threading
from datetime import datetime
import time
import os

import cv2 
from imutils.video import VideoStream,FPS
from imutils.video.pivideostream import PiVideoStream
import imutils
import numpy as np
import glob
from pyzbar import pyzbar

from motors import MotorMood
from config import conf


class SmartCamera():

    cameraWorking = False
    resolution = (320,240)

    target = (0,0)
    telega = None
    
    
    def start(self,file_type  = ".jpg", photo_string= "stream_photo"):
        
        if self.cameraWorking == False:
            print("camera is ready")
            self.vs = VideoStream(framerate=10,resolution=self.resolution).start()
            
            self.file_type = file_type
            self.photo_string = photo_string
            time.sleep(2.0)
            self.cameraWorking = True
     
        else:
            print('camera already working !!!')
            
        
    
    def stop(self):
        self.vs.stop()
        print("camera stop")
        self.cameraWorking = False 




    def get_frame_byte(self):

        frame = self.vs.read()
        ret, jpeg = cv2.imencode(self.file_type, frame)

        return jpeg.tobytes()
    
    def get_frame(self):
        return self.vs.read()
        
    

    def initMobileNet(self):     
        
        self.classes: list = self.readClasses()
        self.categories: list = self.ClassToCategory(self.classes) 
        
        self.net = cv2.dnn.readNetFromCaffe(f'{conf.pathToProject}/Models/MobileNetSSD.txt',
                                            f'{conf.pathToProject}/Models/MobileNetSSD.caffemodel')
           


    def MobileNetStart(self):
        # self.initMobileNet()
        img = self.vs.read()

        h, w = img.shape[0], img.shape[1]
        sizeImg = (300, 300)
        
        # print("обработка...")
        
        
        frame_resized = cv2.resize(img,(300,300))
        blob = cv2.dnn.blobFromImage(frame_resized, 0.007843, (300, 300), (127.5, 127.5, 127.5), False)
        self.net.setInput(blob)

        detections = self.net.forward()
        colors = np.random.uniform(255, 0, size=(len(self.categories), 3))

        
        for i in np.arange(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.2:
                idx = int(detections[0, 0, i, 1])
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype('int')
                label = f"{self.classes[idx]} {int(confidence * 100)}%"
                
                # if 'person' in self.classes[idx]:
                cv2.rectangle(frame_resized, (startX, startY),
                            (endX, endY), colors[idx], 4)

                y = startY - 15 if startY - 15>15 else startY + 15  
                cv2.putText(frame_resized, label, (startX, y),cv2.FONT_HERSHEY_SIMPLEX, 0.5, colors[idx], 2)
                
                if self.classes[idx] is None:
                    self.classes[idx] = "0_0"
                
                    
                
                return (self.classes[idx],frame_resized)

                
    
        

    def readClasses(self):
        return open(f'{conf.pathToProject}/Files/classItems.txt', 'r').readlines()

    def ClassToCategory(self, classes: list):

        category = []

        for i, _class in enumerate(classes):    

            _class = _class.replace("\n",'')
            category.append({i:_class})

        return category


        
    def check_barcodes(self):
        
        frame = self.vs.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        barcodes = pyzbar.decode(gray)

        
        # print('barry code')

        for barcode in barcodes:
            detected_qr_password = barcode.data.decode('utf-8')
            qr_password =  conf.localStorage['qrPassword']
            
            
            bbox = barcode.rect
            
            cv2.rectangle(frame, (bbox.left, bbox.top), (bbox.left + bbox.width, bbox.top + bbox.height), (0, 255, 0), 2)

            
            
            if detected_qr_password == qr_password:
                self.telega.send_message_for_all_subscribers("правильный пароль qrcode")
            else:
                self.telega.send_message_for_all_subscribers("неправильный пароль qrcode")
                
        return frame

    


