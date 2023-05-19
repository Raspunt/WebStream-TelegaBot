import os
import time

import cv2
from PIL import Image 
from imutils.video import VideoStream

from .recognize_config import Config

config = Config()

class Detector:
    
    def __init__(self) -> None:
        self.camera_working = False
        self.names = []
        
        self.face_cascade = cv2.CascadeClassifier(config.rec_path['haarcascade_frontalface_path'])
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read(config.rec_path['trainner_file'])

    

    def set_camera(self,vs):
        self.vs = vs
    
    def enable_camera(self):
        
        if self.camera_working == False:
            self.vs = VideoStream(framerate=10,resolution=(300,300)).start()
            self.camera_working = True
        else :
            print('camera is already open')
        


    def start_regognition_all(self,labels:list):
            
        
        frame = self.vs.get_frame()
        
        #default_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray,1.3,5)

        text = ""
        newImg = None
        
        for (x,y,w,h) in faces:


            roi_gray = gray[y:y+h,x:x+w]

            id,confidence = self.recognizer.predict(roi_gray)
            confidence = 100 - int(confidence)
            
            if confidence > 50:
                text = labels[id]
                font = cv2.FONT_HERSHEY_PLAIN
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                frame = cv2.putText(frame, text, (x, y-4), font, 1, (0, 255, 0), 1, cv2.LINE_AA)
                
            else:   
                text = "UnknownFace"
                font = cv2.FONT_HERSHEY_PLAIN
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                frame = cv2.putText(frame, text, (x, y-4), font, 1, (0, 0,255), 1, cv2.LINE_AA)

            # cv2.imshow("image", frame)
            newImg = frame
            
        return (newImg,text)
    
    
                
              



              


            