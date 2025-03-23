import cv2
import numpy as np
from ultralytics import YOLO

model = YOLO("E:\Teknofest Sema İha Takımı\SEMAVSCODE\HavaSavunma/balon.pt")  # Eğitilmiş modelin yolunu buraya yazın

cap = cv2.VideoCapture(0) 

while True:
    ret, frame = cap.read()
    if not ret:
        print("Kamera kaynagi okunamadi!")
        break

    results = model(frame)
    
    for result in results:
        boxes = result.boxes.xyxy.cpu().numpy()  
        scores = result.boxes.conf.cpu().numpy()  
        
        for box, score in zip(boxes, scores):
            x_min, y_min, x_max, y_max = map(int, box)

           
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
            label = f"Confidence: {score:.2f}"
            cv2.putText(frame, label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.imshow("YOLOv8 Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
