import random
import string
import json
import time

import qrcode



class Config:
    
    # Вкючает детектор движения или сайт  
    is_detector_active = True
    is_webStream_active = False
    is_qr_reader_active = False
    
    httpServer_working = False
    disable_web_authentication = False
    
    block_sending = False
    
    
    objectDetectorFrame = False
    faceRecognationFrame = False
    QrReaderFrame = False    
    
    
    # телеграм клавиатура 
    is_key_pressed = False
    
    
    
    pathToProject = "/home/pi/progs/WebStream-TelegaBot"

    

    class pin:
        MOVING_DETECTOR = 23
        WATER_DETECTOR = 18


    class server:
        host='0.0.0.0'
        port = 5000


    res ={
        "login":"/login",
        "turnOnDetector":("/turn_on_detector","включить детектор"),
        "turnOFFDetector":("/turn_off_detector","выключить детектор"),
        'runHttpServer':("/run_http_server",'включить сайт с управлением'),
        "getQrPassword":("/get_qr_password","получить пароль от qr-login"),
        "turnOnQrLogin":("/turn_on_qr_login","вкючить qr-login"),
        "turnOFFQrLogin":("/turn_off_qr_login","выключить qr-login"),
        'getUserPassword':("/get_user_password",'получить пароль пользователя'),
        'updateUserPassword':("/update_user_password","обновить пароль пользовалеля"),
        "rebootProgram":("/reboot_program","перезапустить программу робота")
    }
    
    
    localStorage = {
        "httpUsername":"admin",
        "httpPassword":"password",
        'qrPassword':"password"
    }
    
    
    def updateHttpPassword(self,length):
        httpPassword = ''.join(random.choice(string.ascii_letters) for i in range(length))

 
        self.localStorage['httpPassword'] = httpPassword
        
        with open(f'{self.pathToProject}/Files/localStorage.json', 'w+') as outfile:
            json.dump(self.localStorage, outfile, indent=5)  
    
    
    def getUserHttpPassword(self):
    
        file = open(f"{conf.pathToProject}/Files/localStorage.json")
        data = json.load(file)
        
        httpPassword = data["httpPassword"]
        
        return httpPassword
    
    def updateQrPassword(self,length):
        
        qr_password = ''.join(random.choice(string.ascii_letters) for i in range(length))

        
        self.localStorage['qrPassword'] = qr_password
        
        img = qrcode.make(qr_password) 
        img.save(f'{conf.pathToProject}/Files/qrPassword.png')
        
        
        
        with open(f'{self.pathToProject}/Files/localStorage.json', 'w+') as outfile:
            json.dump(self.localStorage, outfile, indent=5)  
        
    
    def getQrPassword(self):
        
        file = open(f"{conf.pathToProject}/Files/localStorage.json")
        data = json.load(file)
        
        httpPassword = data["qrPassword"]
        return httpPassword
    
    
    def get_time(self):
        return time.strftime("%H:%M:%S")
    
        
        
        
        
    

conf = Config()
