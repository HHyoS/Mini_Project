개발 목적 :

자율주행에서 차선을 이탈하지 않고 주행하는것은 중요한 기능입니다. 그래서 차량과 비슷한 조작이 가능한 rc카를 이용하여 영상처리기반 Line Tracing을 구현하고, 영상처리 Line Tracing의 장점과 개선점을 직접 알아보고자 프로젝트를 진행하게 되었습니다.
  
사용 보드 

  Motor HAT v0.2
  Raspberry pi 4

실행 환경 : VNC Viewer , MobaXterm

기능 :

  1) GO : RC카를 속도를 + 시키는 기능으로 최대 250까지 증가 가능, GO 함수가 호출될 떄 후진을 하던 중 일경우, 후진 -> 0 -> 전진 의 순으로
   속도가 줄어들었다가 속도가 빨라지도록 구현하였습니다.
   
  2) STOP : RC카를 중지시키는 기능

  3) LEFT, RIGHT : RC카의 앞바퀴의 servo 모터의 각도를 조절하여 이동방향을 조절 

  4) BACK : RC카의 속도를 - 시키는 기능으로, 양수일때는 속도를 감소시키다가, 음수가 되면 후진을 하며 가속하도록 구현

  5) init : RC카의 동작을 처음 실행시킬떄 RC카의 방향을 세팅하는 함수

  6) Physic : 쓰레드로 동작할 기능으로, 현실의 자동차를 반영하기 위해 0.5초마다 속도가 일정 속도가 될 때 까지 감소함


버전 :

  ver 1.0 (22.11.16) : 키보드를 이용한 rc카 이동 구현
  
  ver 2.0 (22.11.21): 
    1. Python의 Timer 사용하여 주기적으로 Query 로 값 받기
    2. Query로 받은 Command 대로 Motor 제어하기
    3. RC Car에서 Sensing( Using senseHat ) 한 데이터를 DB에 Query 하기
    
  ver 3.0(예정) : 웹과 연동하여 시각화 
  
  
RC카 사진 


![rn_image_picker_lib_temp_87787bc7-9dc5-448e-b10f-83a14793dc03](https://user-images.githubusercontent.com/57944215/202118874-7fe147b5-faf1-46ad-8e80-4b5c895f8d9a.jpg)


-----------------------------------------------------         Ver 1.0 ------------------------------------------------------------------------------------------------
구현 코드

    from Raspi_MotorHAT import Raspi_MotorHAT, Raspi_DCMotor
    from Raspi_PWM_Servo_Driver import PWM
    from time import sleep
    import curses
    import threading
    mh = Raspi_MotorHAT(addr=0x6f)
    myMotor = mh.getMotor(2) #핀번호
    servo = PWM(0x6F)
    servo.setPWMFreq(60)  # Set frequency to 60 Hz
    screen = curses.initscr()
    curses.noecho()
    curses.cbreak()
    screen.keypad(True)
    pwmValue =380
    speed = 150
    arrow =0 

    def Physics() : // 물리법칙에 따라 속도 
        global speed
        while True :
            if speed >= 55 :
                speed -= 5
            elif speed <= -55 :
                speed += 5
            else :
                continue
            myMotor.setSpeed(abs(speed))
            sleep(0.5)


    def GO():
        global arrow
        global speed
        speed -= 15
        if speed < 0 :
            if arrow == 1 or arrow == 0 :
                myMotor.run(Raspi_MotorHAT.BACKWARD)
                arrow = 2
            if speed < -250 :
                speed = -250
            bSpeed = abs(speed)
            myMotor.setSpeed(bSpeed)
        else :
            myMotor.setSpeed(speed)

    def LEFT():
        global pwmValue
        pwmValue -=5 
        if pwmValue <= 300 :
            pwmValue = 300

        servo.setPWM(0, 0, pwmValue)

    def RIGHT():
        global pwmValue
        pwmValue += 5
        if pwmValue >= 460 :
            pwmValue = 460
        servo.setPWM(0, 0, pwmValue)

    def BACK():
        global arrow
        global speed
        speed += 15

        if speed > 0 :
            if arrow == 2 or arrow == 0 :
                myMotor.run(Raspi_MotorHAT.FORWARD)
                arrow = 1
            if speed > 250 :
                speed = 250
            bSpeed = speed
            myMotor.setSpeed(bSpeed)
        else :
            myMotor.setSpeed(abs(speed))
    def init() :
        global arrow
        arrow=1
        myMotor.setSpeed(speed)
        myMotor.run(Raspi_MotorHAT.FORWARD)

    def STOP():
        myMotor.run(Raspi_MotorHAT.RELEASE)
        servo.setPWM(0,0,380)

    try :
        t = threading.Thread(target = Physics)
        t.start()
        while True :
            char = screen.getch()
            if char == curses.KEY_DOWN  :
                BACK()
            elif char == curses.KEY_RIGHT :
                RIGHT()
            elif char == curses.KEY_LEFT :
                LEFT()
            elif char == curses.KEY_UP :
                GO()
            elif char == ord('q') :
                STOP()
                t.join()
    finally:
        myMotor.run(Raspi_MotorHAT.RELEASE)


-----------------------------------------------------         Ver 2.0 ------------------------------------------------------------------------------------------------\

[  Ui ]

![image](https://user-images.githubusercontent.com/57944215/202979172-90b6d9a8-2b9f-4eed-96b4-90c4726eb339.png)

[ AWS DB테이블 구조 ] 

1. command table ( 컨트롤러의 입력값을 바탕으로 DB에 작성)

![image](https://user-images.githubusercontent.com/57944215/202979328-36263b70-e65d-424e-a5ab-6fc408fcf966.png)

2. sensing table ( RC카에 부착 된 senseHat )

![image](https://user-images.githubusercontent.com/57944215/202979376-6ece5d5b-1555-4c41-9b35-7287649b74ce.png)


[ 컨트롤러 및 RC카 코드 ]

1) 컨트롤러

        from PySide6.QtWidgets import *
        from PySide6.QtCore import *
        from mainUI import Ui_MainWindow
        import mysql.connector

        class MyApp(QMainWindow, Ui_MainWindow):
            def __init__(self):
                super().__init__()
                self.ui = Ui_MainWindow()
                self.ui.setupUi(self)
                self.init()

            def init(self):
                self.db = mysql.connector.connect(host='13.209.68.90', user='hyo', password='시크륏', database='hyoDB', auth_plugin='mysql_native_password')
                self.cur = self.db.cursor()

                #timer setting
                self.timer = QTimer()
                self.timer.setInterval(500) #500ms
                self.timer.timeout.connect(self.pollingQuery)

            def start(self):
                self.timer.start()

            def pollingQuery(self):
                self.cur.execute("select * from command order by time desc limit 15")
                self.ui.logText.clear()
                for (id, time, cmd_string, arg_string, is_finish) in self.cur:
                    str = "%d | %s | %6s | %6s | %4d" % (id, time.strftime("%Y%m%d %H:%M:%S"), cmd_string, arg_string, is_finish)
                    self.ui.logText.appendPlainText(str)

                self.cur.execute("select * from sensing order by time desc limit 15")
                self.ui.sensingText.clear()
                for (id, time, num1, num2, num3, meta_string, is_finish) in self.cur:
                    str = "%d | %s | %6s | %6s | %6s | %10s | %4d" % (id, time.strftime("%Y%m%d %H:%M:%S"), num1, num2, num3, meta_string, is_finish)
                    self.ui.sensingText.appendPlainText(str)
                self.db.commit()

            def closeEvent(self, event):
                self.cur.close()
                self.db.close()

            def insertCommand(self, cmd_string, arg_string):
                time = QDateTime().currentDateTime().toPython()
                is_finish = 0

                query = "insert into command(time, cmd_string, arg_string, is_finish) values (%s, %s, %s, %s)"
                value = (time, cmd_string, arg_string, is_finish)

                self.cur.execute(query, value)
                self.db.commit()

            def go(self):
                self.insertCommand("go", "0")

            def stop(self):
                self.insertCommand("stop", "0")

            def back(self):
                self.insertCommand("back", "0")

            def left(self):
                self.insertCommand("left", "0")

            def mid(self):
                self.insertCommand("mid", "0")

            def right(self):
                self.insertCommand("right", "0")

        app = QApplication()
        win = MyApp()
        win.show()
        app.exec()
    
    
 2) rc카 코드

        from Raspi_MotorHAT import Raspi_MotorHAT, Raspi_DCMotor
        from Raspi_PWM_Servo_Driver import PWM
        import mysql.connector
        from threading import Timer, Lock
        from time import sleep
        import signal
        import sys
        from sense_hat import SenseHat
        from time import sleep
        import datetime

        def closeDB(signal, frame):
            print("BYE")
            mh.getMotor(2).run(Raspi_MotorHAT.RELEASE)
            cur.close()
            db.close()
            timer.cancel()
            timer2.cancel()
            sys.exit(0)

        def polling():
            global cur, db, ready

            lock.acquire()
            cur.execute("select * from command order by time desc limit 1")
            for (id, time, cmd_string, arg_string, is_finish) in cur:
                if is_finish == 1 : break
                ready = (cmd_string, arg_string)
                cur.execute("update command set is_finish=1 where is_finish=0")

            db.commit()
            lock.release()

            global timer
            timer = Timer(0.1, polling)
            timer.start()

        def sensing():
            global cur, db, sense

            pressure = sense.get_pressure()
            temp = sense.get_temperature()
            humidity = sense.get_humidity()

            time = datetime.datetime.now()
            num1 = round(pressure / 10000, 3)
            num2 = round(temp / 100, 2)
            num3 = round(humidity / 100, 2)
            meta_string = '0|0|0'
            is_finish = 0

            print(num1, num2, num3)
            query = "insert into sensing(time, num1, num2, num3, meta_string, is_finish) values (%s, %s, %s, %s, %s, %s)"
            value = (time, num1, num2, num3, meta_string, is_finish)

            lock.acquire()
            cur.execute(query, value)
            db.commit()
            lock.release()

            global timer2
            timer2 = Timer(1, sensing)
            timer2.start()

        def go():
            myMotor.setSpeed(200)
            myMotor.run(Raspi_MotorHAT.FORWARD)

        def back():
            myMotor.setSpeed(200)
            myMotor.run(Raspi_MotorHAT.BACKWARD)

        def stop():
            myMotor.setSpeed(200)
            myMotor.run(Raspi_MotorHAT.RELEASE)

        def left():
            pwm.setPWM(0, 0, 330)

        def mid():
            pwm.setPWM(0, 0, 370)

        def right():
            pwm.setPWM(0, 0, 440)

        #init
        db = mysql.connector.connect(host='13.209.68.90', user='시크륏', password='시크륏', database='hyoDB', auth_plugin='mysql_native_password')
        cur = db.cursor()
        ready = None
        timer = None

        mh = Raspi_MotorHAT(addr=0x6f)
        myMotor = mh.getMotor(2)
        pwm = PWM(0x6F)
        pwm.setPWMFreq(60)

        sense = SenseHat()
        timer2 = None
        lock = Lock()

        signal.signal(signal.SIGINT, closeDB)
        polling()
        sensing()

        #main thread
        while True:
            sleep(0.1)
            if ready == None : continue

            cmd, arg = ready
            ready = None

            if cmd == "go" : go()
            if cmd == "back" : back()
            if cmd == "stop" : stop()
            if cmd == "left" : left()
            if cmd == "mid" : mid()
            if cmd == "right" : right()





---------------------------------------------ver 3.0 -----------------------------------------------------

ver2 대비 변경사항


ver2 

구성 : rc카 ( RPi 4 + Motor Hat )

동작 : 키보드를 통한 이동

통신 : MobaXterm 을 사용하여 RPi 4를 직접 조작

ver 3

구성 : 
  본체 : ver2 Rc카
  
  센서 및 장치 : 
      Pi Camera v2, 초음파 센서, 부저
     
  통신 : Rc카 본체 < - > Aws DB Server < - > PyQt
         Pyqt에서 Ui를 통해 동작을 입력하면 Aws DB서버로 명령어가 전달되고, 해당 명령어를 RC카 본체에서 읽어 동작을 수행
         
  동작 : Aws DB서버를 통한 수동조작 + Open Cv 를 사용한 Line Trace 자율주행
  
        자율주행 중 초음파센서에 설정한 값 이상으로 물체가 가까이 붙으면 주행을 정지하며 부저를 울리고, 수동조작으로 변경
        
        수동 조작 중 초음파 센서에 물체가 다가오면 부저만 울리고 차는 정지하지 않음
   
   구조
   
   ![image](https://user-images.githubusercontent.com/57944215/210769390-9737a27e-bd8e-4e4d-8d8f-73cb89c8c021.png)

  
---------------------------------------------------------------------------------------------------------------------------------------------------------------------

최종 정리 

프로젝트 목적 : 자율주행에서 차선을 이탈하지 않고 주행하는것은 중요한 기능입니다. 그래서 그 기능을 OpenCv의 구현하고 실제 자동차처럼 동작하는 rc카를 구현하고자 하였습니다

프로젝트 기간/인원 : 2022.11.15 ~ 2022.11.25(11일) / 2인( 센서 회로구성,긴급 제동장치 구현 1인, 데이터 통신. 수동/자율주행 구현 1인)

개발 환경 / 언어 / 라이브러리
- DB서버 : AWS기반 Linux(Ubuntu) / mysql
- Rc카 : Raspbian(RPI 4) / python(Raspi Motor 드라이버, numpy, OpenCV)

프로젝트 담당 기능

1. 데이터 통신 및 수동조작 : UI의 입력이 발생시 AWS DB서버에 입력 데이터 query를 보내고, RC카에서는 timer 함수를 사용하여 0.1초마다 DB데이터를 확인하여 데이터와 매칭되는 동작 수행
2. 영상 처리/자율주행 : Pi Camera로 들어온 Canny Edge Detection 알고리즘을 사용하여 Edge를 검출한 뒤 자유주행에 필요한 차선 도출.후 차선을 기준으로 LineTrace 자율주행하도록 Motor 값 설정

트러블 슈팅
Pi camera의 이미지를 처리하여 자율주행을 동작할 때 지연이 발생하여 즉각적인 방향전환이 되지않는 문제가 발생하였습니다
원인를 분석한 결과 카메라에서 이미지를 받아올 때 이미지의 해상도가 높아서 발생하는 지연 이였습니다
문제 해결을 위해 해상도를 기존 960:560에서 640:360으로 낮추었고, 그 결과 기존대비 지연시간을 약 30퍼센트 낮출 수 있었습니다

Why?
1.Mysql vs MariaDB : Mysql은 MariaDB보다 지원 및 레퍼런스가 많은 RDBMS이고 해당 장점은 문제 발생시 빠르게 대처하기 용이하기 때문에 mysql을 선택하였습니다
2. Canny 알고리즘 사용 이유: Sobel 알고리즘도 사용을 고려했지만, 두 알고리즘을 비교 했을 때, 차선검출의 정확도가 Canny보다 떨어졌고 그로인해 Canny 알고리즘을 사용하게되었습니다
3. Pyside vs Pyqt : pyside는 공식으로 파이썬 바인딩으로, 레퍼런스가 더 많고 LGPL정책이 적용되어 실무에서 사용할 경우 PySide를 더 많이 사용할 것이라고 생각하여 선택하게 되었습니다

프로젝트 결과 

1. 영상 기반의 차선인식은 한계가 존재 : 위 프로젝트의 결과물을 바탕으로 테스트했을 떄, 영상처리 기반으로 자율주행을 주행할 때, 바닥에 무늬가 존재한다면 해당 무늬도 차선으로 인식하는 문제가 있었습니다. 해당 문제는 실제 도로의 환경에서도 발생할 수 있는 문제로 모든 도로가 동일한 형태로 존재할 수 없기때문에 만약 영상처리 기반으로 차선을 인식하게 된다면 사고가 날 가능성이 있고, 이것이 영상처리 차선인식의 한계라고 생각합니다.

2. 비교적 간단한 구현 : 단순 영상기반 차선인식의 경우 영상의 입력과 이미지에서 차선검출하는 알고리즘만 구현한다면 비교적 쉽게 구현이 가능합니다. 그래서 만약 영상처리를 통해 
차선을 정확하게 구현할 수 있다면 영상처리 기반 차선인식의 구현용이성은 큰 장점이 될 것이라고 생각합니다.


https://user-images.githubusercontent.com/57944215/204087921-69a872ee-ab2f-4c1e-894c-7f36dc149400.mp4



RC카 항공샷 

![KakaoTalk_20221124_181054249](https://user-images.githubusercontent.com/57944215/203786095-228f7710-0fbd-413a-ba61-04f8da8adb00.jpg)


RC카 정면샷

![KakaoTalk_20221124_181054249_01](https://user-images.githubusercontent.com/57944215/203786114-68ed40ff-3e32-41c9-9334-d4a2ab8fd95b.jpg)

프로젝트 완성기념 한컷

![KakaoTalk_20221124_181054249_02](https://user-images.githubusercontent.com/57944215/203786147-4e29c784-d11e-4c83-8dee-07745fa5c909.jpg)
