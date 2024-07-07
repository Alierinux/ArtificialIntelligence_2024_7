from PyQt5.QtCore import QThread
import cv2 as cv
from PyQt5.QtCore import pyqtSignal
from ai.traffic import vehicle_detect, body_attr
import time


# 重写run()方法: 线程执行的内容
# Thread的实例对象.start()  run()就会自动执行
class Video(QThread):
    # 使用信号与槽槽函数向外传递数据
    #    发送者   Video
    #    信号类型  自定义信号类型(参数信号所能传递的数据)
    #    接收者   （线程所在的Dialog）
    #    槽函数   （接收者类：功能方法）
    send = pyqtSignal(int, int, int, bytes, int, int)  #emit

    def __init__(self, video_id):
        super().__init__()
        # 准备工作
        self.th_id = 0
        if video_id == 'source/vd1.mp4':
            self.th_id = 1
        if video_id == 'source/vd2.mp4':
            self.th_id = 2
        # 创建视频捕获实例
        self.dev = cv.VideoCapture(video_id)
        # 打开视频文件
        self.dev.open(video_id)
        self._running = True

    def run(self):
        while self._running:
            ret, frame = self.dev.read()
            if self.th_id == 1:
                frame, num = vehicle_detect(frame)
            elif self.th_id == 2:
                frame, num = body_attr(frame)
            print("ret:", ret)
            if not ret:
                print('no')
            # 获取图像的高、宽和通道数
            h, w, c = frame.shape
            # 将图像转换为字节数组
            img_bytes = frame.tobytes()
            # 发送信号
            self.send.emit(h, w, c, img_bytes, self.th_id, num)
            time.sleep(1)
            QThread.usleep(1000)

    def stop(self):
        self._running = False
        self.dev.release()
