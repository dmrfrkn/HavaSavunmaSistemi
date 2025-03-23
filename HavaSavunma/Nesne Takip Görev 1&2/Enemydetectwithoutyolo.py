import cv2
import numpy as np
"c:\Users\CumFur\Desktop\Ekran görüntüsü 2025-03-23 222201.png"
video_path = "c:/Users/CumFur/Desktop/stock-footage-red-balloon-flying-in-blue-sky.webm"  
cap = cv2.VideoCapture(video_path)

lower_blue = np.array([90, 50, 50])    # Mavi için alt HSV değeri
upper_blue = np.array([130, 255, 255]) # Mavi için üst HSV değeri

lower_red1 = np.array([0, 120, 70])    # Kırmızı için alt HSV (ilk aralık)
upper_red1 = np.array([10, 255, 255])  # Kırmızı için üst HSV (ilk aralık)
lower_red2 = np.array([170, 120, 70])  # Kırmızı için alt HSV (ikinci aralık)
upper_red2 = np.array([180, 255, 255]) # Kırmızı için üst HSV (ikinci aralık)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break  
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

    red_mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    red_mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    red_mask = cv2.bitwise_or(red_mask1, red_mask2)

    kernel = np.ones((5, 5), np.uint8)
    blue_mask = cv2.morphologyEx(blue_mask, cv2.MORPH_OPEN, kernel)
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel)

    contours_blue, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_red, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours_blue:
        if cv2.contourArea(contour) > 500:  # Küçük gürültüleri engelle
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(frame, "Dost", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

    for contour in contours_red:
        if cv2.contourArea(contour) > 500:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(frame, "Düşman", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    cv2.imshow("BaloN Algılama", frame)

    if cv2.waitKey(30) & 0xFF == ord('q'):  # 'q' ile çıkış
        break

cap.release()
cv2.destroyAllWindows()
