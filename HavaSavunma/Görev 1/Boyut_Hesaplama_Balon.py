import cv2
import numpy as np

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
    
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)
    
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1.2, minDist=30, param1=50, param2=30, minRadius=10, maxRadius=100)
    
    if circles is not None:
        circles = np.uint16(np.around(circles))
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        for i in circles[0, :]:
            x, y, r = i
            
            # Dairenin içindeki bölgenin renk özelliklerini al
            mask = np.zeros(gray.shape, dtype=np.uint8)
            cv2.circle(mask, (x, y), r, 255, -1)
            
            mean_hue = np.mean(hsv[:, :, 0][mask == 255])  # Ortalama renk tonu
            mean_sat = np.mean(hsv[:, :, 1][mask == 255])  # Ortalama doygunluk
            mean_val = np.mean(hsv[:, :, 2][mask == 255])  # Ortalama parlaklık
            
            # Doygunluk ve parlaklık eşiğini belirleyerek balon olmayanları filtrele
            if mean_sat > 50 and mean_val > 50:  # Balonlar genellikle doygun ve parlaktır
                cv2.circle(frame, (x, y), r, (0, 255, 0), 2)  # Yeşil çember çiz
                cv2.putText(frame, f"Balloon: ({x},{y}) R: {r}", (x - 40, y - r - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    
    cv2.imshow("Balloon Detection", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
