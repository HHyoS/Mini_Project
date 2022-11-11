[ Raspberry Pi zero 를 사용한 단순한 Google Glass  ]

1. 개발 목적 : Raspberry Pi zero 를 사용하여 Google Glass 만들어보기


2. 개발 환경 : 
  1) OS : Raspberry Pi OS

  2) 장비
    1] 개발 보드 : Raspberry Pi zero
    2] LED : OLED Display SSD1306 - SPI통신 사용
    
  3) 회로 연결 
    ![image](https://user-images.githubusercontent.com/57944215/201244393-f91300c6-abfd-465c-b910-fe0401f485ec.png)
    
  4) 개발 전 준비사항
   1] SSD1306 모듈설치
    
      $pip3 install adafruit-circuitpython-ssd1306
      $git clone https://github.com/adafruit/Adafruit_CircuitPython_SSD1306
      
  5) 화면 구성
  
  ![image](https://user-images.githubusercontent.com/57944215/201244595-5524f0ca-a84b-4913-856a-4b6e9ee98f40.png)
  
  
  6) 사용 라이브러리
    1] board
    2] digitalio - board library 와 함께 사용하여 Raspberry Pi zero에 설계한 회로와 연결
    3] PIL - Image, ImageDraw, ImgaeFont - 이미지 영역에 할당할 이미지를 객체로 만들어 화면에 맞도록 프로세싱
    4] adafruit_ssd1306 - SPI 통신을 위한 라이브러리
    5] datetime - 시간 출력용
    
    
  7) 구현

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
    
  8) 실행 방법 
  
    python3 googleGlass.py 
    
    
  10) 사진

  [ 목표 화면 ]
  
  ![image](https://user-images.githubusercontent.com/57944215/201246510-53dbb819-7faf-4c55-a575-ba9a887b3999.png)

  [ OLED화면 ]
  ![rn_image_picker_lib_temp_70d925ec-3d2e-4d56-88c4-af7337d76ce4](https://user-images.githubusercontent.com/57944215/201246162-09552d25-ff98-4d14-9b35-474adfa94c93.jpg)
  
  [ Google Glass ] 
![rn_image_picker_lib_temp_f6a23cef-443c-4bb4-9cc4-87039a8847dc](https://user-images.githubusercontent.com/57944215/201246202-bfafaa58-34f5-4f16-81b8-40461ddd7373.jpg)

  [ 인증샷 ] 
![rn_image_picker_lib_temp_ebec177e-d65e-4e4c-8018-d57e8c02f4e9](https://user-images.githubusercontent.com/57944215/201246242-e467e65e-36e0-44e9-beaa-fb09d8be67ad.jpg)



    
