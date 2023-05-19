import datetime
import threading 

import RPi.GPIO as GPIO
import cv2
from imutils.video.pivideostream import PiVideoStream
from dotenv import load_dotenv
load_dotenv()

from sensors import *
from display import Display_7219
from camera import SmartCamera
from recognize_face.RecCamera import Detector
from recognize_face.trainer import Trainer

from telega import Telega
import httpServer

from config import conf


class Main:

    def __init__(self):
        self.tel = Telega()
        self.tel.RunTelega()
        self.cap = SmartCamera()
        
        self.detector = Detector()
        self.trainner = Trainer()
        

        self.labels = self.trainner.train_classifer_all()
        
        sensors_init()
        self.temp = Temperature_MLX90614()
        self.moving_detector = MovingDetector()
        self.yl69 = YL69_water_detector()
        
        self.display = Display_7219()
        
        self.cap.start()
        self.cap.telega = self.tel;
        # self.cap.initMobileNet()
        
        httpServer.set_camera(self.cap)
        self.detector.set_camera(self.cap)
        
        self.trainner.set_camera(self.cap)
        self.trainner.set_telega(self.tel)
        
        
        # self.trainner.create_images("max")
        
        conf.updateHttpPassword(10)
        conf.updateQrPassword(10)
        
        print(f"qr пароль {conf.getQrPassword()}")
        print(f'http пароль {conf.getUserHttpPassword()}')
        print("")
        
        

        self.tel.send_ip()
        self.display.show_ip()
        
    
        
        dt = threading.Thread(target=self.Display_thread)
        dt.start()
        
    
        while True:
            
            if conf.is_detector_active:    
                conf.is_qr_reader_active = False  
                
                self.DetectMontion()
             
                
            if conf.is_qr_reader_active:
                conf.is_detector_active = False
                self.cap.check_barcodes()
            
            
            if conf.is_webStream_active:
                if conf.httpServer_working == False:
                    
                    conf.httpServer_working = True
                    phs = threading.Thread(target=httpServer.RunHttpServer)
                    httpServer.server_thread = phs 
                    phs.start()
                    
                

    def DetectMontion(self):

        if self.moving_detector.check_moving() :
            
            det = self.detector.start_regognition_all(self.labels)
            
            frame = det[0]
            text = det[1]
            
            if frame is not None:
                
                cv2.imwrite(f'{conf.pathToProject}/Files/fr.jpg',frame)
                img = open(f'{conf.pathToProject}/Files/fr.jpg','rb')
            
                self.tel.send_photo(img)
                self.tel.send_message(f"обнаружен {text}")
                            
            
            
            
                   
            
            
    
    def allow_sending(self):
        
        if self.tel.keyboard_key == False:
            conf.block_sending = False
            self.tel.Alert_Action()
    
    
    def Display_thread(self):
        
        while True:
            if self.temp.check_fire():
                self.display.show_message7219("fire alarm")  
                self.tel.send_message_for_all_subscribers("пожарная тревога")
                
            elif self.yl69.check_water():
                self.display.show_message7219("flood alert")  
                self.tel.send_message_for_all_subscribers("надоднение")
                
            else:
                moving_letter = str(self.moving_detector.check_moving())[0]
                self.display.draw_info(f"T:{self.temp.get_temp()} M:{moving_letter}")            
                    
            




# try:
Main()
# except Exception as e:
#     print(e)
