import customtkinter
import tkinter as tk
import cv2
import os
from customtkinter import *
from PIL import Image, ImageTk
from tkinter import simpledialog
from CTkMessagebox import CTkMessagebox
import json
import sys


phoneICO = Image.open("Sources\\Icons\\phone.png")
mailICO = Image.open("Sources\\Icons\\mail.png")
userICO = Image.open("Sources\\Icons\\user.png")
apiICO = Image.open("Sources\\Icons\\api.png")


# Create main application window
app = customtkinter.CTk()

# Window settings
app.title("Sürücü Kontrol || ANA SAYFA")
app.geometry("500x500")
app.resizable(False, False)
customtkinter.set_appearance_mode("white")

def startProgram():
    os.system("start Sources\\face.py")
    os._exit(0)

# Define the Driver page
def identyPg():
    driverPage = customtkinter.CTkToplevel(app)
    driverPage.grab_set()
    driverPage.geometry("500x500")
    driverPage.title("Sürücü Kontrol || Sürücüler")
    driverPage.resizable(False, False)

    driverFrame = customtkinter.CTkFrame(driverPage, fg_color="#D3FDF3", border_width=3, border_color="#14e9bf", corner_radius=20, width=450, height=450)
    driverFrame.place(x=25, y=25)

    def refreshList():
        driverList.delete(0, tk.END)
        folderPath = r"Sources\faceData"
        for file in os.listdir(folderPath):
            drName, _ = os.path.splitext(file)
            driverList.insert(tk.END, drName)

    def saveDriver():
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        savedriverPage = customtkinter.CTkToplevel(driverPage)
        savedriverPage.grab_set()
        savedriverPage.geometry("500x500")
        savedriverPage.title("Sürücü Kontrol || Sürücü Ekleme")
        savedriverPage.resizable(False, False)
        #cpza mmbs vsxw ijgw

        def reFrame():
            ret, frame = cap.read()
            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                height, width, _ = frame_rgb.shape
                canvas_width = canvas.winfo_width()
                canvas_height = canvas.winfo_height()

                if canvas_width == 1 or canvas_height == 1:
                    canvas_width, canvas_height = 500, 500

                aspect_ratio = width / height
                canvas_aspect_ratio = canvas_width / canvas_height

                if aspect_ratio > canvas_aspect_ratio:
                    new_width = canvas_width
                    new_height = int(new_width / aspect_ratio)
                else:
                    new_height = canvas_height
                    new_width = int(new_height * aspect_ratio)

                if new_width > 0 and new_height > 0:
                    resized_frame = cv2.resize(frame_rgb, (new_width, new_height))
                else:
                    resized_frame = frame_rgb

                img = Image.fromarray(resized_frame)
                img_tk = ImageTk.PhotoImage(image=img)
                canvas.create_image(canvas_width // 2, canvas_height // 2, anchor=tk.CENTER, image=img_tk)
                canvas.image = img_tk

            savedriverPage.after(10, reFrame)

        savedriverFrame = customtkinter.CTkFrame(savedriverPage, fg_color="#D3FDF3", border_width=3, border_color="#14e9bf", corner_radius=20, width=475, height=475)
        savedriverFrame.place(x=12, y=12)

        mailEntry = CTkEntry(savedriverFrame,placeholder_text="Sürücü Mail",font=("helvetica", 15), width=200,corner_radius=15,border_width=0)
        mailEntry.place(x=25, y=375)

        telEntry = CTkEntry(savedriverFrame,placeholder_text="Sürücü Tel, +90 ile girin.",font=("helvetica", 15), width=200,corner_radius=15,border_width=0)
        telEntry.place(x=25, y=325)

        nameEntry = CTkEntry(savedriverFrame,placeholder_text="Sürücü İsmi",font=("helvetica", 15), width=200,corner_radius=15,border_width=0)
        nameEntry.place(x=25, y=275)

        canvas = customtkinter.CTkCanvas(savedriverFrame)
        canvas.place(x=30, y=5)

        def save_image():
            ret, frame = cap.read()
            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                driverName = nameEntry.get()
                driverTel = telEntry.get()
                driverMail = mailEntry.get()

                if driverName and driverTel and driverMail:
                    os.makedirs(r"Sources\faceData", exist_ok=True)

                    img = Image.fromarray(frame_rgb)
                    save_path = os.path.join("Sources", "faceData", f"{driverName}.png")

                    if os.path.exists(save_path):
                        print(f"ERROR: '{driverName}.png' dosyası zaten mevcut!")
                        CTkMessagebox(title="HATA!", message="Bu ada sahip bir sürücü zaten mevcut.", icon="cancel",option_1="Tamam")
                    else:
                        img.save(save_path)
                        print(f"Fotoğraf başarıyla kaydedildi: {save_path}")
                        refreshList()

                        with open("Sources\\driverData\\driverData.json", "r", encoding="utf-8") as file:
                            data = json.load(file)


                        data[driverName] = {
                            "driverMail" : driverMail,
                            "driverTel" : driverTel,
                        }

                        with open("Sources\\driverData\\driverData.json", "w", encoding="utf-8") as file:
                            json.dump(data, file, indent=4, ensure_ascii=False)

                        CTkMessagebox(title="Sürücü İşlem", message="Yeni sürücü eklendi.", icon="check",option_1="Tamam")
                else:
                    CTkMessagebox(title="Hata", message=f"Eksik veri.", icon="cancel")


        save_button = customtkinter.CTkButton(savedriverFrame, text="Kaydet", font=("helvetica", 15), fg_color="#38a620", corner_radius=15, width=50, height=50, hover_color="#40902f", command=save_image)
        save_button.place(x=300, y=300)

        reFrame()

    def deleteDriver():
        selected_driver = driverList.curselection()
        if selected_driver:
            driver_name = driverList.get(selected_driver)

            # Dosya yolu oluşturuluyor
            driver_image_path = os.path.join(r"Sources\faceData", f"{driver_name}.png")

            if os.path.exists(driver_image_path):
                try:
                    os.remove(driver_image_path)  # Fotoğrafı silme
                    with open("Sources\\driverData\\driverData.json", "r", encoding="utf-8") as file:
                        veri = json.load(file)
                    
                    if driver_name in veri:
                        del veri[driver_name]

                    with open("Sources\\driverData\\driverData.json", "w", encoding="utf-8") as file:
                        json.dump(veri, file, indent=4, ensure_ascii=False)
                    print(f"'{driver_name}.png' dosyası başarıyla silindi.")
                    CTkMessagebox(title="Başarılı", message=f"'{driver_name}' sürücüsü silindi.", icon="check")
                except Exception as e:
                    print(f"Silme hatası: {e}")
                    CTkMessagebox(title="Hata", message=f"Bir hata oluştu: {str(e)}", icon="cancel")
                
                driverList.delete(selected_driver)  # Listeden de silme
            else:
                print(f"'{driver_name}.png' dosyası bulunamadı.")
                CTkMessagebox(title="Hata", message="Seçilen sürücüye ait dosya bulunamadı.", icon="cancel")
        else:
            print("Bir sürücü seçilmedi.")
            CTkMessagebox(title="Hata", message="Silmek için bir sürücü seçin.", icon="cancel")

    def informationDriver():
        infdriverPage = customtkinter.CTkToplevel(driverPage)
        infdriverPage.grab_set()
        infdriverPage.geometry("500x500")
        infdriverPage.title("Sürücü Kontrol || Sürücü Bilgileri")
        infdriverPage.resizable(False, False)

        infdriverFrame = customtkinter.CTkFrame(infdriverPage, fg_color="#D3FDF3", border_width=3, border_color="#14e9bf", corner_radius=20, width=450, height=450)
        infdriverFrame.place(x=25, y=25)

        infdownFrame = customtkinter.CTkFrame(infdriverFrame, fg_color="#404040", border_width=3, border_color="#212121", corner_radius=20, width=400, height=200)
        infdownFrame.place(x=25, y=245)

        selected_driver = driverList.curselection()

        if selected_driver:

            

            driver_name = driverList.get(selected_driver)
            driver_image_path = os.path.join(r"Sources\faceData", f"{driver_name}.png")
            driverreImg = Image.open(driver_image_path)
            driverreImg = driverreImg.resize((225,200))
            driverImg = ImageTk.PhotoImage(driverreImg)

            with open("Sources\\driverData\\driverData.json", "r") as file:
                driverData = json.load(file)

            

            driverLabel = customtkinter.CTkLabel(infdriverFrame, text="Sürücü Bilgisi", font=("verdana", 22, "bold"), text_color="#000000")
            driverimg = customtkinter.CTkButton(infdriverFrame, text="", image=driverImg, corner_radius=15, border_width=0, fg_color="#292c29",width=425)
            drivernameLabel = customtkinter.CTkLabel(infdownFrame, text=f"  {driver_name}", font=("verdana", 14), text_color="#FFFFFF", image=CTkImage(light_image=userICO,size=(35, 35)),compound=LEFT)
            drivertelLabel = CTkLabel(infdownFrame,text="{}", font=("verdana", 14),text_color="#FFFFFF", image=CTkImage(phoneICO, size=(35,35)), compound=LEFT).format(driverData[driver_name]["driverMail"])
            drivermailLabel = customtkinter.CTkLabel(infdownFrame, text="  {}", font=("verdana", 14), text_color="#FFFFFF",image=CTkImage(light_image=mailICO,size=(35, 35)),compound=LEFT).format(driverData[driver_name]["driverMail"])

            driverLabel.place(x=135,y=5)
            driverimg.place(x=12,y=35)

            drivernameLabel.place(x=25,y=20)
            drivertelLabel.place(x=25, y=70)
            drivermailLabel.place(x=25, y=120)



            




    driverList = tk.Listbox(driverFrame, bg="#404040", fg="#FFFFFF", selectmode=tk.SINGLE, width=30, height=20)
    driverList.place(x=25, y=50)

    listLabel = customtkinter.CTkLabel(driverFrame, text="Sürücüler", font=("verdana", 25, "bold"), text_color="#000000")

    deldrivertBT = customtkinter.CTkButton(driverFrame, text="Sürücü Sil", font=("helvetica", 15, "bold"), fg_color="#dc6950",
                                          corner_radius=15, width=150, height=40, hover_color="#a95846", command=deleteDriver)

    addrivertBT = customtkinter.CTkButton(driverFrame, text="Sürücü Ekle", font=("helvetica", 15, "bold"), fg_color="#38a620",
                                          corner_radius=15, width=150, height=40, hover_color="#40902f", command=saveDriver)

    infdrivertBT = customtkinter.CTkButton(driverFrame, text="Sürücü Bilgisi", font=("helvetica", 15, "bold"), fg_color="#525853",
                                          corner_radius=15, width=150, height=40, hover_color="#3a3e3a", command=informationDriver)

    refreshlistBT = customtkinter.CTkButton(driverFrame, text="Yenile", font=("helvetica", 15, "bold"), fg_color="#7b9094",
                                            corner_radius=15, width=150, height=40, hover_color="#737d80", command=refreshList)

    listLabel.place(x=25, y=5)
    refreshlistBT.place(x=40, y=380)
    addrivertBT.place(x=250, y=125)
    deldrivertBT.place(x=250, y=200)
    infdrivertBT.place(x=250,y=275)


mainFrame = customtkinter.CTkFrame(app, fg_color="#D3FDF3", border_width=3, border_color="#14e9bf", corner_radius=20, width=450, height=450)
mainFrame.place(x=25, y=25)

mainLabel = customtkinter.CTkLabel(mainFrame, text="Sürücü Kontrol", font=("Impact", 30, "bold"), text_color="#000000")
downLabel = customtkinter.CTkLabel(mainFrame, text="Tübitak 4006", font=("helvetica", 20), text_color="#000000")
madeLabel = customtkinter.CTkLabel(mainFrame, text="Made By VV || KUZEY", font=("helvetica", 10, "bold"), text_color="#000000")

newidBT = customtkinter.CTkButton(mainFrame, text="Sürücü Sayfası", font=("helvetica", 15, "bold"), fg_color="#38a620",
                                  corner_radius=15, width=200, height=40, hover_color="#40902f", command=identyPg)

startBT = customtkinter.CTkButton(mainFrame, text="Başlat", font=("helvetica", 15, "bold"), fg_color="#25a6bd",
                                  corner_radius=15, width=200, height=40, hover_color="#2c96a9", command=startProgram)

mainLabel.place(x=125, y=25)
downLabel.place(x=170, y=75)
madeLabel.place(x=25, y=415)

newidBT.place(x=125, y=175)
startBT.place(x=125, y=250)

app.mainloop()
