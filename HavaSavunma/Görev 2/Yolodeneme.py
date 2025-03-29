import cv2
from ultralytics import YOLO

# YOLO modelini yükle
model_path = "HavaSavunma/Görev 1/HavaSavunmaBest.pt"
model = YOLO(model_path).to("cpu")  # Eğer GPU'n varsa "cuda" kullanabilirsin

# Kamerayı başlat (veya video dosyası kullan)
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue  # Çerçeve okunamazsa döngüye devam et
    
    frame = cv2.resize(frame, (640, 480))  # Çözünürlüğü küçült
    
    try:
        results = model(frame)
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                conf = box.conf[0].item()
                
                if conf > 0.5:  # Güven eşiği
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
    except Exception as e:
        print(f"Hata oluştu: {e}")
    
    cv2.imshow("YOLO Algılama", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
