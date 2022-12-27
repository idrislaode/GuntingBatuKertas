import cv2 
import numpy as np
import serial

import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
 
TEXT_COLOR = (0,0,0)
LINE_COLOR = (255,255,255) 
 
BAUD = 9600
PORT = 'COM4'

try: 
    wemos = serial.Serial(port=PORT, baudrate=BAUD, timeout=1)
    
    print("berhasil koneksi ke port")
except:
    print("serial port tidak bisa dibuka")


THUMB_THRESH = [9, 8]
NON_THUMB_THRESH = [8.6, 7.6, 6.6, 6.1]

BENT_RATIO_THRESH = [0.76, 0.88, 0.85, 0.65]

CAM_W = 1280
CAM_H = 720  

cap = cv2.VideoCapture(0)
cap.set(3, CAM_W)
cap.set(4, CAM_H) 

charKirim = '0'
tangan = ''

with mp_hands.Hands(
    model_complexity=0,  
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:

    while True:
        _, frame = cap.read()
        frame = cv2.flip(frame, 1)   

        frame.flags.writeable = True
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        results = hands.process(frame) 

        detekTangan = results.multi_hand_landmarks

        if detekTangan: 

            # lihat Fig 2. 21 hand landmarks. https://google.github.io/mediapipe/solutions/hands.html

            ujungTelunjuk = detekTangan[0].landmark[8].y
            ujungTengah = detekTangan[0].landmark[12].y
            ujungManis = detekTangan[0].landmark[16].y
            ujungKici = detekTangan[0].landmark[20].y  
            
            bawahTelunjuk = detekTangan[0].landmark[7].y
            bawahTengah = detekTangan[0].landmark[11].y
            bawahManis = detekTangan[0].landmark[15].y
            bawahKici = detekTangan[0].landmark[19].y 
             
            
            if(ujungTelunjuk <= bawahTelunjuk and ujungTengah <= bawahTengah and ujungManis > bawahManis and ujungKici > bawahKici):
                charKirim = '1'
                tangan = 'Gunting'
                print(tangan)
            elif(ujungTelunjuk > bawahTelunjuk and ujungTengah > bawahTengah and ujungManis > bawahManis and ujungKici > bawahKici):
                charKirim = '2'
                tangan = 'Batu'
                print(tangan)
            elif(ujungTelunjuk <= bawahTelunjuk and ujungTengah <= bawahTengah and ujungManis <= bawahManis and ujungKici <= bawahKici):
                charKirim = '3'
                tangan = 'Kertas'
                print(tangan)
            else:
                charKirim = '0'
                tangan = ''
            
            # untuk tampilkan koneksi sendi jari
            # mp_drawing.draw_landmarks(
            #     frame,
            #     detekTangan[0],
            #     mp_hands.HAND_CONNECTIONS,
            #     mp_drawing_styles.get_default_hand_landmarks_style(),
            #     mp_drawing_styles.get_default_hand_connections_style())

            h, w, c = frame.shape
            cx_min = w
            cy_min = h
            cx_max = cy_max = 0

            for id, lm in enumerate(detekTangan[0].landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)

                if cx<cx_min:
                    cx_min = cx
                if cy<cy_min:
                    cy_min = cy
                if cx>cx_max:
                    cx_max = cx
                if cy>cy_max:
                    cy_max = cy
              
            cv2.rectangle(frame, (cx_min-20,cy_min-20), (cx_max+20,cy_max+20),
                        LINE_COLOR, 1, lineType=cv2.LINE_AA)
            cv2.rectangle(frame, (cx_min-20,cy_min-60), (cx_max+20,cy_min-20),
                        LINE_COLOR, -1, lineType=cv2.LINE_AA)

            cv2.putText(frame, tangan, (cx_min-5, cy_min-30), 0, 1,
                TEXT_COLOR, 2, lineType=cv2.LINE_AA)
            


        key = cv2.waitKey(5)
        if key == ord('q'): 
            break  
        

        if(tangan != ''):

            try: 
                dataKirim = charKirim
                wemos.write(dataKirim.encode()) 
            except: 
                try: 
                    wemos = serial.Serial(port=PORT, baudrate=BAUD, timeout=1)
                    print("berhasil koneksi ke port")
                except:
                    print("serial port tidak bisa dibuka") 

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.imshow('Gesture detection', frame)
        

wemos.close()
cap.release()
cv2.destroyAllWindows()
 