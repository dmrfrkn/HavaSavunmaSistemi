import cv2
import numpy as np

def detect_balloon(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print("Görsel yüklenemedi!")
        return

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Kırmızı ve Mavi renk aralıkları
    lower_blue, upper_blue = np.array([90, 50, 50]), np.array([130, 255, 255])
    lower_red1, upper_red1 = np.array([0, 120, 70]), np.array([10, 255, 255])
    lower_red2, upper_red2 = np.array([170, 120, 70]), np.array([180, 255, 255])

    # Renk maskeleri oluştur
    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
    red_mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    red_mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    red_mask = cv2.bitwise_or(red_mask1, red_mask2)

    # Gürültü temizleme
    kernel = np.ones((5, 5), np.uint8)
    blue_mask = cv2.morphologyEx(blue_mask, cv2.MORPH_OPEN, kernel)
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel)

    # Konturları bul
    contours_blue, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_red, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    smallest_balloon = None

    for contour in contours_blue + contours_red:
        if cv2.contourArea(contour) > 500:
            x, y, w, h = cv2.boundingRect(contour)
            area = w * h
            
            # En küçük balonu bul
            if smallest_balloon is None or area < smallest_balloon[0]:
                smallest_balloon = (area, (x, y, w, h))
            
            color = (255, 0, 0) if contour in contours_blue else (0, 0, 255)
            cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)

    if smallest_balloon:
        x, y, w, h = smallest_balloon[1]
        print(f"En küçük balonun alanı: {smallest_balloon[0]} px²")
        print(f"Koordinatlar: (x: {x}, y: {y})")

   
    cv2.imshow("Balon Algılama", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Çalıştır
detect_balloon("c:/Users/CumFur/Desktop/cc.png")
