
import time
import RPi.GPIO as GPIO



mSpeed_1 = 19
mNapr_1 = 27

mSpeed_2 = 17
mNapr_2 = 16




GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(mSpeed_1 ,GPIO.OUT)
GPIO.setup(mNapr_1,GPIO.OUT)# правый мотор

GPIO.setup(mSpeed_2,GPIO.OUT)
GPIO.setup(mNapr_2,GPIO.OUT)# левый мотор




class MotorMood:

    def motorNAZ(self):
        
        GPIO.output(mSpeed_1,True) 
        GPIO.output(mNapr_1,False)

        GPIO.output(mSpeed_2,False) 
        GPIO.output(mNapr_2,True) 

        
      

    def motorS(self):
        GPIO.output(mSpeed_1,False) 
        GPIO.output(mNapr_1,False)

        GPIO.output(mSpeed_2,False) 
        GPIO.output(mNapr_2,False)


    def motorR(self):
        GPIO.output(mSpeed_1,True) 
        GPIO.output(mNapr_1,False)

        GPIO.output(mSpeed_2,True) 
        GPIO.output(mNapr_2,False)

    def motorL(self):
        GPIO.output(mSpeed_1,False) 
        GPIO.output(mNapr_1,True)

        GPIO.output(mSpeed_2,False) 
        GPIO.output(mNapr_2,True)

    
    def motorV(self):
        GPIO.output(mSpeed_1,False) 
        GPIO.output(mNapr_1,True)

        GPIO.output(mSpeed_2,True) 
        GPIO.output(mNapr_2,False) 




