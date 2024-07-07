import sys
import json
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from traffic_monitor.UI.login_register_page import Ui_LoginRegister
from traffic_monitor.function_frame import FunctionDialog

# 定义存储用户数据的文件
USER_DATA_FILE = 'users.json'

class LoginRegisterDialog(QtWidgets.QMainWindow, Ui_LoginRegister):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 连接按钮点击事件到对应的处理函数
        self.loginButton.clicked.connect(self.handle_login)
        self.registerButton.clicked.connect(self.handle_register)

    def handle_login(self):
        # 获取输入的用户名和密码
        username = self.loginUsername.text()
        password = self.loginPassword.text()
        # 从文件加载用户数据
        users = self.load_user_data()
        if username in users and users[username] == password:
            QMessageBox.information(self, 'Login', 'Login successful!')
            self.function_dialog = FunctionDialog()
            self.function_dialog.show()
            self.close()
        else:
            QMessageBox.warning(self, 'Login', 'Invalid username or password.')

    def handle_register(self):
        # 获取输入的用户名和密码
        username = self.registerUsername.text()
        password = self.registerPassword.text()
        # 从文件加载用户数据
        users = self.load_user_data()
        if username in users:
            QMessageBox.warning(self, 'Register', 'Username already exists.')
        else:
            users[username] = password
            # 保存用户数据到文件
            self.save_user_data(users)
            QMessageBox.information(self, 'Register', 'Registration successful!')

    def load_user_data(self):
        try:
            with open(USER_DATA_FILE, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            return {}

    def save_user_data(self, users):
        with open(USER_DATA_FILE, 'w') as file:
            json.dump(users, file, indent=4)
