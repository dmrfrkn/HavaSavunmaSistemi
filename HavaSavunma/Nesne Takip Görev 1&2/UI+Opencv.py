import sys
import cv2
import numpy as np
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
        
        # Logs
        self.logs = QTextEdit()
        self.logs.setPlaceholderText("Sistem logları burada gözükecek")
        self.logs.setReadOnly(True)
        grid.addWidget(self.logs, 1, 0, 1, 2)
        
        self.setLayout(grid)
    
    def update_camera(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.flip(frame, 1)  # Aynalama (tercihe bağlı)
            processed_frame = self.detect_blue_objects(frame)

            # Görüntüyü arayüzde gösterme
            height, width, channel = processed_frame.shape
            bytes_per_line = channel * width
            qimg = QImage(processed_frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            self.camera_view.setPixmap(QPixmap.fromImage(qimg))
    
    def detect_blue_objects(self, frame):
        """Mavi cisimleri tespit eder ve alanlarını log ekranına yazdırır."""
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Mavi renk için HSV aralığı
        lower_blue = np.array([90, 50, 50])
        upper_blue = np.array([130, 255, 255])
        mask = cv2.inRange(hsv, lower_blue, upper_blue)

        # Konturları bulma
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        total_area = 0
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 500:  # Küçük parazitleri yok sayma
                total_area += area
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Yeşil çerçeve çiz

        # Alanı log ekranına yazdır
        if total_area > 0:
            self.logs.append(f"Mavi cisim alanı: {total_area:.2f} piksel")

        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    def start_timer(self):
        self.time_remaining = 300
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)
    
    def update_timer(self):
        if self.time_remaining > 0:
            self.time_remaining -= 1
    
    def closeEvent(self, event):
        self.cap.release()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CameraGUI()
    ex.show()
    sys.exit(app.exec_())
