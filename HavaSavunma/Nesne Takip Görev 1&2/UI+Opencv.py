import sys
import cv2
import numpy as np
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
        self.shooting_mode = "Tekli Atış"
    
    def initUI(self):
        self.setWindowTitle("Camera Interface")
        self.setGeometry(100, 100, 900, 500)
        
        grid = QGridLayout()
        
        # Camera View
        self.camera_view = QLabel("Camera View")
        self.camera_view.setStyleSheet("border: 2px solid black; font-size: 16px;")
        self.camera_view.setFixedSize(480, 240)
        grid.addWidget(self.camera_view, 0, 0, 1, 2)
        
        # Right Panel
        right_panel = QVBoxLayout()
        
        # Logs
        self.logs = QTextEdit()
        self.logs.setPlaceholderText("Sistem logları burada gözükecek")
        self.logs.setReadOnly(True)
        right_panel.addWidget(self.logs)
        
        grid.addLayout(right_panel, 0, 2, 2, 1)
        
        self.setLayout(grid)
    
    def update_camera(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.detect_blue_objects(frame)
            height, width, channel = frame.shape
            bytes_per_line = channel * width
            qimg = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            self.camera_view.setPixmap(QPixmap.fromImage(qimg))
    
    def detect_blue_objects(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
        lower_blue = np.array([100, 150, 50])
        upper_blue = np.array([140, 255, 255])
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 500:  # Küçük gürültüleri önlemek için filtreleme
                self.logs.append(f"Mavi cisim algılandı - Alan: {int(area)} piksel")
    
    def closeEvent(self, event):
        self.cap.release()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CameraGUI()
    ex.show()
    sys.exit(app.exec_())
