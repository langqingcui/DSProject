from PySide6.QtWidgets import (
    QApplication, 
    QWidget, 
    QLabel, 
    QLineEdit, 
    QPushButton, 
    QVBoxLayout,
    QHBoxLayout,
    QMainWindow,
    QMessageBox,
    QTextEdit,
    QGroupBox,
    )
from PySide6.QtGui import QPixmap
from courses_topological_division import generate_course_divisions

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('课程编排系统-登录')
        self.resize(300, 150)
        
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

        self.setWindowTitle("Course Planner")
        self.resize(800, 600)

        # Main horizontal layout
        main_layout = QHBoxLayout()

        # Button area layout
        button_layout = QVBoxLayout()
        button_layout.setSpacing(10)

        # Import button
        self.import_button = QPushButton("Import")
        button_layout.addWidget(self.import_button)
        self.import_button.clicked.connect(self.import_data)

        # Generate button
        self.generate_button = QPushButton("Generate")
        button_layout.addWidget(self.generate_button)
        self.generate_button.clicked.connect(self.generate_division)

        # Export button
        self.export_button = QPushButton("Export")
        button_layout.addWidget(self.export_button)
        self.export_button.clicked.connect(self.export_data)
        
        button_layout.addStretch()

        # Widget to hold the buttons
        button_widget = QWidget()
        button_widget.setLayout(button_layout)
        button_widget.setFixedWidth(100)  # Set a fixed width for the button area

        # Add the button layout to the main layout
        main_layout.addWidget(button_widget)

        # GroupBox for semester text areas
        semester_group_box = QGroupBox("Semesters")
        semester_layout = QVBoxLayout()

        # Text boxes for semesters
        self.semester_boxes = []
        for i in range(8):
            text_edit = QTextEdit()
            text_edit.setReadOnly(True)
            text_edit.setPlaceholderText(f"Semester {i+1}")
            self.semester_boxes.append(text_edit)
            semester_layout.addWidget(text_edit)

        semester_group_box.setLayout(semester_layout)

        # Add the GroupBox to the main layout
        main_layout.addWidget(semester_group_box)

        # Central widget setup
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def import_data(self):
        pass

    def generate_division(self):
        divisions = generate_course_divisions()

        if divisions:
            # Update each word box with the courses for each semester
            for i, division in enumerate(divisions):
                course_names = [course.course_name for course in division]
                self.semester_boxes[i].setPlainText('\n'.join(course_names))
        else:
            print("Unable to generate course divisions.")

    def export_data(self):
        pass


if __name__ == '__main__':
    app = QApplication([])
    window = LoginWindow()
    window.show()
    app.exec()
