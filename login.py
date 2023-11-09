from PySide6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('课程编排系统')
        self.setGeometry(300, 300, 300, 150)

        self.username_label = QLabel('用户名:')
        self.password_label = QLabel('密码:')
        self.username_edit = QLineEdit()
        self.password_edit = QLineEdit()
        self.login_button = QPushButton('登录')

        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_edit)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_edit)
        layout.addWidget(self.login_button)

        self.login_button.clicked.connect(self.on_login_clicked)

        self.setLayout(layout)

    def on_login_clicked(self):
        username = self.username_edit.text()
        password = self.password_edit.text()

        if username == 'admin' and password == 'password':
            print('登录成功！')
        else:
            print('登录失败！')

if __name__ == '__main__':
    app = QApplication([])
    window = LoginWindow()
    window.show()
    app.exec()
