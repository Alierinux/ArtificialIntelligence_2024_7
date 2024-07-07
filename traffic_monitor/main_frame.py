from PyQt5 import QtWidgets, QtGui, QtCore
from traffic_monitor.UI.home_page import Ui_Dialog
from traffic_monitor.login_register_frame import LoginRegisterDialog
import Source.source_rc


class MainDialog(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # 设置窗口背景
        self.set_background()
        # 监听窗口大小变化事件
        self.resizeEvent = self.on_resize
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

    def on_resize(self, event):
        self.label.resize(self.width(), self.height())
        self.label.setPixmap(self.pixmap.scaled(self.label.size(), aspectRatioMode=QtCore.Qt.KeepAspectRatio,
                                                transformMode=QtCore.Qt.SmoothTransformation))

    def goto_login_register_page(self):
        self.login_register_dialog = LoginRegisterDialog()
        self.login_register_dialog.show()
        self.close()


