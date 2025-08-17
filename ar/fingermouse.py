import cv2
import mediapipe as mp
import time
import math
import pyautogui
import numpy as np
from collections import deque

pyautogui.FAILSAFE = False


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)


mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mpDraw = mp.solutions.drawing_utils


try:
    import screeninfo
    monitors = screeninfo.get_monitors()
    total_screen_w = sum(m.width for m in monitors)
    total_screen_h = max(m.height for m in monitors)
except:
    total_screen_w, total_screen_h = pyautogui.size()
    total_screen_w *= 2  

clicking = False
pTime = 0


shrink_ratio_x = 0.3  
shrink_ratio_y = 0.5  
smoothing_factor = 10  
movement_threshold = 1  
speed_reduction = 0.5  

history_x = deque(maxlen=smoothing_factor)
history_y = deque(maxlen=smoothing_factor)


dead_zone = 0.1  
max_response = 0.9  


click_distance_threshold = 60  
click_cooldown = 0.2  
last_click_time = 0


pyautogui.PAUSE = 0.01
pyautogui.MINIMUM_SLEEP = 0.01
pyautogui.MINIMUM_DURATION = 0.01

def apply_nonlinear_response(value, dead_zone, max_response):
    """Apply a non-linear response curve to the input value"""
    if abs(value) < dead_zone:
        return 0
    elif value > 0:
        return ((value - dead_zone) / (max_response - dead_zone)) ** 2
    else:
        return -((abs(value) - dead_zone) / (max_response - dead_zone)) ** 2

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        handLms = results.multi_hand_landmarks[0]  
        h, w, c = img.shape
        
        
        x_min = int((1 - shrink_ratio_x) / 2 * w)
        x_max = int((1 + shrink_ratio_x) / 2 * w)
        y_min = int((1 - shrink_ratio_y) / 2 * h)
        y_max = int((1 + shrink_ratio_y) / 2 * h)

        
        lmList = [(id, int(lm.x * w), int(lm.y * h)) for id, lm in enumerate(handLms.landmark)]

        
        index_tip = next((x for x in lmList if x[0] == 4), None)
        if index_tip:
            cx, cy = index_tip[1], index_tip[2]
            
            
            cx_clamped = np.clip(cx, x_min, x_max)
            cy_clamped = np.clip(cy, y_min, y_max)
            
            
            norm_x = 2 * ((cx_clamped - x_min) / (x_max - x_min)) - 1
            norm_y = 2 * ((cy_clamped - y_min) / (y_max - y_min)) - 1
            
            
            response_x = apply_nonlinear_response(norm_x, dead_zone, max_response)
            response_y = apply_nonlinear_response(norm_y, dead_zone, max_response)
            
            
            screen_x = ((response_x + 1) / 2) * total_screen_w
            screen_y = ((response_y + 1) / 2) * total_screen_h
            
            
            history_x.append(screen_x)
            history_y.append(screen_y)
            
            
            if len(history_x) >= max(1, smoothing_factor // 2):  
                avg_x = sum(history_x) / len(history_x)
                avg_y = sum(history_y) / len(history_y)
                
                
                current_pos = pyautogui.position()
                
                
                target_x = current_pos.x + (avg_x - current_pos.x) * speed_reduction
                target_y = current_pos.y + (avg_y - current_pos.y) * speed_reduction
                
                
                pyautogui.moveTo(target_x, target_y, duration=0.05, _pause=False)

        
        thumb_tip = next((x for x in lmList if x[0] == 8), None)
        if thumb_tip and index_tip:
            x1, y1 = thumb_tip[1], thumb_tip[2]
            x2, y2 = index_tip[1], index_tip[2]
            distance = math.hypot(x2 - x1, y2 - y1)

            current_time = time.time()
            if distance < click_distance_threshold:
                if not clicking and (current_time - last_click_time) > click_cooldown:
                    pyautogui.mouseDown()
                    clicking = True
                    last_click_time = current_time
            else:
                if clicking:
                    pyautogui.mouseUp()
                    clicking = False

        
        mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
        cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

    
    cTime = time.time()
    fps = 1 / (cTime - pTime) if cTime != pTime else 0
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
    
    
    cv2.imshow("fingermouse", img)
    
    
    if cv2.waitKey(1) & 0xFF == 27:
        break


cap.release()
cv2.destroyAllWindows()