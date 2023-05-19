import os
import threading


import telepot
from telepot.loop import MessageLoop
from telepot import Bot
from telepot.namedtuple import ReplyKeyboardMarkup , InlineKeyboardButton,InlineKeyboardMarkup
from telepot.delegate import pave_event_space, per_inline_from_id, create_open
from telepot.namedtuple import InlineQueryResultArticle, InputTextMessageContent
import urllib3

from db import SubscriberDb

from config import conf
import httpServer



class Telega:
    
  
    def __init__(self):
        self.db = SubscriberDb()
        API_TOKEN = os.environ['API_TOKEN']        
        # self.bot = telepot.Bot(API_TOKEN)
        
        self.bot = telepot.DelegatorBot(API_TOKEN, [
            pave_event_space()(
                per_inline_from_id(), create_open, self.MessageHandler , timeout=20),
        ])
        
        
        self.keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Да это я', callback_data='yes_its_me')],
                [InlineKeyboardButton(text='нет это не я', callback_data='no_its_not_me')],
                # [InlineKeyboardButton(text='нет,call')],
                
        ])

    
    def ComandsListeners(self,msg):
        
        
        chat_id = msg['chat']['id']
        first_name = msg['chat']['first_name']
        last_name = msg['chat']['last_name']
        text = msg['text']

        user = self.db.GetByUserID(chat_id)

        try :
   
            if user is None:
                
                self.bot.sendMessage(chat_id,"введите имя и пароль")
                
                if conf.res['login'] in text:

                    loginText = text

                    loginText = loginText.replace(conf.res['login'],"").replace(" ","")

                    loginText = loginText.split(":")

                    username = loginText[0]
                    password = loginText[1]


                    
                    if username == os.environ['username'] and password == os.environ['password']:

                        self.db.CreateUser(
                            chat_id,
                            first_name,
                            last_name
                        )

                        self.bot.sendMessage(chat_id,"вы успешно вошли")
                    else :
                        self.bot.sendMessage(chat_id,"xex")
                        
    
            else:

                if text == conf.res['turnOnDetector'][0]:
                    conf.is_detector_active = True
                    self.bot.sendMessage(chat_id,f"детектор вкючен")


                elif text == conf.res['turnOFFDetector'][0]:
                    conf.is_detector_active = False
                    self.bot.sendMessage(chat_id,f"детектор выключен")

                elif text == conf.res['runHttpServer'][0] :
                    
                    if conf.httpServer_working == True:
                        self.bot.sendMessage(chat_id,"сервер уже работает")
                        return
                    
                    conf.is_webStream_active = True
                    self.bot.sendMessage(chat_id,f"сервер запущен {httpServer.GetLocalIp()}:{conf.server.port}")
                    self.bot.sendMessage(chat_id,"пароль")
                    self.bot.sendMessage(chat_id,conf.getUserHttpPassword())
                
                
                # elif text == conf.res['shutdownHttpServer'][0]:
                    
                    
                #     print(httpServer.server_thread)
                    
                #     httpServer.server.shutdown()
                #     httpServer.server_thread.join()
                       
                #     conf.httpServer_working = False
                #     conf.is_webStream_active = False
                    
                    
                                        
                #     self.bot.sendMessage(chat_id,"сайт выключен")
                
                    
                    
                
                
                elif text == conf.res["getQrPassword"][0]:
                    img = open(f'{conf.pathToProject}/Files/qrPassword.png','rb')
                    self.bot.sendPhoto(chat_id,img)

                elif text == conf.res['getUserPassword'][0]:
                    self.bot.sendMessage(chat_id,f"пароль пользователя {conf.getUserHttpPassword()}")

                elif text == conf.res["updateUserPassword"][0]:
                    conf.updateHttpPassword(10)
                    self.bot.sendMessage(chat_id,f"пароль обновлен {conf.getUserHttpPassword()}")

                
                elif text == conf.res['turnOnQrLogin'][0]:
                    conf.is_qr_reader_active = True
                    self.bot.sendMessage(chat_id,f"qr-login включен")
                    
                    img = open(f'{conf.pathToProject}/Files/qrPassword.png','rb')
                    self.bot.sendPhoto(chat_id,img)
                
                elif text == conf.res['turnOFFQrLogin'][0]:
                    conf.is_qr_reader_active = False
                    self.bot.sendMessage(chat_id,f"qr-login выключен")
                    
                
                
                
                elif text == conf.res["rebootProgram"][0]:
                    self.bot.sendMessage(chat_id,f"перезапускаю")
                    os.system("sudo systemctl restart telega.service ")



                else :
                    self.bot.sendMessage(chat_id,"есть следующие команды")
                    for r in conf.res.items():
                        if (type(r[1]) != str):
                            self.bot.sendMessage(chat_id,f"{r[1][0]} {r[1][1]}")

        
        except urllib3.exceptions.ReadTimeoutError as e:
            print(f"ReadTimeoutError: {e}")
            
            

        

            
    
    
    def KeyboardListener(self,msg):
        
        message = msg['data']
        
        # conf.block_sending = False
        if conf.is_key_pressed == False:
            conf.is_key_pressed = True
            
        
        
            if message == "yes_its_me":
                
                print("ты свой это хорошо")            
                
                first_name = msg['from']['first_name']
                last_name = msg['from']['last_name']
                
                
                self.send_message(f"замечен {first_name} {last_name}")
                
                
            elif message == "no_its_not_me":         
                self.Alert_Action()
                
                    

            

            
    
    # эта функция отвечает на все сообщения 
    def MessageHandler(self,msg):
        
        # это отвечает на выдвежную клавиатуру
        if not 'chat' in msg:
            self.KeyboardListener(msg)
           
        else:
            # это для остальных сообщений
            self.ComandsListeners(msg)
        
    # Действие после окончания таймера
    def action_after_end(self):
        conf.block_sending = False
        
        if conf.is_key_pressed != False:
            conf.is_key_pressed = False
            # self.Alert_Action()
                
        
                

    def send_photo(self,img):

        subs = self.db.GetAllUserID()
        
        for sub in subs:
            print("отправляю фото ",sub[0],conf.get_time())
         
            try:       
                self.bot.sendPhoto(sub[0],img)                
                # self.bot.sendMessage(sub[0],f"это ты?",reply_markup=self.keyboard)
            
            except urllib3.exceptions.ReadTimeoutError as e:
                print(f"ReadTimeoutError: {e}")
            
            
    def send_cat_photo(self):
        
        subs = self.db.GetAllUserID()
        
        timer = threading.Timer(5, self.action_after_end)
        timer.start()


        for sub in subs:
            print("отправляю фото ",sub[0],conf.get_time())
            img = open(f'{conf.pathToProject}/Files/fr.jpg','rb')
            
            try:    
                self.bot.sendPhoto(sub[0],img)                
                self.bot.sendMessage(sub[0],f"обнаружен кот")
            
            except urllib3.exceptions.ReadTimeoutError as e:
                print(f"ReadTimeoutError: {e}")
            
            
    

            
            
            self.keyboard_key = False
            # conf.block_sending = False


    def send_ip(self):
        
        
        try:              
            subs = self.db.GetAllUserID()
            for sub in subs:
                local_ip = f"{httpServer.GetLocalIp()}"
                self.bot.sendMessage(sub[0],f"робот работает, ip робота {local_ip}")

        except urllib3.exceptions.ReadTimeoutError as e:
                print(f"ReadTimeoutError: {e}")

    
    def send_message(self,message):
        
        try:
            subs = self.db.GetAllUserID()
            for sub in subs:
                self.bot.sendMessage(sub[0],message)
            
        except urllib3.exceptions.ReadTimeoutError as e:
            print(f"ReadTimeoutError: {e}")

    
    def send_document_for_all_subscribers(self,doc):
        
        try:
            subs = self.db.GetAllUserID()
            for sub in subs:
                self.bot.sendDocument(sub[0],doc)
                
        except urllib3.exceptions.ReadTimeoutError as e:
                print(f"ReadTimeoutError: {e}")
        


    def Alert_Action(self):
        
        print("тревога",conf.get_time())
        self.send_message("тревога")
        
        # file = open(f'{conf.pathToProject}/Files/F.mp4','rb')
        # self.send_document_for_all_subscribers(file)
        

        
    

    def RunTelega(self):
        MessageLoop(self.bot,self.MessageHandler).run_as_thread()
        # self.bot.infinity_polling(timeout=10, long_polling_timeout = 5)
   

        print("bot is ready")


    
     




