import sys
import socket
import struct
import pickle
import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer

class CameraGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.start_timer()

        # Socket Client Setup
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(("127.0.0.1", 9999))  # OpenCV server ile bağlantı

        self.data = b""
        self.payload_size = struct.calcsize("L")

        self.timer_camera = QTimer(self)
        self.timer_camera.timeout.connect(self.update_camera)
        self.timer_camera.start(30)

    def initUI(self):
        self.setWindowTitle("Camera Interface")
        self.setGeometry(100, 100, 900, 500)

        # Camera View
        self.camera_view = QLabel("Camera View")
        self.camera_view.setStyleSheet("border: 2px solid black; font-size: 16px;")
        self.camera_view.setFixedSize(480, 240)

        layout = QVBoxLayout()
        layout.addWidget(self.camera_view)
        self.setLayout(layout)

    def update_camera(self):
        # Verileri al
        while len(self.data) < self.payload_size:
            packet = self.client_socket.recv(4096)
            if not packet:
                return
            self.data += packet

        # Mesaj boyutunu al
        packed_msg_size = self.data[:self.payload_size]
        self.data = self.data[self.payload_size:]
        msg_size = struct.unpack("L", packed_msg_size)[0]

        # Veriyi al
        while len(self.data) < msg_size:
            self.data += self.client_socket.recv(4096)

        frame_data = self.data[:msg_size]
        self.data = self.data[msg_size:]

        frame = pickle.loads(frame_data)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # PyQt'da görüntüye dönüştür
        h, w, ch = frame.shape
        bytes_per_line = ch * w
        qimg = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.camera_view.setPixmap(QPixmap.fromImage(qimg))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CameraGUI()
    ex.show()
    sys.exit(app.exec_())
