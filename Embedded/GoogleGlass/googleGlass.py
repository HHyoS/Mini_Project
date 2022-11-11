import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
from datetime import datetime
now = datetime.now()


#OLED setting
oled_reset = digitalio.DigitalInOut(board.D24)

WIDTH = 128
HEIGHT = 64
BORDER = 5

spi = board.SPI()
oled_cs = digitalio.DigitalInOut(board.D8)
oled_dc = digitalio.DigitalInOut(board.D25)
oled = adafruit_ssd1306.SSD1306_SPI(WIDTH, HEIGHT, spi, oled_dc, oled_reset, oled_cs)

#base객체 생성
base = Image.new('1', (128,64))

#image객체 생성
im = Image.open('pika.png')
size = (64,64)
im.thumbnail(size)
thumb_im = im.convert('1') 

#message객체 생성
message = Image.new('1', (64,64)) 
draw = ImageDraw.Draw(message)
font = ImageFont.load_default()
draw.text((0,10), "HyoSang!!", font=font, fill=1)
draw.text((0,25), now.strftime("%Y.%m.%d"),font=font, fill=1)
draw.text((0,35), now.strftime("%H:%M:%S"),font=font, fill=1) 

base.paste(thumb_im,(0,0)) #image객체를 base의 (0,0)에 복사하기
base.paste(message,(64,0)) #message객체를 base의 (64,0)에 복사하기
base.show()

#OLED에 base 출력
oled.image(base)
oled.show()
