from PyQt5.QtWidgets import QApplication
from traffic_monitor.main_frame import MainDialog
import sys

# -----------------------------------页面测试用可以删除
from traffic_monitor.login_register_frame import LoginRegisterDialog
from traffic_monitor.function_frame import FunctionDialog
from traffic_monitor.monitor_frame import Monitor
from traffic_monitor.classify_frame import Classify


class TrafficMonitorAPP(QApplication):
    def __init__(self):
        super(TrafficMonitorAPP, self).__init__(sys.argv)
        self.dialog = MainDialog()
        self.dialog.show()
