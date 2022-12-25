
import time
import os
import sys
from threading import Thread 



import RPi.GPIO as GPIO
import cv2
from imutils.video.pivideostream import PiVideoStream
from dotenv import load_dotenv

from camera import SmartCamera
from telega import Telega
import httpServer

from config import conf


load_dotenv()


class Main:



    def __init__(self):


        self.tel = Telega()
        self.tel.RunTelega()
        self.cap = SmartCamera()

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(conf.pin.DETECTOR, GPIO.IN)


        self.cap.start()
        httpServer.SetCamera(self.cap)

        conf.httpServer_working = True
        phs = Thread(target=httpServer.RunHttpServer)
        phs.start()



        while True:

            if conf.is_detector_active:      
                self.DetectMontion()


                
 


    def DetectMontion(self):


        if GPIO.input(conf.pin.DETECTOR) :
            print("движение замечено")
            img = self.cap.MobileNetStart()
            
            if img is not None:
                print("фото")
                cv2.imwrite('./Files/fr.jpg', img)
                self.tel.SendAllSub()
                print("фото готово")






try:
    Main()
except Exception as e:


    logFile = open('./Files/logs.txt','a')
    logFile.write(e)

    print(e)