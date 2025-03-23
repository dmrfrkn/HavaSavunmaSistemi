import cv2
import numpy as np

image_path = "c:/Users/CumFur/Desktop/aa.png"

image = cv2.imread(image_path)
if image is None:
    print("Resim yüklenemedi! Lütfen dosya yolunu kontrol edin.")
    exit()

hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

lower_blue = np.array([90, 50, 50])
upper_blue = np.array([130, 255, 255])

lower_red1 = np.array([0, 120, 70])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([170, 120, 70])
upper_red2 = np.array([180, 255, 255])

blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

red_mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
red_mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
red_mask = cv2.bitwise_or(red_mask1, red_mask2)

kernel = np.ones((5, 5), np.uint8)
blue_mask = cv2.morphologyEx(blue_mask, cv2.MORPH_OPEN, kernel)
red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel)

contours_blue, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours_red, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

small_baloon = None  # Küçük balonu saklayacak değişken

# İki balonun da alanlarını karşılaştırarak küçük olanı belirleme
for contour in contours_blue:
    if cv2.contourArea(contour) > 500:  # Küçük gürültüleri engelle
        x, y, w, h = cv2.boundingRect(contour)
        
        area = w * h
        print(f"Blue Area: {area} px") 
        
        if small_baloon is None or area < small_baloon[0]:  
            small_baloon = (area, "Blue") 

        
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
        
for contour in contours_red:
    if cv2.contourArea(contour) > 500:
        x, y, w, h = cv2.boundingRect(contour)
        
        area = w * h
        print(f"Red Area: {area} px") 
    
        if small_baloon is None or area < small_baloon[0]:  
            small_baloon = (area, "Red")  

      
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)


if small_baloon:
    print(f"Small Baloon: {small_baloon[1]} baloon with Area: {small_baloon[0]} px")


cv2.imshow("Balon Algilama", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
