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
    QFileDialog,
    QComboBox
    )
from PySide6.QtGui import QPixmap
from directed_acyclic_graph import DAG
from courses_topological_division import generate_course_divisions
import json

max_credits_per_semester = []
courses_to_reschedule = []

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set login window appearances
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
        
        # Load users data from json file
        self.users = self.load_users()
    
    def load_users(self):
        try:
            with open('users.json', 'r') as file:
                data = json.load(file)
                return data['users']
        except FileNotFoundError:
            QMessageBox.warning(self, "错误", "用户数据文件未找到！")
            return []
        except json.JSONDecodeError:
            QMessageBox.warning(self, "错误", "用户数据文件格式错误！")
            return []

    def on_login_clicked(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if any(user['username'] == username and user['password'] == password for user in self.users):
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
        
        # Adjust button
        self.adjust_button = QPushButton("调整排课")
        button_layout.addWidget(self.adjust_button)
        self.adjust_button.clicked.connect(self.adjust_division)

        # Export button
        self.export_button = QPushButton("导出排课")
        button_layout.addWidget(self.export_button)
        self.export_button.clicked.connect(self.export_data)
        
        # Read arrangement
        self.read_arrangement_button = QPushButton("读入排布")
        button_layout.addWidget(self.read_arrangement_button)
        self.read_arrangement_button.clicked.connect(self.read_arrangement)
        
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
        
        # Data directory
        self.selected_json_file = ""
        
        # DAG
        self.dag = DAG()

    def import_data(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "打开文件", "", "JSON 文件 (*.json)")
        if not file_name:
            return  # 用户取消了操作
        
        # 判断是否是computer science courses
        try:
            with open(file_name, 'r') as file:
                data = json.load(file)
                if "computer_science_courses" not in data:
                    QMessageBox.warning(self, "错误", "JSON 文件格式错误，缺少 'computer_science_courses' 键。")
                    return
        except json.JSONDecodeError:
            QMessageBox.warning(self, "错误", "无法解析 JSON 文件。")
            return
        except FileNotFoundError:
            QMessageBox.warning(self, "错误", "文件未找到。")
            return
        
        self.selected_json_file = file_name
        QMessageBox.information(self, "文件选中", "文件已成功选中。")

    def generate_division(self):
        # No input file error
        if self.selected_json_file == "":
            QMessageBox.warning(self, "生成失败", "没有选择课程数据文件！")
            return
        
        dialog = MaxCreditDialog(self)
        if dialog.exec() == QDialog.Accepted:
            global max_credits_per_semester
            max_credits_per_semester = dialog.get_max_credits()
        
            divisions, error = generate_course_divisions(max_credits_per_semester, self.selected_json_file)

            if error:
                QMessageBox.warning(self, "排课错误", error)
                return
            
            if divisions:
                # Clear all the previous result
                for box in self.semester_boxes:
                    box.clear()
                # Update each word box with the courses for each semester
                for i, division in enumerate(divisions):
                    course_names = [course.course_name for course in division]
                    self.semester_boxes[i].setPlainText('，'.join(course_names))
            else:
                print("Unable to generate course divisions.")

    def adjust_division(self):
        divisions = []
        no_division_yet = True
        
        for box in self.semester_boxes:
            if box.toPlainText().strip():
                no_division_yet = False
                break
        
        if no_division_yet:
            # Error if all word boxes are empty
            QMessageBox.warning(self, "错误", "当前没有划分，请先生成课程划分！")
            return
        
        for box in self.semester_boxes:
            content = box.toPlainText().strip()
            courses = content.split('，') if content else []
            divisions.append(courses)
            
        dialog = AdjustCourseDialog(divisions)
        if dialog.exec() == QDialog.Accepted:
            new_divisions, error = dialog.rescheduleCourse()
            
            if error:
                QMessageBox.warning(self, "排课错误", error)
                return
            
            if new_divisions:
                # Clear all the previous result
                for box in self.semester_boxes:
                    box.clear()
                # Update each word box with the courses for each semester
                for i, division in enumerate(new_divisions):
                    if i < len(self.semester_boxes):
                        course_names = [course.course_name for course in division]
                        self.semester_boxes[i].setPlainText('，'.join(course_names))
                    else:
                        break
            else:
                print("Unable to generate course divisions.")
            
            
    
    def export_data(self):
        # 检查所有的 semester_boxes 是否都是空的
        if all(not box.toPlainText().strip() for box in self.semester_boxes):
            QMessageBox.warning(self, "导出失败", "没有课程数据可导出。")
            return
        
        # 选择保存文件的位置
        file_name, _ = QFileDialog.getSaveFileName(self, "保存文件", "", "文本文件 (*.txt)")
        if not file_name:
            return  # 用户取消了保存

        try:
            with open(file_name, 'w', encoding='utf-8') as file:
                for i, semester_box in enumerate(self.semester_boxes, start=1):
                    courses = semester_box.toPlainText().strip()
                    if courses:
                        file.write(f"第{i}学期:\n{courses}\n\n")
                
                # 追加调整过的课程和对应的学期
                if courses_to_reschedule:
                    file.write("\n调整过的课程:\n")
                    for course, semester in courses_to_reschedule:
                        file.write(f"{course} - 第{semester}学期\n")
                
                if max_credits_per_semester:
                    file.write("\n每学期最大课时数:\n")
                    for i, credits in enumerate(max_credits_per_semester, start=1):
                        file.write(f"第{i}学期: {credits}课时\n")
                        
            QMessageBox.information(self, "导出成功", "课程安排已成功导出到文本文件。")
        except Exception as e:
            QMessageBox.warning(self, "导出失败", f"导出过程中发生错误: {e}")
    
    def read_arrangement(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "打开文件", "", "文本文件 (*.txt)")
        if not file_name:
            return  # 用户取消了操作

        try:
            with open(file_name, 'r', encoding='utf-8') as file:
                lines = file.readlines()

            # 重置 semester_boxes 和 courses_to_reschedule
            for box in self.semester_boxes:
                box.clear()
            global courses_to_reschedule, max_credits_per_semester
            courses_to_reschedule = []
            max_credits_per_semester = []

            # 读入排布
            current_semester = -10
            max_credits_mode = False
            for line in lines:
                line = line.strip()
                if line.startswith("第") and line.endswith("学期:"):
                    current_semester = int(line[1:-3]) - 1
                elif line and current_semester >= 0 and current_semester < len(self.semester_boxes):
                    self.semester_boxes[current_semester].append(line)
                    current_semester = -10
                elif line.startswith("调整过的课程:"):
                    current_semester = -1  # 进入调整课程模式
                elif line.startswith("每学期最大课时数:"):
                    max_credits_mode = True  # 进入最大学分模式
                elif max_credits_mode:
                    if line:
                        parts = line.split(': ')
                        if len(parts) == 2:
                            semester, credits_str = parts
                            credits = int(credits_str[0:2])
                            max_credits_per_semester.append(credits)
                elif current_semester == -1:
                    parts = line.split(' - 第')
                    if len(parts) == 2:
                        course, semester_str = parts
                        semester = int(semester_str[0])
                        courses_to_reschedule.append((course, semester))
            
            if max_credits_mode == False:
                QMessageBox.warning(self, "错误", "缺少最大学分数！")
                return
            
            # 重建 DAG 并重新生成拓扑划分
            self.dag = DAG()
            self.dag.add_courses_from_json("courses.json")
            for course_name, semester in courses_to_reschedule:
                # 找到对应的课程对象
                course_to_set = next((c for c in self.dag.get_nodes() if c.course_name == course_name), None)
                if course_to_set:
                    # 设置课程的学期
                    course_to_set.set_semester(semester)
                else:
                    print(f"Course '{course_name}' not found in DAG")
            divisions, error = self.dag.topological_division_adjusting_courses(max_credits_per_semester)
            
            if error:
                QMessageBox.warning(self, "重建排课错误", error)
            else:
                # 更新 semester_boxes
                for i, division in enumerate(divisions):
                    course_names = [course.course_name for course in division]
                    self.semester_boxes[i].setPlainText('，'.join(course_names))

        except Exception as e:
            QMessageBox.warning(self, "读入失败", f"读入过程中发生错误: {str(e)}")
    
    def clearAllWordBoxes(self):
        # 清空文字框
        for box in self.semester_boxes:
            box.clear()
        
        # 清空每学期最大学分数
        max_credits_per_semester = []
        
        # 调整课程清空
        courses_to_reschedule = []

class MaxCreditDialog(QDialog):
    def __init__(self, parent=None):
        super(MaxCreditDialog, self).__init__(parent)
        self.setWindowTitle("设置每学期最大课时数")

        self.credit_comboboxes = []
        main_layout = QVBoxLayout()

        for i in range(1, 9):
            hbox = QHBoxLayout()
            label = QLabel(f"第{i}学期最大课时数：")
            combobox = QComboBox()
            for j in range(16, 25):  # credit ranges from 16 to 25
                combobox.addItem(str(j))
            self.credit_comboboxes.append(combobox)
            hbox.addWidget(label)
            hbox.addWidget(combobox)
            main_layout.addLayout(hbox)

        # Buttons
        self.confirmButton = QPushButton("确定")
        self.confirmButton.clicked.connect(self.accept)
        self.cancelButton = QPushButton("取消")
        self.cancelButton.clicked.connect(self.reject)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.confirmButton)
        button_layout.addWidget(self.cancelButton)

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def get_max_credits(self):
        return [int(combobox.currentText()) for combobox in self.credit_comboboxes]

class AdjustCourseDialog(QDialog):
    def __init__(self, divisions, parent=None):
        super(AdjustCourseDialog, self).__init__(parent)
        
        self.dag = DAG()
        self.dag.add_courses_from_json("courses.json")

        self.setWindowTitle("调整排课")
        self.divisions = divisions

        # Create labels and combo boxes
        self.label = QLabel("请选择课程")
        self.semesterComboBox = QComboBox()
        self.courseComboBox = QComboBox()
        self.targetSemesterComboBox = QComboBox()

        # Default options for combo boxes
        self.semesterComboBox.addItem("--学期--")
        self.courseComboBox.addItem("--课程--")
        self.targetSemesterComboBox.addItem("--目标学期--")

        # Fill the semester combobox
        for i in range(1, 9):
            self.semesterComboBox.addItem(f"第{i}学期")

        # Signal of semesterComboBox
        self.semesterComboBox.currentIndexChanged.connect(self.onSemesterChanged)
        
        # Create the confirm and cancel button
        self.confirmButton = QPushButton("确定")
        self.confirmButton.clicked.connect(self.accept)
        self.cancelButton = QPushButton("取消")
        self.cancelButton.clicked.connect(self.reject)

        # layout
        comboboxLayout = QHBoxLayout()
        comboboxLayout.addWidget(self.semesterComboBox)
        comboboxLayout.addWidget(self.courseComboBox)
        comboboxLayout.addWidget(self.targetSemesterComboBox)
        
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.confirmButton)
        buttonLayout.addWidget(self.cancelButton)
        
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.label)
        mainLayout.addLayout(comboboxLayout)
        mainLayout.addLayout(buttonLayout)        
        
        self.setLayout(mainLayout)

    def onSemesterChanged(self, index):
        # 清空课程下拉框并重新填充
        self.courseComboBox.clear()
        self.courseComboBox.addItem("--课程--")
        if index > 0 and index <= len(self.divisions):
            for course in self.divisions[index - 1]:
                self.courseComboBox.addItem(course)
        
        # 填充目标学期下拉框
        for i in range(1, 9):
            self.targetSemesterComboBox.addItem(f"第{i}学期")
            
    def set_course_semester(self, course_name, new_semester):
        course_to_set = next((c for c in self.dag.get_nodes() if c.course_name == course_name), None)
        if course_to_set:
            course_to_set.set_semester(new_semester)
        else:
            raise ValueError(f"Course {course_name} not found")
          
    def rescheduleCourse(self):
        # -1是因为前面有默认值
        current_semester = self.semesterComboBox.currentIndex()
        target_semester = self.targetSemesterComboBox.currentIndex()
        course_to_reschedule = self.courseComboBox.currentText()
        courses_to_reschedule.append((course_to_reschedule, target_semester))
        # 如果选择默认值则报错
        if current_semester < 1 or target_semester < 1 or course_to_reschedule == "--课程--":
            QMessageBox.warning(self, "错误", "请选择有效的学期和课程")
            return None, None
        
        try:
            # 更新调整课程的学期属性
            for course_name, target_semester in courses_to_reschedule:
                self.set_course_semester(course_name, target_semester)
            
            # 重新拓扑排序
            new_divisions, error = self.dag.topological_division_adjusting_courses(max_credits_per_semester)
            
            return new_divisions, error
            
        except Exception as e:
            QMessageBox.warning(self, "调整失败", f"调整课程时发生错误: {str(e)}")
            return None, str(e)
            
        
        
if __name__ == '__main__':
    app = QApplication([])
    window = LoginWindow()
    window.show()
    app.exec()
