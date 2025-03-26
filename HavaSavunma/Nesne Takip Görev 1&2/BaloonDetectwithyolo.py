import cv2
from ultralytics import YOLO

model = YOLO("HavaSavunma/Nesne Takip Görev 1&2/HavaSavunmaBest.pt")

print("Model yüklendi.")
cap = cv2.VideoCapture(0)
print("Kamera baslatildi.")
while True:
    ret, frame = cap.read()
    if not ret:
        print("Kamera kaynagi okunamadi!")
        break
    results = model(frame)

    for result in results:
        boxes = result.boxes.xyxy.cpu().numpy()  # x_min, y_min, x_max, y_max
        class_ids = result.boxes.cls.cpu().numpy()  # Class IDs

        for box,  class_id in zip(boxes,  class_ids):
            x_min, y_min, x_max, y_max = map(int, box)

            if class_id == 0: 
                color = (0, 255, 0)  
                label = f"Friend"
            elif class_id == 1:  # 
                color = (0, 0, 255)  
                label = f"Enemy"
            else:
                color = (255, 255, 255)  
                label = f"Unknow"

            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), color, 2)
            cv2.putText(frame, label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    cv2.imshow("YOLOv8 Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
