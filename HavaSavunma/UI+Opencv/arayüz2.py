import sys
import socket
import pickle
import base64
import cv2
import numpy as np
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer, pyqtSignal

class CameraGUI(QWidget):
    data_received = pyqtSignal(dict)  # PyQt sinyali

    def __init__(self):
        super().__init__()
        self.initUI()
        self.start_socket()
        self.data_received.connect(self.update_camera)

    def initUI(self):
        self.setWindowTitle("Camera Interface")
        self.setGeometry(100, 100, 900, 500)

        self.layout = QVBoxLayout()
        self.camera_view = QLabel("Camera View")
        self.layout.addWidget(self.camera_view)
        self.setLayout(self.layout)

    def start_socket(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect(("localhost", 55555))
            print("Bağlantı kuruldu!")

            self.thread = threading.Thread(target=self.receive_data, daemon=True)
            self.thread.start()
        except Exception as e:
            print(f"Socket bağlantı hatası: {e}")

    def receive_data(self):
        while True:
            try:
                print("1 - Veri alınıyor...")
                data = b""
                while True:
                    packet = self.client_socket.recv(4096)
                    if not packet:
                        break
                    data += packet
                print(f"2 - Veri alındı, boyut: {len(data)} bayt")

                received_data = pickle.loads(data)
                print("3 - Veri çözüldü, GUI güncellenecek...")
                self.data_received.emit(received_data)  # PyQt sinyali ile GUI'yi güncelle
            except Exception as e:
                print(f"Socket Hatası: {e}")
                break

    def update_camera(self, received_data):
        print("Veri alındı, arayüz güncelleniyor...")
        try:
            print("4 - Görüntü işleniyor...")
            img = base64.b64decode(received_data["image"])
            np_img = np.frombuffer(img, dtype=np.uint8)
            frame = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

            print("5 - Görüntü başarıyla koddan çözüldü...")
            for obj in received_data["objects"]:
                label, x, y, w, h = obj
                color = (255, 0, 0) if label == "Friend" else (0, 0, 255)
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

            print("6 - Nesneler çizildi, PyQt'ye aktarılıyor...")
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame.shape
            bytes_per_line = channel * width
            qimg = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            self.camera_view.setPixmap(QPixmap.fromImage(qimg))
            print("7 - Görüntü başarıyla ekrana basıldı!")
        except Exception as e:
            print(f"Görüntü işleme hatası: {e}")

    def closeEvent(self, event):
        self.client_socket.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CameraGUI()
    ex.show()
    sys.exit(app.exec_())
