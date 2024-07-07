from PyQt5.Qt import Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QDialog
from traffic_monitor.UI.monitor_page import Ui_Dialog
from traffic_monitor.monitor_video import Video

class Monitor(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.set_background()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.th1 = Video('source/vd1.mp4')
        # 绑定信号与槽函数
        self.th1.send.connect(self.showimg)
        self.th1.start()
        self.th2 = Video('source/vd2.mp4')
        # 绑定信号与槽函数
        self.th2.send.connect(self.showimg)
        self.th2.start()

    def set_background(self):
        self.label = QtWidgets.QLabel(self)
        self.setCentralWidget(self.label)
        self.pixmap = QtGui.QPixmap(":/home_page.png")
        # 设置QLabel的尺寸
        self.label.resize(self.width(), self.height())
        self.label.setScaledContents(True)
        # 将背景图片设置为QLabel的内容
        self.label.setPixmap(self.pixmap.scaled(self.label.size(), aspectRatioMode=QtCore.Qt.KeepAspectRatio,
                                                transformMode=QtCore.Qt.SmoothTransformation))

    def showimg(self, h, w, c, b, th_id,num):
        image = QImage(b, w, h, w * c, QImage.Format_BGR888)
        pix = QPixmap.fromImage(image)
        if th_id == 1:
            # 自动缩放
            width = self.ui.video1.width()
            height = self.ui.video1.height()
            scale_pix = pix.scaled(width, height, Qt.KeepAspectRatio)
            self.ui.video1.setPixmap(scale_pix)
            # str(num) 类型转换
            self.ui.car_num.setText(str(num))
        if th_id == 2:
            # 自动缩放
            width = self.ui.video2.width()
            height = self.ui.video2.height()
            scale_pix = pix.scaled(width, height, Qt.KeepAspectRatio)
            self.ui.video2.setPixmap(scale_pix)
            # str(num) 类型转换
            self.ui.people_num.setText(str(num))

    def closeEvent(self, event):
        self.th1.stop()
        self.th2.stop()
        self.th1.wait()
        self.th2.wait()
        event.accept()
