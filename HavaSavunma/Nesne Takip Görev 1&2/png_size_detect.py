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
        self.process_image("c:/Users/CumFur/Desktop/cc.png")  # PNG dosyasını işle
    
    def initUI(self):
        self.setWindowTitle("Camera Interface")
        self.setGeometry(100, 100, 900, 500)
        
        grid = QGridLayout()
        
        # Görüntü Alanı
        self.image_view = QLabel("Image View")
        self.image_view.setStyleSheet("border: 2px solid black;")
        self.image_view.setFixedSize(480, 320)
        grid.addWidget(self.image_view, 0, 0, 1, 2)
        
        # Log Ekranı
        self.logs = QTextEdit()
        self.logs.setPlaceholderText("Sistem logları burada gözükecek")
        self.logs.setReadOnly(True)
        grid.addWidget(self.logs, 1, 0, 1, 2)
        
        # Açılar
        self.shooting_angle = QLabel("Ateş Açısı: -")
        self.motion_angle = QLabel("Hareket Açısı: -")
        grid.addWidget(self.shooting_angle, 2, 0)
        grid.addWidget(self.motion_angle, 2, 1)
        
        self.setLayout(grid)
    
    def process_image(self, image_path):
        image = cv2.imread(image_path)
        if image is None:
            self.logs.append("Görsel yüklenemedi!")
            return
        
        image, smallest_balloon, yaw, pitch = self.detect_balloon(image)
        if smallest_balloon:
            self.logs.append(f"Tespit edilen balon: {smallest_balloon[1]} ({smallest_balloon[0]} px) - Koordinatlar: {smallest_balloon[2]}")
            self.shooting_angle.setText(f"Ateş Açısı: {yaw:.2f}°")
            self.motion_angle.setText(f"Hareket Açısı: {pitch:.2f}°")
        
        # Görseli QLabel içinde gösterme
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width, channel = image.shape
        qimg = QImage(image.data, width, height, channel * width, QImage.Format_RGB888)
        self.image_view.setPixmap(QPixmap.fromImage(qimg))
    
    def detect_balloon(self, image):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower_blue, upper_blue = np.array([90, 50, 50]), np.array([130, 255, 255])
        lower_red1, upper_red1 = np.array([0, 120, 70]), np.array([10, 255, 255])
        lower_red2, upper_red2 = np.array([170, 120, 70]), np.array([180, 255, 255])
        
        blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
        red_mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        red_mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        red_mask = cv2.bitwise_or(red_mask1, red_mask2)
        
        kernel = np.ones((5, 5), np.uint8)
        blue_mask = cv2.morphologyEx(blue_mask, cv2.MORPH_OPEN, kernel)
        red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel)
        
        contours_blue, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours_red, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        smallest_balloon = None
        center_x, center_y = image.shape[1] // 2, image.shape[0] // 2
        
        for contour in contours_blue + contours_red:
            if cv2.contourArea(contour) > 500:
                x, y, w, h = cv2.boundingRect(contour)
                area = w * h
                
                if smallest_balloon is None or area < smallest_balloon[0]:
                    smallest_balloon = (area, "Blue" if contour in contours_blue else "Red", (x, y))
                
                cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0) if contour in contours_blue else (0, 0, 255), 2)
        
        if smallest_balloon:
            x, y = smallest_balloon[2]
            yaw = (x - center_x) / center_x * 45  # -45° ile +45° arası normalleştir
            pitch = (y - center_y) / center_y * 30  # -30° ile +30° arası normalleştir
            return image, smallest_balloon, yaw, pitch
        
        return image, None, 0, 0

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CameraGUI()
    ex.show()
    sys.exit(app.exec_())