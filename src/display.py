import time
from datetime import datetime
import socket

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT

from smbus2 import SMBus
from mlx90614 import MLX90614
import RPi.GPIO as GPIO

from httpServer import GetLocalIp


class Display_7219():
    
    def __init__(self) -> None:
        
        serial = spi(port=0, device=0, gpio=noop())
        self.device = max7219(serial, cascaded=4, block_orientation=90, blocks_arranged_in_reverse_order=True)
        self.device.contrast(8)

                
    
    def show_message7219(self,message):
        show_message(self.device, message, fill="white", font=proportional(CP437_FONT))
        
    
    def show_ip(self):
        
        local_ip = GetLocalIp()
        show_message(self.device, local_ip, fill="white", font=proportional(CP437_FONT))
        
        
        
        # with canvas(self.device) as draw:
        #     text(draw, (0, 1), local_ip, fill="white", font=proportional(TINY_FONT))

    
    def draw_info(self,message):
        
        with canvas(self.device) as draw:
            text(draw, (0, 1), message, fill="white", font=proportional(TINY_FONT))

    