from PyQt5.QtCore import QThread
import cv2 as cv
from PyQt5.QtCore import pyqtSignal
from ai.traffic import general
import time
import json


# 重写run()方法: 线程执行的内容
# Thread的实例对象.start()  run()就会自动执行
class Video(QThread):
    # 使用信号与槽槽函数向外传递数据
    #    发送者   Video
    #    信号类型  自定义信号类型(参数信号所能传递的数据)
    #    接收者   （线程所在的Dialog）
    #    槽函数   （接收者类：功能方法）
    send = pyqtSignal(int, int, int, bytes, int, int, str)  #emit

    def __init__(self, video_id):
        super().__init__()
        self.video_flag = False
        # 准备工作
        self.th_id = 0
        if video_id == 'source/vd3.mp4':
            self.th_id = 3
        # 创建视频捕获实例
        self.dev = cv.VideoCapture(video_id)
        # 打开视频文件
        self.dev.open(video_id)
        self._running = True

    def run(self):
        while self._running:
            ret, frame = self.dev.read()
            if self.th_id == 3:
                msg, num, self.video_flag = general(frame, self.video_flag)
                # 将 msg 转换为 JSON 字符串
                msg = json.dumps(msg)
            print("ret:", ret)
            if not ret:
                print('no')
            # 获取图像的高、宽和通道数
            h, w, c = frame.shape
            # 将图像转换为字节数组
            img_bytes = frame.tobytes()
            # 发送信号
            print(msg)
            self.send.emit(h, w, c, img_bytes, self.th_id, num, msg)
            time.sleep(1)
            QThread.usleep(1000)

    def change_video_flag(self):
        self.video_flag = True

    def stop(self):
        self._running = False
        self.dev.release()
