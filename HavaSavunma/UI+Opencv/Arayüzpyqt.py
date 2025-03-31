import sys
import socket
import pickle
import base64
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer

class CameraGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.start_socket()
        self.timer.start(30)

    def initUI(self):
        self.setWindowTitle("Camera Interface")
        self.setGeometry(100, 100, 900, 500)

        self.layout = QVBoxLayout()
        self.camera_view = QLabel("Camera View")
        self.layout.addWidget(self.camera_view)
        self.setLayout(self.layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_camera)

    def start_socket(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(("localhost", 55555))

    def update_camera(self):
        print("Veri alınıyor...")
    
        try:
            # Gelen veriyi al
            data = b""
            while True:
                packet = self.client_socket.recv(4096)
                if not packet:
                    break
                data += packet

            # Veriyi çözüp ekrana bastır
            received_data = pickle.loads(data)
            image_data = received_data["image"]
            objects = received_data["objects"]

            # Base64'ten OpenCV formatına çevir
            img = base64.b64decode(image_data)
            np_img = np.frombuffer(img, dtype=np.uint8)
            frame = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

            # Gelen verileri ekrana çiz
            for obj in objects:
                label, x, y, w, h = obj
                color = (255, 0, 0) if label == "Friend" else (0, 0, 255)
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

            # OpenCV görüntüsünü PyQt’ye aktar
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame.shape
            bytes_per_line = channel * width
            qimg = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            self.camera_view.setPixmap(QPixmap.fromImage(qimg))

        except Exception as e:
            print(f"Socket Hatası: {e}")

    def closeEvent(self, event):
        self.client_socket.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CameraGUI()
    ex.show()
    sys.exit(app.exec_())
