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

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while cap.isOpened():
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = hands.process(img_rgb)

    draw_buttons(img)

    screen_x_start, screen_y_start = 540, 50  
    screen_x_end, screen_y_end = screen_x_start + 4 * button_size, screen_y_start + 200
    cv2.rectangle(img, (screen_x_start, screen_y_start), (screen_x_end, screen_y_end), (255, 255, 255), -1)

    max_display_length = 15  
    display_result = result[-max_display_length:] if len(result) > max_display_length else result
    cv2.putText(img, display_result, (screen_x_start + 10, screen_y_start + 150), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]

            h, w, c = img.shape
            index_finger_tip = (int(index_finger_tip.x * w), int(index_finger_tip.y * h))
            middle_finger_tip = (int(middle_finger_tip.x * w), int(middle_finger_tip.y * h))

            distance = np.linalg.norm(np.array(index_finger_tip) - np.array(middle_finger_tip))
            if distance < 30:
                detect_click(index_finger_tip[0], index_finger_tip[1])

    cv2.imshow("Virtual Calculator", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
