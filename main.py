from PySide6.QtWidgets import QApplication
from user_interface import LoginWindow

def main():
    app = QApplication([])
    login_window = LoginWindow()
    login_window.show()
    app.exec()
    
if __name__ == "__main__":
    main()