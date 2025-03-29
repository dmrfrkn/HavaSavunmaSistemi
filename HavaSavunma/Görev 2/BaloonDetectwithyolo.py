import cv2
import torch
import numpy as np
from ultralytics import YOLO

# YOLO modelini yükle
model_path = "HavaSavunma/Görev 2/HavaSavunmaBest.pt"
model = YOLO(model_path)

def classify_balloon_by_color(image, bbox):
    """
    ROI'daki baskın rengi analiz ederek kırmızı mı yoksa mavi mi olduğunu belirler.
    """
    x1, y1, x2, y2 = map(int, bbox)
    roi = image[y1:y2, x1:x2]
    
    # BGR formatından HSV formatına çevir
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    
    # Kırmızı ve mavi için renk aralıklarını belirle
    lower_red1, upper_red1 = np.array([0, 120, 70]), np.array([10, 255, 255])
    lower_red2, upper_red2 = np.array([170, 120, 70]), np.array([180, 255, 255])
    lower_blue, upper_blue = np.array([100, 150, 50]), np.array([140, 255, 255])
    
    # Maskeleme işlemi
    mask_red = cv2.inRange(hsv, lower_red1, upper_red1) + cv2.inRange(hsv, lower_red2, upper_red2)
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    
    # Pikselleri sayarak hangi rengin daha fazla olduğunu belirle
    red_pixels = np.sum(mask_red > 0)
    blue_pixels = np.sum(mask_blue > 0)
    
    return "Düşman" if red_pixels > blue_pixels else "Dost"

# Kamerayı başlat (veya video dosyası kullan)
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    results = model(frame)
    
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            conf = box.conf[0].item()
            
            if conf > 0.5:  # Güven eşiği
                label = classify_balloon_by_color(frame, (x1, y1, x2, y2))
                color = (0, 0, 255) if label == "Düşman" else (255, 0, 0)
                
                # Dikdörtgen çiz ve etiketi ekle
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
                cv2.putText(frame, label, (int(x1), int(y1) - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    
    cv2.imshow("Hava Savunma Algılama", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
