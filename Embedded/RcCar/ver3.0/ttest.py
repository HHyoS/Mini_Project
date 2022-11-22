import threading

from Raspi_MotorHAT import Raspi_MotorHAT, Raspi_DCMotor
from Raspi_PWM_Servo_Driver import PWM
import mysql.connector
from threading import Timer, Lock, Thread
import signal
import sys
from sense_hat import SenseHat
from time import sleep
import datetime
from PySide2.QtWidgets import *
from visual import Ui_MainWindow
from PySide2.QtGui import *
from PySide2.QtCore import *
import numpy as np
from time import *
import cv2
from PIL import Image


class MyThread(QThread):
    mySignal = Signal(QPixmap)

    def __init__(self):
        super().__init__()
        self.cam = cv2.VideoCapture(0)

    def run(self):
        while self.cam.isOpened() :
            ret, self.img = self.cam.read()
            src = cv2.flip(self.img, 0)

            if ret:
                frame = cv2.resize(src, (640, 360))

                cv2.imshow('ImageWindow', self.DetectLineSlope(frame)[0])
                l, r = self.DetectLineSlope(frame)[1], self.DetectLineSlope(frame)[2]

                if abs(l) <= 155 or abs(r) <= 155:
                    if l == 0 or r == 0:
                        if l < 0 or r < 0:
                            print('left')
                        elif l > 0 or r > 0:
                            print('right')
                    elif abs(l - 15) > abs(r):
                        print('right')
                    elif abs(r + 15) > abs(l):
                        print('left')
                    else:
                        print('go')
                else:
                    if l > 155 or r > 155:
                        print('hard right')
                    elif l < -155 or r < -155:
                        print('hard left')

                if cv2.waitKey(1) & 0xff == ord('q'):
                    break
            sleep(0.1)


    def DetectLineSlope(self, ssrc):
        src = cv2.cvtColor(ssrc, cv2.COLOR_BGR2RGB)  # 흑백화
        gray = cv2.cvtColor(ssrc, cv2.COLOR_BGR2GRAY)

        # 모서리 검출
        can = cv2.Canny(gray, 50, 200, None, 3)

        # 관심 구역 설정
        height = can.shape[0]
        rectangle = np.array([[(0, height), (120, 300), (520, 300), (640, height)]])
        mask = np.zeros_like(can)
        cv2.fillPoly(mask, rectangle, 255)
        masked_image = cv2.bitwise_and(can, mask)
        ccan = cv2.cvtColor(masked_image, cv2.COLOR_GRAY2BGR)

        # 직선 검출
        line_arr = cv2.HoughLinesP(masked_image, 1, np.pi / 180, 20, minLineLength=10, maxLineGap=10)

        # line color
        # color = [0, 0, 255]
        # thickness = 5
        # for line in line_arr:
        #   for x1, y1, x2, y2 in line:
        #        cv2.line(ccan, (x1, y1), (x2, y2), color, thickness)

        # 중앙을 기준으로 오른쪽, 왼쪽 직선 분리
        line_R = np.empty((0, 5), int)
        line_L = np.empty((0, 5), int)
        if line_arr is not None:
            line_arr2 = np.empty((len(line_arr), 5), int)
            for i in range(0, len(line_arr)):
                temp = 0
                l = line_arr[i][0]
                line_arr2[i] = np.append(line_arr[i], np.array((np.arctan2(l[1] - l[3], l[0] - l[2]) * 180) / np.pi))
                if line_arr2[i][1] > line_arr2[i][3]:
                    temp = line_arr2[i][0], line_arr2[i][1]
                    line_arr2[i][0], line_arr2[i][1] = line_arr2[i][2], line_arr2[i][3]
                    line_arr2[i][2], line_arr2[i][3] = temp
                if line_arr2[i][0] < 320 and (abs(line_arr2[i][4]) < 170 and abs(line_arr2[i][4]) > 95):
                    line_L = np.append(line_L, line_arr2[i])
                elif line_arr2[i][0] > 320 and (abs(line_arr2[i][4]) < 170 and abs(line_arr2[i][4]) > 95):
                    line_R = np.append(line_R, line_arr2[i])
        line_L = line_L.reshape(int(len(line_L) / 5), 5)
        line_R = line_R.reshape(int(len(line_R) / 5), 5)

        # 중앙과 가까운 오른쪽, 왼쪽 선을 최종 차선으로 인식
        try:
            line_L = line_L[line_L[:, 0].argsort()[-1]]
            degree_L = line_L[4]
            cv2.line(ccan, (line_L[0], line_L[1]), (line_L[2], line_L[3]), (255, 0, 0), 10, cv2.LINE_AA)
        except:
            degree_L = 0
        try:
            line_R = line_R[line_R[:, 0].argsort()[0]]
            degree_R = line_R[4]
            cv2.line(ccan, (line_R[0], line_R[1]), (line_R[2], line_R[3]), (255, 0, 0), 10, cv2.LINE_AA)
        except:
            degree_R = 0

        # 원본에 합성
        mimg = cv2.addWeighted(src, 1, ccan, 1, 0)
        h, w, byte = mimg.shape
        img = QImage(mimg, w, h, byte * w, QImage.Format_RGB888)
        pix_img = QPixmap(img)
        self.mySignal.emit(pix_img)

        return pix_img,degree_L,degree_R



class MyApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.main()

    def main(self):
        self.th = MyThread()
        self.th.mySignal.connect(self.setImage)

    def setImage(self, img):
        self.pic1.setPixmap(img)

    def mode(self):
        pass

    def play(self):
        self.th.start()

    def closeEvent(self, event):
        self.th.terminate()
        self.th.wait(3000)
        self.close()


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
        if is_finish == 1: break
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


def test():
    global ready
    while True:
        sleep(0.1)
        if ready == None: continue

        cmd, arg = ready
        ready = None

        if cmd == "go": go()
        if cmd == "back": back()
        if cmd == "stop": stop()
        if cmd == "left": left()
        if cmd == "mid": mid()
        if cmd == "right": right()


# init
db = mysql.connector.connect(host='3.36.70.114', user='hyo', password='1234', database='hyoDB',
                             auth_plugin='mysql_native_password')
cur = db.cursor()
ready = None
timer = None

mh = Raspi_MotorHAT(addr=0x6f)
myMotor = mh.getMotor(2)
pwm = PWM(0x6F)
pwm.setPWMFreq(60)

# sense = SenseHat()
timer2 = None
lock = Lock()

signal.signal(signal.SIGINT, closeDB)
polling()
# sensing()
t = Thread(target=test)
t.start()
app = QApplication()
win = MyApp()
win.show()
app.exec_()
# main thread



