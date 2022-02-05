# Automation Control <<Subway Surf>>
# UP : Index finger
# DOWN : Middle finger
# LEFT : Thumb
# RIGHT : Little finger

import cv2
import mediapipe as mp

import time
from directionkeys import NP_4, NP_6, NP_2, NP_8
from directionkeys import PressKey, ReleaseKey

right_pressed = NP_6
left_pressed = NP_4
up_pressed = NP_8
down_pressed = NP_2

left_key_pressed = left_pressed
right_key_pressed = right_pressed
up_key_pressed = up_pressed
down_key_pressed = down_pressed

time.sleep(2.0)
current_key_pressed = set()


mp_hand = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
handLmsStyle = mp_draw.DrawingSpec(color=(0,0,255), thickness=5)
handConStyle = mp_draw.DrawingSpec(color=(0,255,0), thickness=10)

tipIds = [4,8,12,16,20]

video = cv2.VideoCapture(0)

with mp_hand.Hands(max_num_hands=1, min_detection_confidence=0.85,
                min_tracking_confidence=0.5) as hands:

    while True:
        keyPressed = False
        left_pressed = False
        right_pressed = False
        up_pressed = False
        down_pressed = False

        key_count = 0
        key_pressed = 0

        success, img = video.read()
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img.flags.writeable = False #資料區域可以被寫入，將該值設定為 False，則資料為只讀
        results = hands.process(img)
        img.flags.writeable = True
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        lmList = []
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                myHands = results.multi_hand_landmarks[0]
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([id, cx, cy])
                mp_draw.draw_landmarks(img, handLms, mp_hand.HAND_CONNECTIONS, handLmsStyle, handConStyle)

        
        if len(lmList) != 0:
            
            left_direct = False
            right_direct = False
            up_direct = False
            down_direct = False

            fingers = []
            if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
            for id in range(1,5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            totalfingers = fingers.count(1)
            if totalfingers == 1:
                # LEFT (大拇指)
                if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:
                    left_direct = True
                else:
                    left_direct = False

                # UP (食指)
                if lmList[tipIds[1]][2] < lmList[tipIds[1] - 2][2]:
                    up_direct = True
                else:
                    up_direct = False

                # DOWN (中指)
                if lmList[tipIds[2]][2] < lmList[tipIds[2] - 2][2]:
                    down_direct = True
                else:
                    down_direct = False

                # RIGHT (小拇指)
                if lmList[tipIds[4]][2] < lmList[tipIds[4] - 2][2]:
                    right_direct = True
                else:
                    right_direct = False




            if left_direct: #左跳
                cv2.rectangle(img, (20, 300), (270, 425), (0, 255, 0),cv2.FILLED)
                cv2.putText(img, "LEFT", (73, 382), cv2.FONT_HERSHEY_SIMPLEX,
                2, (255,0,0), 5)
                PressKey(left_key_pressed)
                left_pressed = True
                keyPressed = True
                current_key_pressed.add(left_key_pressed)
                key_pressed = left_key_pressed
                key_count = key_count + 1

            elif right_direct: #右跳
                cv2.rectangle(img, (20, 300), (270, 425), (0, 255, 0),cv2.FILLED)
                cv2.putText(img, "RIGHT", (55, 382), cv2.FONT_HERSHEY_SIMPLEX,
                2, (255,0,0), 5)
                PressKey(right_key_pressed)
                key_pressed = right_key_pressed
                right_pressed = True
                keyPressed = True
                current_key_pressed.add(right_key_pressed)
                key_count = key_count + 1

            elif down_direct: #下滑
                cv2.rectangle(img, (20, 300), (270, 425), (0, 255, 0),cv2.FILLED)
                cv2.putText(img, "DOWN", (55, 382), cv2.FONT_HERSHEY_SIMPLEX,
                2, (255,0,0), 5)
                PressKey(down_key_pressed)
                down_pressed = True
                keyPressed = True
                current_key_pressed.add(down_key_pressed)
                key_pressed = down_key_pressed
                key_count = key_count + 1

            elif up_direct: #上跳
                cv2.rectangle(img, (20, 300), (270, 425), (0, 255, 0),cv2.FILLED)
                cv2.putText(img, "UP", (101, 382), cv2.FONT_HERSHEY_SIMPLEX,
                2, (255,0,0), 5)
                PressKey(up_key_pressed)
                up_pressed = True
                keyPressed = True
                current_key_pressed.add(up_key_pressed)
                key_pressed = up_key_pressed
                key_count = key_count + 1

        if not keyPressed and len(current_key_pressed) != 0: 
            for key in current_key_pressed:
                ReleaseKey(key)
            current_key_pressed = set()
        elif key_count == 1 and len(current_key_pressed) == 2:
            for key in current_key_pressed:
                if key_pressed == key:
                    ReleaseKey(key)

            current_key_pressed = set()
            for key in current_key_pressed:
                print(key)
                ReleaseKey(key)
            current_key_pressed = set()

        if success:
            cv2.imshow("Image", img)
        else:
            break
        if cv2.waitKey(1) == ord('q'):
            break
video.release()
cv2.destroyAllWindows()