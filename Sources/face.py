import cv2
import face_recognition
import os
import threading
import time
import os
import sys
import pygame
import subprocess

pygame.mixer.init()
girisSound = pygame.mixer.Sound("Sources\\giris.mp3")
KNOWN_FACES_DIR = "Sources\\faceData"
SCALE = 0.25
FRAME_SKIP = 15

known_face_encodings = []
known_face_names = []

def soundPlay():
    girisSound.play()

for filename in os.listdir(KNOWN_FACES_DIR):
    path = os.path.join(KNOWN_FACES_DIR, filename)
    image = face_recognition.load_image_file(path)
    try:
        encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(encoding)
        known_face_names.append(os.path.splitext(filename)[0])
    except IndexError:
        print(f"[!] Yüz bulunamadı: {filename} atlandı.")

latest_faces = []
latest_locations = []
lock = threading.Lock()
giris_yapildi = False  # <<< Ekleme

def face_recognition_thread(frame):
    global latest_faces, latest_locations, giris_yapildi

    small = cv2.resize(frame, (0, 0), fx=SCALE, fy=SCALE)
    rgb = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)

    locations = face_recognition.face_locations(rgb, model='hog')
    encodings = face_recognition.face_encodings(rgb, locations)

    names = []

    for encoding in encodings:
        distances = face_recognition.face_distance(known_face_encodings, encoding)
        if len(distances) > 0:
            min_distance = min(distances)
            if min_distance < 0.6:
                index = distances.tolist().index(min_distance)
                name = known_face_names[index]
                names.append(name)

                if not giris_yapildi:
                    # İsmi dosyaya kaydet
                    with open("Sources\\driverData\\activeDriver.txt", "w", encoding="utf-8") as f:
                        f.write(name)

                    #threading.Thread(target=soundPlay).start()
                    print(f"[✓] {name} sisteme giriş yaptı.")
                    giris_yapildi = True
                    cap.release()
                    subprocess.Popen(["python", "Sources\\woRasp.py", "-p", "awreqsoqueureq@SYWGS?!_32112222341"])
                    girisSound.play()

            else:
                names.append("Bilinmiyor")
        else:
            names.append("Bilinmiyor")

    with lock:
        latest_faces = names
        latest_locations = locations


cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
frame_id = 0

print("[i] Canlı yüz tanıma başlatıldı. Çıkmak için Q tuşu.")

while True:
    start = time.time()
    ret, frame = cap.read()
    if not ret:
        break

    frame_id += 1
    if frame_id % FRAME_SKIP == 0:
        threading.Thread(target=face_recognition_thread, args=(frame.copy(),)).start()

    with lock:
        names = latest_faces[:]
        locations = latest_locations[:]

    for (top, right, bottom, left), name in zip(locations, names):
        top *= int(1 / SCALE)
        right *= int(1 / SCALE)
        bottom *= int(1 / SCALE)
        left *= int(1 / SCALE)

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

    elapsed = time.time() - start
    fps = 1 / elapsed if elapsed > 0 else 0

    cv2.putText(frame, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    cv2.imshow("Yuz Tarama", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
