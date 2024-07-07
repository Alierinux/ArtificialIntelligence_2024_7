from PyQt5.Qt import Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QDialog
from traffic_monitor.UI.classify_page import Ui_Dialog
from traffic_monitor.classify_video import Video
import json


class Classify(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.set_background()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.introduction.setWordWrap(True)
        self.th3 = Video('source/vd3.mp4')
        # 绑定信号与槽函数
        self.th3.send.connect(self.showimg)
        self.th3.start()

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

    def showimg(self, h, w, c, b, th_id, num, msg):
        msg = json.loads(msg)
        image = QImage(b, w, h, w * c, QImage.Format_BGR888)
        pix = QPixmap.fromImage(image)
        if th_id == 3:
            # 自动缩放
            width = self.ui.video3.width()
            height = self.ui.video3.height()
            scale_pix = pix.scaled(width, height, Qt.KeepAspectRatio)
            self.ui.video3.setPixmap(scale_pix)
            if num>0:
                # str(num) 类型转换
                self.ui.general_num.setText(str(num))
                # 提取并拼接 msg 中的内容
                introduction_text = ""
                for entry in msg:
                    keyword = entry.get('keyword', '未知')
                    description = entry.get('baike_info', {}).get('description', '无描述')
                    introduction_text += f"关键词: {keyword}\n描述: {description}\n\n"
                self.ui.introduction.setText(introduction_text)

    def classifyPushButton(self):
        self.th3.change_video_flag()

    def closeEvent(self, event):
        self.th3.stop()
        self.th3.stop()
        event.accept()
