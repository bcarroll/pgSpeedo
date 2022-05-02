from time import sleep
#from machine import Pin
#from machine import I2C

#from machine import UART
#from machine import PWM

#from ulib.PicoLCD1_8 import LCD_1inch8
#from ulib.lcd_api import LcdApi
#from ulib.pico_i2c_lcd import I2cLcd

#i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
#lcd = I2cLcd(i2c, 0x27, 2, 16)
#lcd.putstr("init")
#print( dir(lcd) )
#lcd.clear()

from GPS import GPS

gps = GPS()
gps.smoke_test()

#LCD = LCD_1inch8()
#LCD.fill(LCD.BLACK)
#LCD.show()
#LCD.fill_rect(0,0,160,20,LCD.RED)
#LCD.rect(0,0,160,20,LCD.RED)
#LCD.text("M.G. Midget",2,8,LCD.WHITE)
