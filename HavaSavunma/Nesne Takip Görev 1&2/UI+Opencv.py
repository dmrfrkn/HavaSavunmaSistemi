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
        self.load_image("c:/Users/CumFur/Desktop/cc.png")  # PNG dosyasını yükle
    
    def initUI(self):
        self.setWindowTitle("Camera Interface")
        self.setGeometry(100, 100, 900, 500)
        
        grid = QGridLayout()
        
        # Görüntü Alanı
        self.image_view = QLabel()
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
    
    def load_image(self, image_path):
        image = cv2.imread(image_path)
        if image is None:
            self.logs.append("Görsel yüklenemedi!")
            return
        
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width, channel = image.shape
        qimg = QImage(image.data, width, height, channel * width, QImage.Format_RGB888)
        self.image_view.setPixmap(QPixmap.fromImage(qimg))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CameraGUI()
    ex.show()
    sys.exit(app.exec_())
