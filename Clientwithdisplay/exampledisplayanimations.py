# WaveShare Pico LCD 1.8 inch Display
# TFT Display Workout
# Tony Goodhew - 1 July 2021
#======== START OF DRIVER AND SETUP ===========
# https://www.waveshare.com/wiki/Pico-LCD-1.8
from machine import Pin,SPI,PWM
import framebuf
import machine
import utime
import random
import math

BL = 13
DC = 8
RST = 12
MOSI = 11
SCK = 10
CS = 9

class LCD_1inch8(framebuf.FrameBuffer):
    def __init__(self):
        self.width = 161 # This number was not expected?
        self.height = 130
        
        self.cs = Pin(CS,Pin.OUT)
        self.rst = Pin(RST,Pin.OUT)
        
        self.cs(1)
        self.spi = SPI(1)
        self.spi = SPI(1,1000_000)
        self.spi = SPI(1,10000_000,polarity=0, phase=0,sck=Pin(SCK),mosi=Pin(MOSI),miso=None)
        self.dc = Pin(DC,Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()
        
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
        
        self.write_cmd(0x36);
        self.write_data(0x70);
        
        self.write_cmd(0x3A);
        self.write_data(0x05);

         #ST7735R Frame Rate
        self.write_cmd(0xB1);
        self.write_data(0x01);
        self.write_data(0x2C);
        self.write_data(0x2D);

        self.write_cmd(0xB2);
        self.write_data(0x01);
        self.write_data(0x2C);
        self.write_data(0x2D);

        self.write_cmd(0xB3);
        self.write_data(0x01);
        self.write_data(0x2C);
        self.write_data(0x2D);
        self.write_data(0x01);
        self.write_data(0x2C);
        self.write_data(0x2D);

        self.write_cmd(0xB4); #Column inversion
        self.write_data(0x07);

        #ST7735R Power Sequence
        self.write_cmd(0xC0);
        self.write_data(0xA2);
        self.write_data(0x02);
        self.write_data(0x84);
        self.write_cmd(0xC1);
        self.write_data(0xC5);

        self.write_cmd(0xC2);
        self.write_data(0x0A);
        self.write_data(0x00);

        self.write_cmd(0xC3);
        self.write_data(0x8A);
        self.write_data(0x2A);
        self.write_cmd(0xC4);
        self.write_data(0x8A);
        self.write_data(0xEE);

        self.write_cmd(0xC5); #VCOM
        self.write_data(0x0E);

        #ST7735R Gamma Sequence
        self.write_cmd(0xe0);
        self.write_data(0x0f);
        self.write_data(0x1a);
        self.write_data(0x0f);
        self.write_data(0x18);
        self.write_data(0x2f);
        self.write_data(0x28);
        self.write_data(0x20);
        self.write_data(0x22);
        self.write_data(0x1f);
        self.write_data(0x1b);
        self.write_data(0x23);
        self.write_data(0x37);
        self.write_data(0x00);
        self.write_data(0x07);
        self.write_data(0x02);
        self.write_data(0x10);

        self.write_cmd(0xe1);
        self.write_data(0x0f);
        self.write_data(0x1b);
        self.write_data(0x0f);
        self.write_data(0x17);
        self.write_data(0x33);
        self.write_data(0x2c);
        self.write_data(0x29);
        self.write_data(0x2e);
        self.write_data(0x30);
        self.write_data(0x30);
        self.write_data(0x39);
        self.write_data(0x3f);
        self.write_data(0x00);
        self.write_data(0x07);
        self.write_data(0x03);
        self.write_data(0x10);

        self.write_cmd(0xF0); #Enable test command
        self.write_data(0x01);

        self.write_cmd(0xF6); #Disable ram power save mode
        self.write_data(0x00);

            #sleep out
        self.write_cmd(0x11);
        #DEV_Delay_ms(120);

        #Turn on the LCD display
        self.write_cmd(0x29);

    def show(self):
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(0x01)
        self.write_data(0x00)
        self.write_data(0xf1)        
        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(0x01)
        self.write_data(0x00)
        self.write_data(0xf1)        
        self.write_cmd(0x2C)       
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)
  
pwm = PWM(Pin(BL))
pwm.freq(1000)

pwm.duty_u16(32768) # max 65535
LCD = LCD_1inch8()
# Background colour is BLACK
LCD.fill(0x0) # BLACK
LCD.show()
# ============= END OF SCREEN DRIVER & SETUP ==================


def colour(R,G,B):
# Get RED value
    rp = int(R*31/255) # range 0 to 31
    if rp < 0: rp = 0
    r = rp *8
# Get Green value - more complicated!
    gp = int(G*63/255) # range 0 - 63
    if gp < 0: gp = 0
    g = 0
    if gp & 1:  g = g + 8192
    if gp & 2:  g = g + 16384
    if gp & 4:  g = g + 32768
    if gp & 8:  g = g + 1
    if gp & 16: g = g + 2
    if gp & 32: g = g + 4
# Get BLUE value       
    bp =int(B*31/255) # range 0 - 31
    if bp < 0: bp = 0
    b = bp *256
    colour = r+g+b
    return colour
    
def ring(cx,cy,r,cc):   # Centre (x,y), radius
    for angle in range(0, 90, 2):  # 0 to 90 degrees in 2s
        y3=int(r*math.sin(math.radians(angle)))
        x3=int(r*math.cos(math.radians(angle)))
        LCD.pixel(cx-x3,cy+y3,cc)  # 4 quadrants
        LCD.pixel(cx-x3,cy-y3,cc)
        LCD.pixel(cx+x3,cy+y3,cc)
        LCD.pixel(cx+x3,cy-y3,cc)
#=============== MAIN ============

LCD.rect(1,1,159,128,colour(0,0,255)) # Blue Frame
LCD.text("WaveShare", 38,20,colour(255,0,0))
LCD.text('Pico Display 1.8"', 10,40,colour(255,255,0))
LCD.text("159x128 SPI", 30,60,colour(0,255,0))
LCD.text("WORKOUT", 50,80,colour(255,128,0))
LCD.text("Tony Goodhew", 30,110,colour(100,100,100))
LCD.show()
utime.sleep(6)
LCD.fill(0)
LCD.show()

LCD.rect(1,1,159,128,colour(0,0,255)) # Blue Frame
# White Corners
LCD.pixel(1,1,0xFFFF)     # LT
LCD.pixel(1,128,0xFFFF)   # LB
LCD.pixel(159,1,0xFFFF)   # RT
LCD.pixel(159,128,0xFFFF) # RB
LCD.text("200 Pixels", 40,20,0xFFFF)
LCD.rect(29,49,103,53,colour(0,255,0))
LCD.show()
for i in range (200):
    x = random.randint(30, 130)
    y = random.randint(50, 100)
    LCD.pixel(x,y,0xFFFF)
    LCD.show()
utime.sleep(1.5)
LCD.fill(0)
LCD.show()

# Lines
LCD.text("Lines",10,10,colour(200,200,200))
LCD.show()
c = colour(255,0,0)
b = colour(0,0,255)
LCD.vline(1,1,128,c)
LCD.hline(1,128,128,c)
LCD.vline(159,1,128,b)
LCD.hline(159-127,1,128,b)
for i in range(0,127,5):
    ii = i +1
    LCD.line(1,ii,ii,128,c)
    LCD.line(159,128-ii,159-ii,1,b)
    utime.sleep(0.03)
    LCD.show()

LCD.text("Circles",95,112,colour(200,200,200))
LCD.show()
ring(80,64,47,colour(70,70,70))
ring(80,64,41,colour(100,100,100))
ring(80,64,35,colour(150,150,150))
LCD.show()
ring(80,64,30,colour(255,255,0))
ring(80,64,25,colour(255,0,255))
ring(80,64,20,colour(0,255,255))
LCD.show()
utime.sleep(1)
for r in range(5):
    ring(80,64,10+r,colour(255,0,0))
LCD.show()
utime.sleep(1)
for r in range(5):
    ring(80,64,5+r,colour(0,255,0))
LCD.show()
utime.sleep(1)
for r in range(5):
    ring(80,64,r,colour(0,0,255))
LCD.show()
utime.sleep(2.5)
LCD.fill(0)
LCD.show()

# === Sin & Cos graphs ====
factor = 361 /159    
LCD.show()
cr = colour(255,0,0)
LCD.hline(1,60,159,0xFFFF)
LCD.text("Sine", 70, 20, cr)
for x in range(1,159):
    y = int ((math.sin(math.radians(x * factor)))* -50) + 60
    LCD.pixel(x,y,cr)
    LCD.show()
LCD.show()

cg = colour(0,255,0)
LCD.text("Cosine", 5, 90, cg)
for x in range(0,240):
    y = int((math.cos(math.radians(x * factor)))* -50) + 60
    LCD.pixel(x,y,cg)
LCD.show()
utime.sleep(3)
LCD.fill(0)
LCD.show()

# Text on a Sin wave
msg ='  WS Pico Display'
LCD.text("Text on a Sine Curve",1,115,0xFFFF)
factor = 361 /159
for i in range(len(msg)):
    y = int ((math.sin(math.radians(i*7 * factor)))* -40) + 40
    ch = msg[i]
    LCD.text(ch, i*8,y +10,colour(255,255,0))
    LCD.show()
utime.sleep(3)
LCD.fill(0)
LCD.show()

# Set up potentiometers
rpot=machine.ADC(28)
gpot=machine.ADC(27)
bpot=machine.ADC(26)
LCD.fill(0)
LCD.show()
LCD.text(" Turn the Pots",20,112,0xFFFF)
LCD.hline(0,127,159,0xFFFF) # Draw edge frame Bottom
LCD.line(0,1,159,1,0xFFFF)                  # Top  
LCD.vline(0,1,127,0xFFFF)                   # Left
LCD.line(159,0,159,127,0xFFFF)              # Right
while True:
# Get RED value
    rp = int(rpot.read_u16() / 2000) # range 0 to 31
    if rp < 0: rp = 0
    if rp > 31: rp = 31
    r = rp *8
# Get Green value - more complicated!
    gp = int(gpot.read_u16() / 1000) # range 0 - 63
    if gp < 0: gp = 0
    if gp > 63: gp = 63
    g = 0
    if gp & 1:  g = g + 8192
    if gp & 2:  g = g + 16384
    if gp & 4:  g = g + 32768
    if gp & 8:  g = g + 1
    if gp & 16: g = g + 2
    if gp & 32: g = g + 4
# Get BLUE value       
    bp =int(bpot.read_u16() / 2090) # range 0 - 31
    if bp < 0: bp = 0
    if bp > 31: gp = 31
    b = bp *256

    colour = r+g+b

    LCD.fill_rect(4,20,152,20,colour)
    LCD.fill_rect(50,5,80,10,0) # Black out old value
    LCD.text(str(hex(colour)),58,7,0xFFFF)
    
    LCD.fill_rect(10,55,140,10,0)
    LCD.text(str(rp),10,55,0xF8) # RED
    LCD.fill_rect(120,55,25,10,r)
    LCD.rect(120,55,25,10,0xAA52) # Grey2 frame
    if rp > 0: LCD.fill_rect(35,55,rp*2,10,0x76AD) # GREY
    
    LCD.fill_rect(10,75,140,10,0)
    LCD.text(str(gp),10,75,0xE007) # GREEN
    LCD.fill_rect(120,75,25,10,g)
    LCD.rect(120,75,25,10,0xAA52)
    if gp > 0: LCD.fill_rect(35,75,gp,10,0x76AD)
    
    LCD.fill_rect(10,95,140,10,0)
    LCD.text(str(bp),10,95,0x1F00) # BLUE   
    LCD.fill_rect(120,95,25,10,b)
    LCD.rect(120,95,25,10,0xAA52)
    if bp > 0: LCD.fill_rect(35,95,bp*2,10,0x76AD)
    
    LCD.fill(LCD.WHITE)
    LCD.show()
