import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout, QGridLayout, QComboBox, QLineEdit
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

class CameraGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.process_image("c:/Users/CumFur/Desktop/cc.png")
    
    def initUI(self):
        self.setWindowTitle("Camera Interface")
        self.setGeometry(100, 100, 1000, 600)
        
        main_layout = QGridLayout()
        
        # Kamera Görüntüsü
        self.image_view = QLabel()
        self.image_view.setFixedSize(300, 200)
        self.image_view.setStyleSheet("border: 2px solid black;")
        main_layout.addWidget(self.image_view, 0, 0, 1, 2)
        
        # Açılar
        self.shooting_range = QLabel("Ateş edebileceğimiz açı aralığı")
        self.motion_range = QLabel("Hareket edebileceğimiz açı aralığı")
        main_layout.addWidget(self.shooting_range, 1, 0)
        main_layout.addWidget(self.motion_range, 1, 1)
        
        # Log Ekranı
        self.logs = QTextEdit()
        self.logs.setPlaceholderText("Sistem logları burada gözükecek")
        self.logs.setReadOnly(True)
        main_layout.addWidget(self.logs, 0, 2, 2, 2)
        
        self.setLayout(main_layout)
    
    def process_image(self, image_path):
        image = cv2.imread(image_path)
        if image is None:
            self.logs.append("Görsel yüklenemedi!")
            return
        
        image, smallest_balloon, yaw, pitch = self.detect_balloon(image)
        if smallest_balloon:
            self.logs.append(f"Tespit edilen balon: {smallest_balloon[1]} - Koordinatlar: {smallest_balloon[2]}")
        
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width, channel = image.shape
        qimg = QImage(image.data, width, height, channel * width, QImage.Format_RGB888)
        self.image_view.setPixmap(QPixmap.fromImage(qimg))
    
    def detect_balloon(self, image):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower_red1, upper_red1 = np.array([0, 120, 70]), np.array([10, 255, 255])
        lower_red2, upper_red2 = np.array([170, 120, 70]), np.array([180, 255, 255])
        red_mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        red_mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        red_mask = cv2.bitwise_or(red_mask1, red_mask2)
        
        kernel = np.ones((5, 5), np.uint8)
        red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel)
        
        contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        smallest_balloon = None
        for contour in contours:
            if cv2.contourArea(contour) > 500:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
                if smallest_balloon is None or (w * h) < smallest_balloon[0]:
                    smallest_balloon = (w * h, "Red", (x, y))
        
        return image, smallest_balloon, 0, 0

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CameraGUI()
    ex.show()
    sys.exit(app.exec_())