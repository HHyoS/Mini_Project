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

def Physics() :
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


def BACK():
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

def GO():
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
            GO()
        elif char == curses.KEY_RIGHT :
            RIGHT()
        elif char == curses.KEY_LEFT :
            LEFT()
        elif char == curses.KEY_UP :
            BACK()
        elif char == ord('q') :
            STOP()
            t.join()
finally:
    myMotor.run(Raspi_MotorHAT.RELEASE)

