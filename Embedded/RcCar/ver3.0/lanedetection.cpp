import cv2
import numpy as np
from Raspi_MotorHAT import Raspi_MotorHAT, Raspi_DCMotor
from Raspi_PWM_Servo_Driver import PWM
import time
def DetectLineSlope(src):
    # 흑백화
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

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
    return mimg, degree_L, degree_R

def gogo() :
    myMotor.setSpeed(100)
    pwm.setPWM(0,0,375)
    myMotor.run(Raspi_MotorHAT.BACKWARD)

def autoRight() :
    global pwmm
    pwmm -=45
    if pwmm <= 300 :
        pwmm = 300
    pwm.setPWM(0,0,pwmm)

def mid() :
    global pwmm
    pwm.setPWM(0,0,375)
    pwmm = 375

def autoLeft() :
    global pwmm
    pwmm +=45 
    if pwmm >= 440 :
        pwmm = 440
    pwm.setPWM(0,0,pwmm)

def stop():
    myMotor.run(Raspi_MotorHAT.RELEASE)

pwmm = 375
cap = cv2.VideoCapture(0)
mh = Raspi_MotorHAT(addr=0x6f)
myMotor = mh.getMotor(2)
pwm = PWM(0x6F)
pwm.setPWMFreq(60)
gogo()
try :
    while cap.isOpened():

        ret, frame = cap.read()
        # 상하좌우 반전
        frame = cv2.flip(frame, 0)

        if ret:
            frame = cv2.resize(frame, (640, 360))
            cv2.imshow('ImageWindow', DetectLineSlope(frame)[0])
            l, r = DetectLineSlope(frame)[1], DetectLineSlope(frame)[2]

            if abs(l) <= 155 or abs(r) <= 155:
                if l == 0 or r == 0:
                    if l < 0 or r < 0:
                        autoLeft()
                        print('left')
                    elif l > 0 or r > 0:
                        autoRight()
                        print('right')
                elif abs(l - 15) > abs(r):
                    autoRight()
                    print('right')
                elif abs(r + 15) > abs(l):
                    autoLeft()
                    print('Left')
                else:
                    mid()
                    print('go')
            else:
                if l > 155 or r > 155:
                    print('hard right')
                elif l < -155 or r < -155:
                    print('hard left')


finally:
    cv2.destroyAllWindows()
    cap.release()
    stop()
