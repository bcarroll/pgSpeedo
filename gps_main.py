import micropython
micropython.alloc_emergency_exception_buf(100)

import utime
from machine import Pin
from machine import Timer

from config import PicoMoto

from ulib.util import Log
from ulib.util import toggle_pico_led
from ulib.util import blink_pico_led

timer = Timer()
mg = PicoMoto()

log = Log()
log.debug(mg.pico_gpio)

def irq_sw():
    log.debug('irq_sw()')

def setup_irq_sw():
    for key in mg.pico_gpio:
        if key.endswith('_sw'):
            if mg.pico_gpio[key] is not None:
                mg.pico_gpio[key].irq(irq_sw, Pin.IRQ_FALLING)

setup_irq_sw()

#timer.init(freq=0.5, mode=Timer.PERIODIC, callback=check_sw)

#log.debug( 'horn_sw: %s' % mg.pico_gpio['horn_sw'].value() )
    

#from ulib.gps import GPS
#
#from utime import sleep_ms
#from _thread import start_new_thread
#
#Log().debug('%s begin' % __name__)
#
#blink_pico_led(repeat=4)
#
#gps = GPS()
#
#def _gps_thread_loop(gps):
#    while True:
#        Log().debug(gps.getPositionData())
#        gps._get_data()
#        sleep_ms(500)
#
#gps_thread = start_new_thread(_gps_thread_loop, (gps,))
#
#print('test')
#sleep_ms(1000)
#print('test2')
#
#blink_pico_led()
#Log().debug('%s end' % __name__)