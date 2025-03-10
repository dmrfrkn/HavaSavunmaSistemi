import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFrame


class ControlPanel(QWidget):
    def __init__(self):
        super().__init__()

        # Form Ayarları
        self.setWindowTitle("Hava Savunma Kontrol Paneli")
        self.setGeometry(100, 100, 800, 600)

        # Kamera Görüntüsü (placeholder)
        self.cameraView = QFrame(self)
        self.cameraView.setGeometry(20, 20, 300, 200)
        self.cameraView.setStyleSheet("border: 1px solid black;")

        # Açılar
        self.fireAngleLabel = QLabel("Ateş Açısı", self)
        self.fireAngleText = QLineEdit(self)

        self.moveAngleLabel = QLabel("Hareket Açısı", self)
        self.moveAngleText = QLineEdit(self)

        # Görev Butonları
        self.task1Button = QPushButton("Görev 1", self)
        self.task2Button = QPushButton("Görev 2", self)
        self.task3Button = QPushButton("Görev 3", self)

        # Log Alanı
        self.logLabel = QLabel("Loglar:", self)

        # Durum Panelleri
        self.cameraStatus = QLabel(self)
        self.cameraStatus.setGeometry(400, 20, 20, 20)
        self.cameraStatus.setStyleSheet("background-color: red;")

        self.systemStatus = QLabel(self)
        self.systemStatus.setGeometry(440, 20, 20, 20)
        self.systemStatus.setStyleSheet("background-color: red;")

        # Bullet Count
        self.bulletCountLabel = QLabel("Mermi: 0", self)

        # Layout Ayarları
        self.init_ui()

    def init_ui(self):
        # Açılar için Layout
        angleLayout = QVBoxLayout()
        angleLayout.addWidget(self.fireAngleLabel)
        angleLayout.addWidget(self.fireAngleText)
        angleLayout.addWidget(self.moveAngleLabel)
        angleLayout.addWidget(self.moveAngleText)

        # Butonlar için Layout
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.task1Button)
        buttonLayout.addWidget(self.task2Button)
        buttonLayout.addWidget(self.task3Button)

        # Durum ve Bullet Count Layout
        statusLayout = QVBoxLayout()
        statusLayout.addWidget(self.cameraStatus)
        statusLayout.addWidget(self.systemStatus)
        statusLayout.addWidget(self.bulletCountLabel)

        # Ana Layout
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.cameraView)
        mainLayout.addLayout(angleLayout)
        mainLayout.addLayout(buttonLayout)
        mainLayout.addWidget(self.logLabel)
        mainLayout.addLayout(statusLayout)

        self.setLayout(mainLayout)

    def update_status(self):
        # Durum panellerini değiştirme
        current_camera_status = self.cameraStatus.styleSheet()
        current_system_status = self.systemStatus.styleSheet()

        if "red" in current_camera_status:
            self.cameraStatus.setStyleSheet("background-color: green;")
        else:
            self.cameraStatus.setStyleSheet("background-color: red;")

        if "red" in current_system_status:
            self.systemStatus.setStyleSheet("background-color: green;")
        else:
            self.systemStatus.setStyleSheet("background-color: red;")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    panel = ControlPanel()
    panel.show()
    sys.exit(app.exec_())
