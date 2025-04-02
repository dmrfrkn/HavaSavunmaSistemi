import cv2
from ultralytics import YOLO

# Model yolunu yazın
model = YOLO("HavaSavunmaBest.pt").to("cuda")
print("Model yüklendi.")

# Kamerayı başlat
cap = cv2.VideoCapture(0)
print("Kamera başlatıldı.")

# Takip için bir OpenCV MultiTracker oluştur
trackers = cv2.legacy.MultiTracker_create()

# YOLO tespitini kaç karede bir yapacağınızı belirleyin
frame_count = 0
DETECTION_INTERVAL = 30  # Her 30 karede bir YOLO tespiti yapılacak

while True:
    ret, frame = cap.read()
    if not ret:
        print("Kamera kaynağı okunamadı!")
        break

    frame_count += 1

    # Eğer YOLO tespiti yapılması gereken bir kareyse
    if frame_count % DETECTION_INTERVAL == 0:
        # Önceki takipçileri temizle
        trackers = cv2.legacy.MultiTracker_create()

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
                    label = "Düşman"
                else:
                    label = "Bilinmeyen"

                # Dikdörtgeni takipçiye ekle
                tracker = cv2.legacy.TrackerCSRT_create()
                trackers.add(tracker, frame, (x_min, y_min, x_max - x_min, y_max - y_min))

    # Takipçiyi güncelle
    success, boxes = trackers.update(frame)

    # Her bir nesneyi çiz
    for box in boxes:
        x, y, w, h = map(int, box)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Görüntüyü göster
    cv2.imshow("YOLOv8 Detection with Tracking", frame)

    # 'q' tuşuna basıldığında döngüden çık
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
