import cv2
import numpy as np

# Önceki karelerde tespit edilen balonları saklamak için liste
tracked_balloons = []

# Kamera bağlantısı açma
cap = cv2.VideoCapture(0)

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
    
    # Gürültüyü azalt
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)
    
    # Dairesel nesneleri tespit et
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1.2, minDist=30, param1=50, param2=30, minRadius=10, maxRadius=100)
    
    new_tracked_balloons = []
    
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            x, y, r = i
            
            # Daha önce takip edilen balon mu?
            is_tracked = any(abs(x - bx) < 30 and abs(y - by) < 30 for bx, by, _ in tracked_balloons)
            if is_tracked:
                new_tracked_balloons.append((x, y, r))
                continue
            
            # Dairenin içindeki bölgenin renk özelliklerini al
            mask_circle = np.zeros_like(gray)
            cv2.circle(mask_circle, (x, y), r, 255, -1)
            mean_sat = np.mean(hsv[:, :, 1][mask_circle == 255])
            mean_val = np.mean(hsv[:, :, 2][mask_circle == 255])
            
            # Balon olup olmadığını kontrol et
            if mean_sat > 50 and mean_val > 50:
                x1, y1, x2, y2 = x - r, y - r, x + r, y + r
                area = (x2 - x1) * (y2 - y1)
                print(f"Balloon detected at ({x},{y}) - Area: {area} pixels^2")
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"Area: {area}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                new_tracked_balloons.append((x, y, r))
    
    tracked_balloons = new_tracked_balloons  # Takip edilen balonları güncelle
    
    cv2.imshow("Balloon Detection", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
