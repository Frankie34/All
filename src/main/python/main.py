import sys
import cv2
import numpy as np
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog, QGridLayout, QLabel, QPushButton


class win(QDialog):
    def __init__(self):
        # 初始化一个img的ndarry，用于存储图像
        self.img = np.ndarray(())
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(400, 300)
        self.btnOpen = QPushButton('Open', self)
        self.btnSave = QPushButton('Save', self)
        self.btnProcess = QPushButton('Process', self)
        self.btnQuit = QPushButton('Quit', self)
        self.label = QLabel()

        # 布局设定
        layout = QGridLayout(self)
        layout.addWidget(self.label, 0, 1, 3, 4)
        layout.addWidget(self.btnOpen, 4, 1, 1, 1)
        layout.addWidget(self.btnSave, 4, 2, 1, 1)
        layout.addWidget(self.btnProcess, 4, 3, 1, 1)
        layout.addWidget(self.btnQuit, 4, 4, 1, 1)

        # 信号与槽进行连接，信号可绑定普通成员函数
        self.btnOpen.clicked.connect(self.openSlot)
        self.btnSave.clicked.connect(self.saveSlot)
        self.btnProcess.clicked.connect(self.processSlot)
        self.btnQuit.clicked.connect(self.close)

    def openSlot(self):
        # 调用存储文件
        fileName, tmp = QFileDialog.getOpenFileName(self, 'Open Image', 'Image', '*.png *.jpg *.bmp')
        if fileName is '':
            return
        # 采用OpenCV函数读取数据
        self.fileName = fileName
        self.img = cv2.imread(fileName)
        if self.img.size == 1:
            return
        self.refreshShow()

    def saveSlot(self):
        # 调用存储文件dialog
        fileName, tmp = QFileDialog.getSaveFileName(self, 'Save Image', 'Image', '*.png *.jpg *.bmp')
        if fileName is '':
            return
        if self.img.size == 1:
            return
        # 调用OpenCV写入函数
        cv2.imwrite(fileName, self.img)

    def processSlot(self):
        if self.img.size == 1:
            return
        # 对图像缩放
        # self.img = cv2.resize(self.img,None,fx=0.5, fy=0.5, interpolation = cv2.INTER_CUBIC)
        erosion_size = 10
        element = cv2.getStructuringElement(cv2.MORPH_RECT, (2*erosion_size + 1, 2*erosion_size+1), (erosion_size, erosion_size))
        self.img = cv2.erode(self.img, element)
        self.refreshShow()

    
    def refreshShow(self):
        # 提取图像的通道和尺寸，用于将OpenCV下的image转换成Qimage
        height, width, channel = self.img.shape
        bytesPerline = 3 * width
        self.qImg = QImage(self.img.data, width, height, bytesPerline, QImage.Format_RGB888).rgbSwapped()
        # 将QImage显示出来
        self.label.setPixmap(QPixmap.fromImage(self.qImg))


if __name__ == '__main__':
    a = QApplication(sys.argv)
    w = win()
    w.show()
    sys.exit(a.exec_())


# import sys
# import os
# import cv2

# from PyQt5 import QtCore, QtGui, QtWidgets
# from PyQt5.QtWidgets import *
# from PyQt5.QtCore import *
# from PyQt5.QtGui import QPalette, QBrush, QPixmap


# class Ui_MainWindow(QtWidgets.QWidget):
#     def __init__(self, parent=None):
#         super(Ui_MainWindow, self).__init__(parent)

#         self.timer_camera = QtCore.QTimer()  # 初始化定时器
#         self.cap = cv2.VideoCapture()  # 初始化摄像头
#         self.CAM_NUM = 0
#         self.set_ui()
#         self.slot_init()
#         self.__flag_work = 0
#         self.x = 0
#         self.count = 0

#     def set_ui(self):
#         self.__layout_main = QtWidgets.QHBoxLayout()  # 采用QHBoxLayout类，按照从左到右的顺序来添加控件
#         self.__layout_fun_button = QtWidgets.QHBoxLayout()
#         self.__layout_data_show = QtWidgets.QVBoxLayout()  # QVBoxLayout类垂直地摆放小部件

#         self.button_open_camera = QtWidgets.QPushButton(u'打开相机')
#         self.button_close = QtWidgets.QPushButton(u'退出')

#         # button颜色修改
#         button_color = [self.button_open_camera, self.button_close]
#         for i in range(2):
#             button_color[i].setStyleSheet("QPushButton{color:black}"
#                                            "QPushButton:hover{color:red}"
#                                            "QPushButton{background-color:rgb(78,255,255)}"
#                                            "QpushButton{border:2px}"
#                                            "QPushButton{border_radius:10px}"
#                                            "QPushButton{padding:2px 4px}")

#         self.button_open_camera.setMinimumHeight(50)
#         self.button_close.setMinimumHeight(50)

#         # move()方法是移动窗口在屏幕上的位置到x = 500，y = 500的位置上
#         self.move(500, 500)

#         # 信息显示
#         self.label_show_camera = QtWidgets.QLabel()
#         self.label_move = QtWidgets.QLabel()
#         self.label_move.setFixedSize(100, 100)

#         self.label_show_camera.setFixedSize(641, 481)
#         self.label_show_camera.setAutoFillBackground(False)

#         self.__layout_fun_button.addWidget(self.button_open_camera)
#         self.__layout_fun_button.addWidget(self.button_close)
#         self.__layout_fun_button.addWidget(self.label_move)

#         self.__layout_main.addLayout(self.__layout_fun_button)
#         self.__layout_main.addWidget(self.label_show_camera)

#         self.setLayout(self.__layout_main)
#         self.label_move.raise_()
#         self.setWindowTitle(u'摄像头')

#         '''
#         # 设置背景颜色
#         palette1 = QPalette()
#         palette1.setBrush(self.backgroundRole(),QBrush(QPixmap('background.jpg')))
#         self.setPalette(palette1)
#         '''

#     def slot_init(self):  # 建立通信连接
#         self.button_open_camera.clicked.connect(self.button_open_camera_click)
#         self.timer_camera.timeout.connect(self.show_camera)
#         self.button_close.clicked.connect(self.close)

#     def button_open_camera_click(self):
#         if self.timer_camera.isActive() == False:
#             flag = self.cap.open(self.CAM_NUM)
#             if flag == False:
#                 msg = QtWidgets.QMessageBox.Warning(self, u'Warning', u'请检测相机与电脑是否连接正确',
#                                                     buttons=QtWidgets.QMessageBox.Ok,
#                                                     defaultButton=QtWidgets.QMessageBox.Ok)
#                 # if msg==QtGui.QMessageBox.Cancel:
#                 #                     pass
#             else:
#                 self.timer_camera.start(30)
#                 self.button_open_camera.setText(u'关闭相机')
#         else:
#             self.timer_camera.stop()
#             self.cap.release()
#             self.label_show_camera.clear()
#             self.button_open_camera.setText(u'打开相机')

#     def show_camera(self):
#         flag, self.image = self.cap.read()
#         show = cv2.resize(self.image, (640, 480))
#         show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
#         showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
#         self.label_show_camera.setPixmap(QtGui.QPixmap.fromImage(showImage))

#     def closeEvent(self, event):
#         ok = QtWidgets.QPushButton()
#         cancel = QtWidgets.QPushButton()
#         msg = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, u'关闭', u'是否关闭！')
#         msg.addButton(ok, QtWidgets.QMessageBox.ActionRole)
#         msg.addButton(cancel, QtWidgets.QMessageBox.RejectRole)
#         ok.setText(u'确定')
#         cancel.setText(u'取消')
#         if msg.exec_() == QtWidgets.QMessageBox.RejectRole:
#             event.ignore()
#         else:
#             if self.cap.isOpened():
#                 self.cap.release()
#             if self.timer_camera.isActive():
#                 self.timer_camera.stop()
#             event.accept()


# if __name__ == '__main__':
#     App = QApplication(sys.argv)
#     win = Ui_MainWindow()
#     win.show()
#     sys.exit(App.exec_())


# import cv2
# import numpy as np

# from fbs_runtime.application_context.PyQt5 import ApplicationContext
# from PyQt5.QtWidgets import QMainWindow

# from PyQt5 import QtWidgets, QtCore, QtGui
# from PyQt5.QtGui import *
# from PyQt5.QtWidgets import *
# from PyQt5.QtCore import *



# class Ui_MainWindow(object):
#     def setupUi(self, MainWindow):
#         MainWindow.setObjectName("MainWindow")
#         MainWindow.resize(800, 600)
#         self.centralwidget = QtWidgets.QWidget(MainWindow)
#         self.centralwidget.setObjectName("centralwidget")
#         self.label = QtWidgets.QLabel(self.centralwidget)
#         self.label.setGeometry(QtCore.QRect(79, 40, 381, 471))
#         self.label.setObjectName("label")
#         self.pushButton = QtWidgets.QPushButton(self.centralwidget)
#         self.pushButton.setGeometry(QtCore.QRect(610, 90, 101, 32))
#         self.pushButton.setObjectName("pushButton")
#         self.pushButton.clicked.connect(self.shift)
#         self.comboBox = QtWidgets.QComboBox(self.centralwidget)
#         self.comboBox.setGeometry(QtCore.QRect(610, 50, 104, 26))
#         self.comboBox.setObjectName("comboBox")
#         MainWindow.setCentralWidget(self.centralwidget)
#         self.menubar = QtWidgets.QMenuBar(MainWindow)
#         self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
#         self.menubar.setObjectName("menubar")
#         MainWindow.setMenuBar(self.menubar)
#         self.statusbar = QtWidgets.QStatusBar(MainWindow)
#         self.statusbar.setObjectName("statusbar")
#         MainWindow.setStatusBar(self.statusbar)

#         self.retranslateUi(MainWindow)
#         QtCore.QMetaObject.connectSlotsByName(MainWindow)

#     def retranslateUi(self, MainWindow):
#         _translate = QtCore.QCoreApplication.translate
#         MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
#         self.label.setText(_translate("MainWindow", "TextLabel"))
#         self.pushButton.setText(_translate("MainWindow", "PushButton"))

    
#     def openimage(self):
#         imgName, imgType = QFileDialog.getOpenFileName(self.label, "打开图片", "", "*.jpg;;*.png;;All Files(*)")
#         jpg = QtGui.QPixmap(imgName).scaled(self.label.width(), self.label.height())
#         self.label.setPixmap(jpg)
    
#     def shift():
#         img = cv2.imread('jet.jpg',0)
#         rows,cols = img.shape

#         M = np.float32([[1,0,100],[0,1,50]])
#         dst = cv2.warpAffine(img,M,(cols,rows))

#         cv2.imshow('img',dst)
#         cv2.waitKey(0)
#         cv2.destroyAllWindows()

        

# import sys

# if __name__ == '__main__':
#     appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext
#     window = QMainWindow()
#     wids = Ui_MainWindow()
#     wids.setupUi(window)
#     window.show()
#     exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
#     sys.exit(exit_code)




