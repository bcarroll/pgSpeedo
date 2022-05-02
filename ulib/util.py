# Utility methods
from utime import time
from utime import sleep
from machine import Pin

def toggle_pico_led():
    Pin(25, Pin.OUT).toggle()

def blink_pico_led(repeat=1):
    delay = .01
    for i in range(repeat):
        toggle_pico_led()
        sleep(delay)
        toggle_pico_led()
        sleep(delay)
    
#################################################################

class Log():
    """
    Message logging
    
    Params:
        device    <str>    Device to write Log messages to
    """
    def __init__(self, device='STDOUT'):
        self.device = device
        self.format = '%s %s' # (time(), msg)
        
    def debug(self, msg, device:str=None):
        """
        Display debug messages.
        Modify this message for the intended display device
        """
        if device is None:
            device = self.device

        if device == 'STDOUT':
            print(self.format % (time(),msg))
        else:
            if ':' in device:
                # I2C:OLED:128:32
                (protocol, type,width, height) = device.split(':')
                print('Log device: ', protocol, type,width, height)
            else:
                print ('%s device is not supported' % device)
                return False
        return True

################################################################
