from ulib.util import blink_pico_led, toggle_pico_led
from ulib.util import Log
from ulib.micropyGPS import MicropyGPS

from utime import sleep_ms
from time import time
from time import sleep
from machine import Pin
from machine import UART
import _thread

log = Log()
log.debug('%s import begin' % __name__)

class GPS():
    def __init__(self, uart=0, baudrate=4800, tx_pin=16, rx_pin=17):
        blink_pico_led()
        sleep_ms(500)
        toggle_pico_led()
        log.debug('%s __init__(uart=%s, baudrate=%s, tx_pin=%s, rx_pin=%s)' % (__name__, uart, baudrate, tx_pin, rx_pin))
        self.gps_uart   = UART(uart, baudrate=baudrate, tx=Pin(tx_pin), rx=Pin(rx_pin))
        self.mGPS       = MicropyGPS()
        print('Aquiring GPS Satellite')
        self._get_data()
        sleep_ms(1000)
        self._get_data()
        self.thread = _thread.start_new_thread(self.thread_loop, ())

    def _get_data(self):
        for i in range(4):
            sentence = self.gps_uart.readline()
            if sentence:
                for char in sentence:
                    try:
                        self.mGPS.update(str(char))
                    except Exception as e:
                        #log.debug(e)
                        pass
    
    def thread_loop(self):
        self.data()
        sleep_ms(500)
    
    def data(self):
        print('Getting GPS data')
        self._get_data()
        data = {
            #'active_segment': self.mGPS.active_segment,
            'altitude': self.mGPS.altitude,

            #'clean_sentences': self.mGPS.clean_sentences,
            'compass_direction': self.mGPS.compass_direction(),
            #'char_count': self.mGPS.char_count,
            #'crc_fails': self.mGPS.crc_fails,
            #'crc_xor': self.mGPS.crc_xor,
            #'coord_format': self.mGPS.coord_format,
            #'course': self.mGPS.course,

            ##'fix_stat': self.mGPS.fix_stat,
            ##'fix_time': self.mGPS.fix_time,
            ##'fix_type': self.mGPS.fix_type,
            
            #'geoid_height': self.mGPS.geoid_height,

            'latitude': self.mGPS.latitude,
            'longitude': self.mGPS.longitude,
            ##'log_en': self.mGPS.log_en,
            ##'log_handle': self.mGPS.log_handle,
            #'local_offset': self.mGPS.local_offset,
                       
            #'process_crc': self.mGPS.process_crc,
            #'gps_segments': self.mGPS.gps_segments,
            #'parsed_sentences': self.mGPS.parsed_sentences,
            #'timestamp': self.mGPS.timestamp,
            'date': self.mGPS.date,

            'satellite_data_updated': self.mGPS.satellite_data_updated(),
            'speed': self.mGPS.speed,
            #'sentence_active': self.mGPS.sentence_active,
            
            #'satellites_in_view': self.mGPS.satellites_in_view,
            #'satellites_in_use': self.mGPS.satellites_in_use,
            #'satellites_used': self.mGPS.satellites_used,
            
            #'last_sv_sentence': self.mGPS.last_sv_sentence,
            #'total_sv_sentences': self.mGPS.total_sv_sentences,
            ##'satellite_data': self.mGPS.satellite_data,
            #'hdop': self.mGPS.hdop,
            #'pdop': self.mGPS.pdop,
            #'vdop': self.mGPS.vdop,
            #'valid': self.mGPS.valid,
            #'start_logging': self.mGPS.start_logging,
            #'stop_logging': self.mGPS.stop_logging,
            #'write_log': self.mGPS.write_log,
            #'gprmc': self.mGPS.gprmc,
            'date_string': self.mGPS.date_string(),
            #'new_fix_time': self.mGPS.new_fix_time,
            #'gpgll': self.mGPS.gpgll,
            #'gpvtg': self.mGPS.gpvtg,
            #'gpgga': self.mGPS.gpgga,
            #'gpgsa': self.mGPS.gpgsa,
            #'gpgsv': self.mGPS.gpgsv,
            #'new_sentence': self.mGPS.new_sentence,
            #'supported_sentences': self.mGPS.supported_sentences,
            ##'satellite_data_updated': self.mGPS.satellite_data_updated(),
            #'unset_satellite_data_updated': self.mGPS.unset_satellite_data_updated,
            ##'satellites_visible': self.mGPS.satellites_visible,
            ##'time_since_fix': self.mGPS.time_since_fix(),
            #'latitude_string': self.mGPS.latitude_string,
            #'longitude_string': self.mGPS.longitude_string,
            'speed_string': self.mGPS.speed_string()
        }
        return data
                       
    #function to convert raw Latitude and Longitude
    #to actual Latitude and Longitude
    def convertToDigree(self, RawDegrees):
        RawAsFloat = float(RawDegrees)
        firstdigits = int(RawAsFloat/100) #degrees
        nexttwodigits = RawAsFloat - float(firstdigits*100) #minutes
        Converted = float(firstdigits + nexttwodigits/60.0)
        Converted = '{0:.6f}'.format(Converted) # to 6 decimal places
        return str(Converted)
    
log.debug('%s import end' % __name__, device='I2C:OLED:128:32')

if __name__ == '__main__':
    gps = GPS()
    #sleep_ms(2000)
    #while True:
    #    print(gps.data())
    #    sleep_ms(1000)

