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

class SmartCamera():

    cameraWorking = False
    resolution = (320,240)

    
    def start(self,file_type  = ".jpg", photo_string= "stream_photo"):
        
        if self.cameraWorking == False:
            print("camera is ready")
            self.vs = PiVideoStream(framerate=10,resolution=self.resolution).start()
            
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




    def get_frame(self):

        frame = self.vs.read()
        ret, jpeg = cv2.imencode(self.file_type, frame)

        return jpeg.tobytes()
    

    def initMobileNet(self):     
        
        self.classes: list = self.readClasses()
        self.categories: list = self.ClassToCategory(self.classes) 
        
        self.net = cv2.dnn.readNetFromCaffe('./Models/MobileNetSSD.txt',
                                            './Models/MobileNetSSD.caffemodel')
           


    def MobileNetStart(self):

        self.initMobileNet()

        img = self.vs.read()

        h, w = img.shape[0], img.shape[1]

        sizeImg = (300, 300)

        img_reseze = cv2.resize(img, sizeImg)
        blob = cv2.dnn.blobFromImage(img_reseze, 0.007843, sizeImg, 127.5)
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

                if 'person' in self.classes[idx] or 'cat' in self.classes[idx] or 'dog' in self.classes[idx] or 'car' in self.classes[idx]:

                    cv2.rectangle(img, (startX, startY),
                                (endX, endY), colors[idx], 4)

                    y = startY - 15 if startY - 15>15 else startY + 15  
                    cv2.putText(img, label, (startX, y),cv2.FONT_HERSHEY_SIMPLEX, 0.5, colors[idx], 2)
                    
                    return img

    def readClasses(self):
        return open('./Files/classItems.txt', 'r').readlines()

    def ClassToCategory(self, classes: list):

        category = []

        for i, _class in enumerate(classes):    

            _class = _class.replace("\n",'')
            category.append({i:_class})

        return category


  

