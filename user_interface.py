from PySide6.QtWidgets import (
    QApplication, 
    QWidget, 
    QLabel, 
    QLineEdit, 
    QPushButton, 
    QVBoxLayout,
    QMainWindow,
    QMessageBox,
    )
from PySide6.QtGui import QPixmap

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('课程编排系统-登录')
        self.setGeometry(300, 300, 300, 150)
        
        self.logo_label = QLabel(self)
        pixmap = QPixmap('bjut.png') 
        self.logo_label.setPixmap(pixmap)
        
        self.username_label = QLabel('用户名:')
        self.password_label = QLabel('密码:')
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        
        self.login_button = QPushButton('登录')
        self.login_button.clicked.connect(self.on_login_clicked)

        layout = QVBoxLayout()
        layout.addWidget(self.logo_label)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def on_login_clicked(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if username == 'admin' and password == '111':
            self.main_window = MainWindow()
            self.main_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "错误", "用户名或密码错误！")
            
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("课程编排系统-主界面")
        self.setGeometry(200, 100, 600, 600)
        
        label = QLabel("欢迎来到主界面！")
        layout = QVBoxLayout()
        layout.addWidget(label)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

if __name__ == '__main__':
    app = QApplication([])
    window = LoginWindow()
    window.show()
    app.exec()
