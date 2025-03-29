import cv2
import numpy as np
from ultralytics import YOLO

# Model yolunu yazın
model = YOLO("E:/Teknofest Sema İha Takımı/SEMAVSCODE/HavaSavunma/HavaSavunmaBest.pt")

# Kamerayı başlat
cap = cv2.VideoCapture(0)

# Takip için bir OpenCV MultiTracker oluştur
trackers = cv2.legacy.MultiTracker_create()

# Takip edilen nesnelerin etiketlerini tutmak için liste
target_labels = []

# YOLO tespitini kaç karede bir yapacağınızı belirleyin
frame_count = 0
DETECTION_INTERVAL = 15  # Her 30 karede bir YOLO tespiti yapılacak

while True:
    ret, frame = cap.read()
    if not ret:
        print("Kamera kaynagi okunamadi!")
        break

    frame_count += 1

    # Eğer YOLO tespiti yapılması gereken bir kareyse
    if frame_count % DETECTION_INTERVAL == 0:
        # Önceki takipçileri temizle
        trackers = cv2.legacy.MultiTracker_create()
        target_labels = []

        # YOLO modelinden sonuçları alın
        results = model(frame)

        for result in results:
            boxes = result.boxes.xyxy.cpu().numpy()  # x_min, y_min, x_max, y_max
            class_ids = result.boxes.cls.cpu().numpy()  # Class IDs

            for box, class_id in zip(boxes, class_ids):
                x_min, y_min, x_max, y_max = map(int, box)

                # Sınıf etiketlerini belirle
                if class_id == 0:  # "Dost" sınıfı
                    label = "Dost"
                elif class_id == 1:  # "Düşman" sınıfı
                    label = "Dusman"
                else:
                    label = "Bilinmeyen"

                # Dikdörtgeni takipçiye ekle
                tracker = cv2.legacy.TrackerCSRT_create()
                trackers.add(tracker, frame, (x_min, y_min, x_max - x_min, y_max - y_min))
                target_labels.append(label)

    # Takipçiyi güncelle
    success, boxes = trackers.update(frame)

    # Her bir nesneyi çiz
    for i, box in enumerate(boxes):
        x, y, w, h = map(int, box)
        label = target_labels[i]

        if label == "Dost":
            color = (0, 255, 0)  # Yeşil
        elif label == "Dusman":
            color = (0, 0, 255)  # Kırmızı
        else:
            color = (255, 255, 255)  # Beyaz

        # Dikdörtgen ve etiket çizin
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        cv2.putText(frame, label, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2) 

    # Görüntüyü göster
    cv2.imshow("YOLOv8 Detection with OpenCV Tracking", frame)

    # 'q' tuşuna basıldığında döngüden çık
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
