import numpy
from PySide2.QtWidgets import *
from visual import Ui_MainWindow
from PySide2.QtGui import *
from PySide2.QtCore import *
from time import *
import cv2

class MyThread(QThread) :
    mySignal = Signal(QPixmap)

    def __init__(self):
        super().__init__()
        self.cam = cv2.VideoCapture(0)
        self.cam.set(3,480)
        self.cam.set(4,320)
        self.idx = 0

    def run(self):
        while True :
            ret,self.img = self.cam.read()
            if ret :
                self.printImage(self.img)
            sleep(0.1)
    def printImage(self, imgBGR):

        n_imgRGB = cv2.cvtColor(imgBGR, cv2.COLOR_BGR2RGB)
        h, w, byte = n_imgRGB.shape
        if self.idx == 0 :
            img = QImage(n_imgRGB, w, h, byte * w, QImage.Format_RGB888)
            pix_img = QPixmap(img)
        elif self.idx == 1 :
            imgBlur = cv2.blur(imgBGR,(55,55))
            imgCanny = cv2.Canny(imgBlur,100,100)
            img1 = QImage(imgCanny,w,h,imgCanny.strides[0], QImage.Format_RGB888)
            pix_img = QPixmap(img1)
            
        elif self.idx == 2 :
            imgGray = cv2.cvtColor(imgBGR, cv2.COLOR_BGR2GRAY)
            imgCanny = cv2.Canny(imgGray,100,100)
            img2 = QImage(imgCanny,w,h,imgCanny.strides[0], QImage.Format_Grayscale8)
            pix_img = QPixmap(img2)
            
        elif self.idx == 3 :
            kernel = numpy.ones((3,3))
            imgMor = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel)
            imgCanny = cv2.Canny(imgMor,100,100)
            img3 = QImage(imgCanny,w,h,imgCanny.strides[0], QImage.Format_RGB888)
            pix_img = QPixmap(img3)


        self.mySignal.emit(pix_img)
    
    def changeMode(self,idx) :
        self.idx = idx

class MyApp(QMainWindow, Ui_MainWindow) :
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.main()
        self.idx = 0

    def main(self):
        self.th = MyThread()
        self.th.mySignal.connect(self.setImage)

    def setImage(self,img):
        self.pic1.setPixmap(img)

    def mode(self):
        self.idx = (self.idx+1)%5
        self.th.changeMode(self.idx)

    def play(self):
        self.th.start()

    
    def closeEvent(self, event) :
        self.th.terminate()
        self.th.wait(3000)
        self.close()

app = QApplication()
win = MyApp()
win.show()
app.exec_()

