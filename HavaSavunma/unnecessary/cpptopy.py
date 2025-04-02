import cv2
import numpy as np

# Check if CUDA is available
cuda_enabled = cv2.cuda.getCudaEnabledDeviceCount() > 0
if cuda_enabled:
    print("CUDA is enabled")
else:
    print("CUDA is not enabled")

# Open default camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open video capture device.")
    exit()

# Create morphological filter
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))

# Define color ranges
lower_red1, upper_red1 = (0, 70, 70), (10, 255, 255)
lower_red2, upper_red2 = (160, 70, 70), (179, 255, 255)
lower_blue, upper_blue = (100, 70, 70), (130, 255, 255)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame from video capture.")
        break
    
    if cuda_enabled:
        # Upload to GPU
        gpu_frame = cv2.cuda_GpuMat()
        gpu_frame.upload(frame)
        
        # Apply Gaussian blur
        gaussian_filter = cv2.cuda.createGaussianFilter(gpu_frame.type(), gpu_frame.type(), (7, 7), 0)
        gpu_frame = gaussian_filter.apply(gpu_frame)
        
        # Convert to HSV
        gpu_hsv = cv2.cuda.cvtColor(gpu_frame, cv2.COLOR_BGR2HSV)
        
        # Red mask
        gpu_red_mask1 = cv2.cuda.inRange(gpu_hsv, lower_red1, upper_red1)
        gpu_red_mask2 = cv2.cuda.inRange(gpu_hsv, lower_red2, upper_red2)
        gpu_red_mask = cv2.cuda.add(gpu_red_mask1, gpu_red_mask2)
        
        # Blue mask
        gpu_blue_mask = cv2.cuda.inRange(gpu_hsv, lower_blue, upper_blue)
        
        # Morphological opening
        morph_filter = cv2.cuda.createMorphologyFilter(cv2.MORPH_OPEN, cv2.CV_8U, kernel)
        gpu_red_mask = morph_filter.apply(gpu_red_mask)
        gpu_blue_mask = morph_filter.apply(gpu_blue_mask)
        
        # Download to CPU
        red_mask = gpu_red_mask.download()
        blue_mask = gpu_blue_mask.download()
    else:
        # Process on CPU if CUDA is not available
        frame_blur = cv2.GaussianBlur(frame, (7, 7), 0)
        hsv = cv2.cvtColor(frame_blur, cv2.COLOR_BGR2HSV)
        red_mask1 = cv2.inRange(hsv, np.array(lower_red1), np.array(upper_red1))
        red_mask2 = cv2.inRange(hsv, np.array(lower_red2), np.array(upper_red2))
        red_mask = cv2.add(red_mask1, red_mask2)
        blue_mask = cv2.inRange(hsv, np.array(lower_blue), np.array(upper_blue))
        red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel)
        blue_mask = cv2.morphologyEx(blue_mask, cv2.MORPH_OPEN, kernel)
    
    # Clone frame for debugging overlay
    debug_overlay = frame.copy()
    
    # Find and draw contours
    for mask, color1, color2 in [(red_mask, (0, 255, 255), (0, 255, 0)), (blue_mask, (255, 255, 0), (255, 0, 0))]:
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < frame.shape[0] * frame.shape[1] * 0.01:
                continue
            (x, y), radius = cv2.minEnclosingCircle(contour)
            center = (int(x), int(y))
            radius = int(radius)

            
            if radius > 0:
                cv2.circle(debug_overlay, center, radius, color1, 2)
                if area >= 0.65 * radius * radius * np.pi:
                    cv2.circle(debug_overlay, center, radius, color2, 2)
    
    # Show output
    cv2.imshow("BalloonDetection", debug_overlay)
    if cv2.waitKey(1) >= 0:
        break

cap.release()
cv2.destroyAllWindows()
