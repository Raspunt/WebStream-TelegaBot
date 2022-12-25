import hashlib
import sys
import os
from multiprocessing import Process



class Config:

    is_detector_active = False
    is_webStream_active = False


    httpServer_working = False


    class pin:
        DETECTOR = 23


    class server:
        host='0.0.0.0'
        port = 5000


    res ={
        "login":"/login",
        "turnOnDetector":("/turn_on_detector","включить детектор"),
        "turnOFFDetector":("/turn_off_detector","выключить детектор"),
        'runHttpServer':("/run_http_server",'включить сайт с управлением'),
        'dropHttpServer':("/drop_http_server","выключить сайт с управлением")
    }

    

    def encrypt_string(self,hash_string):
        sha_signature = \
            hashlib.sha256(hash_string.encode()).hexdigest()
        return sha_signature






   


conf = Config()

