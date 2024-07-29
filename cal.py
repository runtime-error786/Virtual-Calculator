import cv2
import numpy as np
import mediapipe as mp
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

button_positions = []
button_size = 100
result = ""
last_click_time = 0
click_cooldown = 1 

def create_buttons():
    global button_positions
    x_start, y_start = 540, 300  
    labels = ['7', '8', '9', '/',
              '4', '5', '6', '*',
              '1', '2', '3', '-',
              '0', 'C', '=', '+']
    for i in range(4):
        for j in range(4):
            x = x_start + j * button_size
            y = y_start + i * button_size
            button_positions.append((x, y, labels[i * 4 + j]))

def draw_buttons(img):
    for (x, y, label) in button_positions:
        overlay = img.copy()
        cv2.rectangle(overlay, (x, y), (x + button_size, y + button_size), (150, 150, 150), -1)
        alpha = 0.6  
        cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)
        cv2.rectangle(img, (x, y), (x + button_size, y + button_size), (255, 255, 255), 2)

        cv2.putText(img, label, (x + 30, y + 70), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)

def detect_click(x, y):
    global result, last_click_time
    current_time = time.time()
    if current_time - last_click_time < click_cooldown:
        return
    for (bx, by, label) in button_positions:
        if bx < x < bx + button_size and by < y < by + button_size:
            last_click_time = current_time
            if label == 'C':
                result = ""
            elif label == '=':
                try:
                    eval_result = eval(result)
                    if isinstance(eval_result, float):
                        eval_result = f"{eval_result:.4f}"
                    result = str(eval_result)
                except:
                    result = "Error"
            else:
                result += label

create_buttons()
