import cv2
import numpy as np

# Kamera bağlantısı açma (varsayılan kamera 0)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Kamera açılmadı!")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Kare alınamadı!")
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Mavi renk aralığı (HSV renk uzayında)
    lower_blue = np.array([90, 50, 50])
    upper_blue = np.array([130, 255, 255])

    # Mavi cisim için maske oluşturma
    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Gürültü azaltma işlemi
    kernel = np.ones((5, 5), np.uint8)
    blue_mask = cv2.morphologyEx(blue_mask, cv2.MORPH_OPEN, kernel)

    # Kontur tespiti
    contours_blue, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Mavi cisim için koordinatlar ve boyutlar
    for contour in contours_blue:
        if cv2.contourArea(contour) > 500:  # Küçük nesneleri engelle
            x, y, w, h = cv2.boundingRect(contour)
            area = w * h
            # Koordinatları ve boyutları ekrana yazdır
            cv2.putText(frame, f"Blue: ({x},{y}) Size: {w}x{h}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)  # Dikdörtgen çiz

    # Ekranda görüntüyü göster
    cv2.imshow("Camera - Blue Object Detection", frame)

    # 'q' tuşuna basılınca çık
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
