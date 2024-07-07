from PyQt5.Qt import Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QDialog
from traffic_monitor.UI.record_page import Ui_Dialog

class Record(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.set_background()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

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