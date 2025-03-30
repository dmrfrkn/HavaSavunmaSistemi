import cv2
import numpy as np

cap = cv2.VideoCapture(0)
tracker = cv2.TrackerCSRT_create()  # CSRT Tracker kullanılıyor
tracking = False  # Takip durumunu belirleyen bayrak
bbox = None  # Takip edilen alan

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
    
    if not tracking:
        circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1.2, minDist=30, param1=50, param2=30, minRadius=10, maxRadius=100)
        
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                x, y, r = i
                
                mask_circle = np.zeros_like(gray)
                cv2.circle(mask_circle, (x, y), r, 255, -1)
                mean_sat = np.mean(hsv[:, :, 1][mask_circle == 255])
                mean_val = np.mean(hsv[:, :, 2][mask_circle == 255])
                
                if mean_sat > 50 and mean_val > 50:
                    x1, y1, x2, y2 = x - r, y - r, x + r, y + r
                    bbox = (x1, y1, x2 - x1, y2 - y1)
                    tracker.init(frame, bbox)  # Takibi başlat
                    tracking = True
                    break
    else:
        # Takibi devam ettir
        success, bbox = tracker.update(frame)
        if success:
            x, y, w, h = [int(v) for v in bbox]
            area = w * h
            print(f"Balloon tracked at ({x},{y}) - Area: {area} pixels^2")
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, f"Area: {area}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        else:
            tracking = False  # Eğer takip kaybolursa, tekrar algılama yap
    
    cv2.imshow("Balloon Tracking", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
