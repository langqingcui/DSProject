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
    QDialog,
    QComboBox
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

        self.setWindowTitle("课程编排系统-主界面")
        self.resize(800, 600)

        # Main horizontal layout
        main_layout = QHBoxLayout()

        # Button area layout
        button_layout = QVBoxLayout()
        button_layout.setSpacing(10)

        # Import button
        self.import_button = QPushButton("导入课程")
        button_layout.addWidget(self.import_button)
        self.import_button.clicked.connect(self.import_data)

        # Generate button
        self.generate_button = QPushButton("开始排课")
        button_layout.addWidget(self.generate_button)
        self.generate_button.clicked.connect(self.generate_division)

        # Export button
        self.export_button = QPushButton("导出排课")
        button_layout.addWidget(self.export_button)
        self.export_button.clicked.connect(self.export_data)
        
        # Clear button
        self.clear_button = QPushButton("清空排课")
        button_layout.addWidget(self.clear_button)
        self.clear_button.clicked.connect(self.clearAllWordBoxes)
        
        button_layout.addStretch()

        # Widget to hold the buttons
        button_widget = QWidget()
        button_widget.setLayout(button_layout)
        button_widget.setFixedWidth(100) 

        # Add the button layout to the main layout
        main_layout.addWidget(button_widget)

        # GroupBox for semester text areas
        semester_group_box = QGroupBox("学期")
        semester_layout = QVBoxLayout()

        # Text boxes for semesters
        self.semester_boxes = []
        for i in range(8):
            text_edit = QTextEdit()
            text_edit.setReadOnly(True)
            text_edit.setPlaceholderText(f"第{i+1}学期")
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
        dialog = MaxCreditDialog(self)
        result = dialog.exec()
        
        if result == QDialog.Accepted:
            max_credits = dialog.selected_credits()
        
            divisions = generate_course_divisions(max_credits)

            if divisions:
                # Update each word box with the courses for each semester
                for i, division in enumerate(divisions):
                    course_names = [course.course_name for course in division]
                    self.semester_boxes[i].setPlainText('，'.join(course_names))
            else:
                print("Unable to generate course divisions.")

    def export_data(self):
        pass
    
    def clearAllWordBoxes(self):
        for box in self.semester_boxes:
            box.clear()

class MaxCreditDialog(QDialog):
    def __init__(self, parent=None):
        super(MaxCreditDialog, self).__init__(parent)
        
        self.setWindowTitle("学分数")
        
        label = QLabel("每学期最大学分：")
        
        # Create the combo box that select max credits
        self.creditComboBox = QComboBox()
        for i in range(16, 36):  # Add credit options from 16 to 35
            self.creditComboBox.addItem(str(i))
            
        # Create the confirm and cancel button
        self.confirmButton = QPushButton("确定")
        self.confirmButton.clicked.connect(self.accept)
        self.cancelButton = QPushButton("取消")
        self.cancelButton.clicked.connect(self.reject)
        
        # Layout for the combo box and label
        comboLayout = QHBoxLayout()
        comboLayout.addWidget(label)
        comboLayout.addWidget(self.creditComboBox)
        
        # Layout for buttons
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.confirmButton)
        buttonLayout.addWidget(self.cancelButton)
        
        # Main layout
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(comboLayout)
        mainLayout.addLayout(buttonLayout)
        
        self.setLayout(mainLayout)

    def selected_credits(self):
        return int(self.creditComboBox.currentText())


if __name__ == '__main__':
    app = QApplication([])
    window = LoginWindow()
    window.show()
    app.exec()
