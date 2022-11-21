개발 목적 :

  개발 보드와 코드를 이용하여 사용자의 입력에 따라 움직이는 RC카 구현해보기
  
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

  ver 1.0 : 키보드를 이용한 rc카 이동 구현
  
  ver 2.0 : 
    1. Python의 Timer 사용하여 주기적으로 Query 로 값 받기
    2. Query로 받은 Command 대로 Motor 제어하기
    3. RC Car에서 Sensing( Using senseHat ) 한 데이터를 DB에 Query 하기
  
  
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
                self.db = mysql.connector.connect(host='13.209.68.90', user='시크륏', password='시크륏', database='hyoDB', auth_plugin='mysql_native_password')
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





