import sys
import cv2
import time
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout, QGridLayout, QComboBox, QLineEdit
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QTimer

class CameraGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.start_timer()
        self.cap = cv2.VideoCapture(0)
        self.timer_camera = QTimer(self)
        self.timer_camera.timeout.connect(self.update_camera)
        self.timer_camera.start(30)
    
    def initUI(self):
        self.setWindowTitle("Camera Interface")
        self.setGeometry(100, 100, 900, 500)
        
        grid = QGridLayout()
        
        # Camera View
        self.camera_view = QLabel("Camera View")
        self.camera_view.setStyleSheet("border: 2px solid black; font-size: 16px;")
        self.camera_view.setFixedSize(480, 240)
        grid.addWidget(self.camera_view, 0, 0, 1, 2)
        
        # Angle Ranges
        self.shooting_angle = QLabel("Ateş edebileceğimiz açı aralığı")
        self.shooting_angle.setStyleSheet("border: 1px solid black;")
        self.motion_angle = QLabel("Hareket edebileceğimiz açı aralığı")
        self.motion_angle.setStyleSheet("border: 1px solid black;")
        
        grid.addWidget(self.shooting_angle, 1, 0)
        grid.addWidget(self.motion_angle, 1, 1)
        
        # Right Panel
        right_panel = QVBoxLayout()
        
        # Mode Selection
        self.mode_label = QLabel("Mod Seçimi:")
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Manuel", "Otonom"])
        mode_layout = QHBoxLayout()
        mode_layout.addWidget(self.mode_label)
        mode_layout.addWidget(self.mode_combo)
        right_panel.addLayout(mode_layout)
        
        # Camera status
        self.camera_status = QLabel("Camera")
        self.camera_status.setStyleSheet("background-color: green; padding: 5px;")
        
        self.status_indicator = QLabel("Sistem Aktifliği")
        self.status_indicator.setStyleSheet("background-color: red; padding: 5px;")
        
        status_layout = QHBoxLayout()
        status_layout.addWidget(self.camera_status)
        status_layout.addWidget(self.status_indicator)
        
        right_panel.addLayout(status_layout)
        
        # Logs
        self.logs = QTextEdit()
        self.logs.setPlaceholderText("Sistem logları burada gözükecek")
        self.logs.setReadOnly(True)
        right_panel.addWidget(self.logs)
        
        # Task Buttons
        task_layout = QHBoxLayout()
        self.task1_btn = QPushButton("Görev 1")
        self.task2_btn = QPushButton("Görev 2")
        self.task3_btn = QPushButton("Görev 3")
        self.task1_btn.clicked.connect(lambda: self.log_task(1))
        self.task2_btn.clicked.connect(lambda: self.log_task(2))
        self.task3_btn.clicked.connect(lambda: self.log_task(3))
        
        task_layout.addWidget(self.task1_btn)
        task_layout.addWidget(self.task2_btn)
        task_layout.addWidget(self.task3_btn)
        right_panel.addLayout(task_layout)
        
        # Bullet Count and Timer
        self.bullet_count = QLabel("Bullet Count")
        self.timer_label = QLabel("Kalan süre: 300")
        
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.bullet_count)
        bottom_layout.addWidget(self.timer_label)
        right_panel.addLayout(bottom_layout)
        
        # Angle Limit Inputs
        self.shoot_angle_input = QLineEdit()
        self.shoot_angle_input.setPlaceholderText("Örn: -45, 45")
        self.move_angle_input = QLineEdit()
        self.move_angle_input.setPlaceholderText("Örn: 0, 270")
        
        angle_layout = QVBoxLayout()
        angle_layout.addWidget(QLabel("Ateş açısı sınırları:"))
        angle_layout.addWidget(self.shoot_angle_input)
        angle_layout.addWidget(QLabel("Hareket açısı sınırları:"))
        angle_layout.addWidget(self.move_angle_input)
        right_panel.addLayout(angle_layout)
        
        grid.addLayout(right_panel, 0, 2, 2, 1)
        
        self.setLayout(grid)
        
    def start_timer(self):
        self.time_remaining = 300
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)
    
    def update_timer(self):
        if self.time_remaining > 0:
            self.time_remaining -= 1
            self.timer_label.setText(f"Kalan süre: {self.time_remaining}")
        else:
            self.timer.stop()
    
    def update_camera(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame.shape
            bytes_per_line = channel * width
            qimg = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            self.camera_view.setPixmap(QPixmap.fromImage(qimg))
    
    def log_task(self, task_number):
        self.logs.append(f"Görev {task_number} başladı")

    def closeEvent(self, event):
        self.cap.release()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CameraGUI()
    ex.show()
    sys.exit(app.exec_())