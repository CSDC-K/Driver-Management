import argparse
import sys
import dlib
import cv2
import numpy as np
import threading
import pygame
import time
import geocoder
import json
import pywhatkit

import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

mailHost = "smtp-gmail.com"
hostPort = 587

mailSender = "urazerkoc3@gmail.com"
passCode = "qxgm qqns figr qavu"

# ARGPARSE: Şifre kontrolü
parser = argparse.ArgumentParser(description="Göz takip uygulaması")
parser.add_argument("-p", "--password", required=True, help="Giriş şifresi")
args = parser.parse_args()

def sendMsg():
    with open("Sources\\driverData\\driverData.json", "r") as file:
        driverData = json.load(file)

    with open("Sources\\driverData\\activeDriver.txt", "r") as file2:
        activeDriver = file2.read()

        sendTo = driverData[f"{activeDriver}"]["driverTel"]

        pywhatkit.sendwhatmsg_instantly(sendTo, "Sürücünün Uyuduğu Tetiklendi.", wait_time=2, tab_close=True)

def sendMail():
    with open("Sources\\driverData\\driverData.json", "r") as file:
        driverData = json.load(file)

    with open("Sources\\driverData\\activeDriver.txt", "r") as file2:
        activeDriver = file2.read()

        loc = geocoder.ip('me')

        if loc.ok:
            lat, lng = loc.latlng
            google_maps_link = f"https://www.google.com/maps?q={lat},{lng}"


        Mesg = f"""

        Sürücü Uyku Uyarısı!

        Konum: {google_maps_link}
        """

        Title = "Sürücü Uyarı Sistemi."

        recHost = driverData[f"{activeDriver}"]["driverMail"]

        msg = MIMEMultipart()
        msg["From"] = mailSender
        msg["To"] = recHost
        msg["Subject"] = Title
        msg.attach(MIMEText(Mesg, "plain"))
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            print("Sending Mail")
            server.starttls()
            server.login(mailSender, "qxgm qqns figr qavu")
            server.send_message(msg)
            print("Sended Mail")

if args.password != "awreqsoqueureq@SYWGS?!_32112222341":
    print("❌ Yasaklı giriş denemesi.")
    sys.exit(1)
else:
    print("🔓 Arayüz erişimi başarılı.")

# Kamera ve ses dosyası başlatma
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)


pygame.mixer.init()
acikSound = pygame.mixer.Sound("Sources\\gozler_acik.mp3")
beepSound = pygame.mixer.Sound("Sources\\beep.mp3")
kapaliSound = pygame.mixer.Sound("Sources\\gozler_kapali.mp3")

goz_durumu = "açık"
uyari_veriliyor = False
uyari_tetiklendi_zamani = None
UYANMA_SINIRI = 3

def playMpSound(soundName: str):
    if soundName == "kapaliSound":
        kapaliSound.play()
    elif soundName == "acikSound":
        acikSound.play()

    elif soundName == "beepSound":
        beepSound.play()

# dlib modelleri
detector = dlib.get_frontal_face_detector()
model = dlib.shape_predictor("Sources\\shape_predictor_68_face_landmarks.dat")

# Göz oranı hesaplama
def euclidean(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

def eye_aspect_ratio(eye):
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

        left_ear = eye_aspect_ratio(left_eye)
        right_ear = eye_aspect_ratio(right_eye)
        ear = (left_ear + right_ear) / 2.0

        if ear < 0.21:
            say += 1
            goz_durumu = "kapalı"
        else:
            say = 0
            goz_durumu = "açık"
            uyari_veriliyor = False
            uyari_tetiklendi_zamani = None

        if goz_durumu == "kapalı":
            cv2.putText(frame, "Gozler Kapali", (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)
            if not uyari_veriliyor and say >= 30:
                print("Uyan artık...")
                uyari_veriliyor = True
                uyari_tetiklendi_zamani = time.time()
                threading.Thread(target=playMpSound, args=("kapaliSound",)).start()
                threading.Thread(target=sendMail).start()
                
            elif uyari_veriliyor and uyari_tetiklendi_zamani:
                if time.time() - uyari_tetiklendi_zamani > UYANMA_SINIRI:
                    cv2.putText(frame, "UYAN!", (30, 120), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)
                    threading.Thread(target=playMpSound, args=("beepSound",)).start()

        else:
            cv2.putText(frame, "Gozler Acik", (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 3)

        print("ORAN:", round(ear, 3), f" {goz_durumu}")

        for (x, y) in left_eye + right_eye:
            cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

    cv2.imshow("frame", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()