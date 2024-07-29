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

