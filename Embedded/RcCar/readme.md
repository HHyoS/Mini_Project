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


RC카 사진 


![rn_image_picker_lib_temp_87787bc7-9dc5-448e-b10f-83a14793dc03](https://user-images.githubusercontent.com/57944215/202118874-7fe147b5-faf1-46ad-8e80-4b5c895f8d9a.jpg)

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

