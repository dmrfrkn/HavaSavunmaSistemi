import cv2
import numpy as np

# Kamera bağlantısı açma
cap = cv2.VideoCapture(0)
tracker_list = []  # Birden fazla tracker tutmak için liste
balloon_id = 0  # Her balona benzersiz ID atamak için sayaç

if not cap.isOpened():
    print("Kamera açılmadı!")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Kare alınamadı!")
        break
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)
    
    # Takip edilen balonları güncelle
    new_tracker_list = []
    for tracker, bid, initial_area, bx, by in tracker_list:
        success, bbox = tracker.update(frame)
        if success:
            x, y, w, h = [int(v) for v in bbox]
            area = w * h
            print(f"Balloon {bid} tracked at ({x},{y}) - Area: {area} pixels^2")
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, f"Balloon {bid}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            new_tracker_list.append((tracker, bid, initial_area, x, y))
    
    # Yeni balonları tespit et
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1.2, minDist=30, param1=50, param2=30, minRadius=10, maxRadius=100)
    
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            x, y, r = i
            
            # Renk filtresi uygula
            mask_circle = np.zeros_like(gray)
            cv2.circle(mask_circle, (x, y), r, 255, -1)
            mean_sat = np.mean(hsv[:, :, 1][mask_circle == 255])
            mean_val = np.mean(hsv[:, :, 2][mask_circle == 255])
            
            if mean_sat > 50 and mean_val > 50:
                x1, y1 = max(0, x - r), max(0, y - r)
                x2, y2 = min(frame.shape[1] - 1, x + r), min(frame.shape[0] - 1, y + r)
                new_bbox = (x1, y1, x2 - x1, y2 - y1)
                
                # Yeni bir balon mu?
                already_tracked = any(abs(x - bx) < 30 and abs(y - by) < 30 for _, _, _, bx, by in tracker_list)
                if not already_tracked:
                    tracker = cv2.TrackerCSRT_create()
                    tracker.init(frame, new_bbox)
                    balloon_id += 1
                    initial_area = (x2 - x1) * (y2 - y1)
                    new_tracker_list.append((tracker, balloon_id, initial_area, x, y))
    
    tracker_list = new_tracker_list  # Takip listesini güncelle
    
    cv2.imshow("Balloon Tracking", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
