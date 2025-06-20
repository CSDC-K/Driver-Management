import pandas as pd
import dlib
import cv2
import numpy as np
import time
from gpiozero import Buzzer

buzzer = Buzzer(17)
cap = cv2.VideoCapture(0)


detector = dlib.get_frontal_face_detector()
model = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

def euclidean(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

def eye_aspect_ratio(eye):
    # EAR
    A = euclidean(eye[1], eye[5])
    B = euclidean(eye[2], eye[4])
    C = euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)

say = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray_frame)

    for face in faces:
        points = model(gray_frame, face)
        points_list = [(p.x, p.y) for p in points.parts()]
        left_eye = [points_list[42], points_list[43], points_list[44],
                    points_list[45], points_list[46], points_list[47]]
        right_eye = [points_list[36], points_list[37], points_list[38],
                     points_list[39], points_list[40], points_list[41]]

        # EAR hes
        left_ear = eye_aspect_ratio(left_eye)
        right_ear = eye_aspect_ratio(right_eye)
        ear = (left_ear + right_ear) / 2.0
        if ear < 0.135:
            say += 1
        else:
            say = 0
        if say == 30:
            print("Uyan artık...")
            buzzer.on()
            time.sleep(3)
            buzzer.off()
            say = 0

        print("EAR:", round(ear, 3), " Say:", say)
        for (x, y) in left_eye + right_eye:
            cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

    cv2.imshow("frame", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
