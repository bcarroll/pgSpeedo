from machine import Pin,SPI,PWM
import framebuf
import time

class LCD_1inch8(framebuf.FrameBuffer):
    BL     = 13
    DC     = 8
    RST    = 12
    MOSI   = 11
    SCK    = 10
    CS     = 9
    width  = 160
    height = 128
    def __init__(self):
        self.cs = Pin(self.CS,Pin.OUT)
        self.rst = Pin(self.RST,Pin.OUT)

        self.cs(1)
        self.spi = SPI(1)
        self.spi = SPI(1,1000_000)
        self.spi = SPI(1,10000_000,polarity=0, phase=0,sck=Pin(self.SCK),mosi=Pin(self.MOSI),miso=None)
        self.dc = Pin(DC,Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()

        #############
        self.backlight_pwm = PWM(Pin(self.BL))
        self.backlight_pwm.freq(1000)
        self.backlight_pwm.duty_u16(32768) #max 65535

        self.WHITE  = 0xFFFF
        self.BLACK  = 0x0000
        self.GREEN  = 0x001F
        self.BLUE   = 0xF800
        self.RED    = 0x07E0

    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def init_display(self):
        """Initialize display"""
        self.rst(1)
        self.rst(0)
        self.rst(1)

        self.write_cmd(0x36)
        self.write_data(0x70)

        self.write_cmd(0x3A)
        self.write_data(0x05)

         #ST7735R Frame Rate
        self.write_cmd(0xB1)
        self.write_data(0x01)
        self.write_data(0x2C)
        self.write_data(0x2D)

        self.write_cmd(0xB2)
        self.write_data(0x01)
        self.write_data(0x2C)
        self.write_data(0x2D)

        self.write_cmd(0xB3)
        self.write_data(0x01)
        self.write_data(0x2C)
        self.write_data(0x2D)
        self.write_data(0x01)
        self.write_data(0x2C)
        self.write_data(0x2D)

        self.write_cmd(0xB4) #Column inversion
        self.write_data(0x07)

        #ST7735R Power Sequence
        self.write_cmd(0xC0)
        self.write_data(0xA2)
        self.write_data(0x02)
        self.write_data(0x84)
        self.write_cmd(0xC1)
        self.write_data(0xC5)

        self.write_cmd(0xC2)
        self.write_data(0x0A)
        self.write_data(0x00)

        self.write_cmd(0xC3)
        self.write_data(0x8A)
        self.write_data(0x2A)
        self.write_cmd(0xC4)
        self.write_data(0x8A)
        self.write_data(0xEE)

        self.write_cmd(0xC5) #VCOM
        self.write_data(0x0E)

        #ST7735R Gamma Sequence
        self.write_cmd(0xe0)
        self.write_data(0x0f)
        self.write_data(0x1a)
        self.write_data(0x0f)
        self.write_data(0x18)
        self.write_data(0x2f)
        self.write_data(0x28)
        self.write_data(0x20)
        self.write_data(0x22)
        self.write_data(0x1f)
        self.write_data(0x1b)
        self.write_data(0x23)
        self.write_data(0x37)
        self.write_data(0x00)
        self.write_data(0x07)
        self.write_data(0x02)
        self.write_data(0x10)

        self.write_cmd(0xe1)
        self.write_data(0x0f)
        self.write_data(0x1b)
        self.write_data(0x0f)
        self.write_data(0x17)
        self.write_data(0x33)
        self.write_data(0x2c)
        self.write_data(0x29)
        self.write_data(0x2e)
        self.write_data(0x30)
        self.write_data(0x30)
        self.write_data(0x39)
        self.write_data(0x3f)
        self.write_data(0x00)
        self.write_data(0x07)
        self.write_data(0x03)
        self.write_data(0x10)

        self.write_cmd(0xF0) #Enable test command
        self.write_data(0x01)

        self.write_cmd(0xF6) #Disable ram power save mode
        self.write_data(0x00)

            #sleep out
        self.write_cmd(0x11)
        #DEV_Delay_ms(120)

        #Turn on the LCD display
        self.write_cmd(0x29)

    def show(self):
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(0x01)
        self.write_data(0x00)
        self.write_data(0xA0)
        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(0x02)
        self.write_data(0x00)
        self.write_data(0x81)
        self.write_cmd(0x2C)
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)

    @micropython.native
    def TFTColor( self, aR, aG, aB ) :
      '''Create a 16 bit rgb value from the given R,G,B from 0-255.
         This assumes rgb 565 layout and will be incorrect for bgr.'''
      return ((aR & 0xF8) << 8) | ((aG & 0xFC) << 3) | (aB >> 3)

    def show_image(self, image_file):
        f = open(image_file, 'rb')
        if f.read(2) == b'BM':  #header
            dummy   = f.read(8) #file size(4), creator bytes(4)
            offset  = int.from_bytes(f.read(4), 'little')
            hdrsize = int.from_bytes(f.read(4), 'little')
            image_width   = int.from_bytes(f.read(4), 'little')
            image_height  = int.from_bytes(f.read(4), 'little')
            if int.from_bytes(f.read(2), 'little') == 1: #planes must be 1
                depth = int.from_bytes(f.read(2), 'little')
                if depth == 24 and int.from_bytes(f.read(4), 'little') == 0:#compress method == uncompressed
                    print("Image size:", image_width, "x", image_height)
                    rowsize = (image_width * 3 + 3) & ~3
                    if image_height < 0:
                        image_height = -image_height
                        flip = False
                    else:
                        flip = True
                    w, h = image_width, image_height
                    if w > self.height: w = self.height
                    if h > self.width: h = self.width
                    for row in range(h):
                        if flip:
                            pos = offset + (image_height - 1 - row) * rowsize
                        else:
                            pos = offset + row * rowsize
                        if f.tell() != pos:
                            dummy = f.seek(pos)
                        for col in range(w):
                            col = w-col
                            bgr = f.read(3)
                            self.pixel(row, col, self.TFTColor(bgr[2],bgr[1],bgr[0]))
                    self.show()


if __name__=='__main__':
    LCD = LCD_1inch8()
    #color BRG
    LCD.fill(LCD.WHITE)
    LCD.show()

    LCD.fill_rect(0,0,160,20,LCD.RED)
    LCD.rect(0,0,160,20,LCD.RED)
    LCD.text("Raspberry Pi Pico",2,8,LCD.WHITE)

    LCD.fill_rect(0,20,160,20,LCD.BLUE)
    LCD.rect(0,20,160,20,LCD.BLUE)
    LCD.text("PicoGo",2,28,LCD.WHITE)

    LCD.fill_rect(0,40,160,20,LCD.GREEN)
    LCD.rect(0,40,160,20,LCD.GREEN)
    LCD.text("Pico-LCD-1.8",2,48,LCD.WHITE)

    LCD.fill_rect(0,60,160,10,0X07FF)
    LCD.rect(0,60,160,10,0X07FF)
    LCD.fill_rect(0,70,160,10,0xF81F)
    LCD.rect(0,70,160,10,0xF81F)
    LCD.fill_rect(0,80,160,10,0x7FFF)
    LCD.rect(0,80,160,10,0x7FFF)
    LCD.fill_rect(0,90,160,10,0xFFE0)
    LCD.rect(0,90,160,10,0xFFE0)
    LCD.fill_rect(0,100,160,10,0XBC40)
    LCD.rect(0,100,160,10,0XBC40)
    LCD.fill_rect(0,110,160,10,0XFC07)
    LCD.rect(0,110,160,10,0XFC07)
    LCD.fill_rect(0,120,160,10,0X8430)
    LCD.rect(0,120,160,10,0X8430)
    LCD.show()
    time.sleep(1)
    LCD.fill(0xFFFF)