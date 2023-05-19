from mlx90614 import MLX90614
from smbus2 import SMBus
import RPi.GPIO as GPIO

from config import conf


def sensors_init():
    GPIO.setmode(GPIO.BCM)


class Temperature_MLX90614():
    
    
    def __init__(self) -> None:
        bus = SMBus(1)
        self.sensor = MLX90614(bus, address=0x5A)
    
    def get_temp(self):
        return  round(self.sensor.get_obj_temp())
    
    
    def check_fire(self):
        if self.sensor.get_obj_temp() >= 40:
            return True

        return False
    


class MovingDetector():
    
    
    def __init__(self) -> None:   
        GPIO.setup(conf.pin.MOVING_DETECTOR, GPIO.IN)
        
    
    
    def check_moving(self):    
        if GPIO.input(conf.pin.MOVING_DETECTOR):
            return True
        
        return False
    
    
class YL69_water_detector():
    
    def __init__(self) -> None:
        GPIO.setup(conf.pin.WATER_DETECTOR, GPIO.IN)

    def check_water(self):
        if GPIO.input(conf.pin.WATER_DETECTOR):
            return False
        
        return True


# sensors_init()
# while True:
    
#     yl69 = YL69_water_detector()
    
#     print(yl69.check_water())
    
    
    