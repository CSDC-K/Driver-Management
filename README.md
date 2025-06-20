# Driver Management 🚗🕵️‍♂️

[![License: MIT](https://img.shields.io/github/license/CSDC-K/Driver-Management?style=for-the-badge)](LICENSE)
![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge)
![Platform: Windows](https://img.shields.io/badge/Platform-Windows%2010%2B-00adee?style=for-the-badge&logo=windows)
![UI: CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-ff69b4?style=for-the-badge)

<p align="center">
  <img src="docs/python.gif" alt="Driver Management Demo" width="1200" height="600">
</p>

> **Driver Management** is a lightweight desktop application that lets you **register, identify and manage drivers** using real‑time face recognition and an intuitive CustomTkinter interface.

---

## ✨ Features

|  | Capability |
|:--|:--|
| 👁️ **Face Recognition Login** | Launch the *Start* button to invoke `Sources/face.py`, which authenticates drivers against their stored portraits. |
| ➕ **One‑Click Enrollment** | Capture a driver’s photo from your webcam, enter basic contact info, and save—no command line needed. |
| 🗑️ **Safe Removal** | Delete both the portrait and JSON record in a single action, with confirmation dialogs. |
| 🔄 **Dynamic List View** | Refresh the driver list instantly to reflect new additions or removals. |
| 📂 **Structured Data Store** | Images live under `Sources/faceData/`, metadata in `Sources/driverData/driverData.json`. |
| 🛡️ **Offline‑First** | Runs completely offline; perfect for kiosks or in‑vehicle PCs. |

---

## 🗂️ Project Layout

```text
Driver-Management/
├── main.py                 # GUI entry point
├── Modules/                # (Pluggable extra modules ‑ empty for now)
├── Sources/
│   ├── face.py             # Real‑time recognition loop (starts from main window)
│   ├── faceData/           # Saved driver portraits (*.png)
│   ├── driverData/
│   │   └── driverData.json # Contact info store
│   └── Icons/              # UI icons (phone.png, mail.png, user.png, api.png)
├── docs/
│   └── python.gif          # Demonstration visual
├── requirements.txt        # Dependency list
└── LICENSE
```

---

## 🚀 Getting Started

### Prerequisites

* Windows 10/11
* Python **3.10+**
* Webcam & OpenCV‑compatible camera driver

### Installation

```bash
# 1. Clone & enter repository
$ git clone https://github.com/CSDC-K/Driver-Management.git
$ cd Driver-Management

# 2. Create virtual environment (recommended)
$ python -m venv .venv
$ .\.venv\Scripts\activate

# 3. Install dependencies
$ pip install -r requirements.txt

# 4. Launch
$ python main.py
```

---

## 🛠️ Usage

1. **Run the application** and wait for the main window.
2. Click **“Driver Page”** to open the driver management panel.
3. Use **“Add Driver”** 👉 enter *Name*, *Phone (+90)*, *Mail* & capture the face snapshot.
4. Hit **“Save”** — the portrait lands in `Sources/faceData/NAME.png`, while contact info is appended to `driverData.json`.
5. To **remove** a driver, select their name, then **“Delete Driver”** (with safety checks).
6. **Refresh** at any time to reload the on‑disk list.
7. Back on the home screen, **“Start”** spins up `face.py` to begin live recognition & monitoring.

---

## 🧾 Requirements

Dependencies are listed in [`requirements.txt`](requirements.txt). It includes:

```text
customtkinter
opencv-python
pillow
CTkMessagebox
```

Install them all using:

```bash
pip install -r requirements.txt
```

---

## 🏗️ Roadmap

- [ ] Packaging with **PyInstaller** for one‑click `DriverManagement.exe`
- [ ] Add **CSV/Excel export** for driver lists
- [ ] Integrate SMS/email alerts via Twilio/SMTP
- [ ] Dark‑mode toggle & theme settings
- [ ] CI workflow (GitHub Actions) with basic lint & build badges

Feel free to open an issue to suggest new features! 💡

---

## 🤝 Contributing

1. Fork the repo & create your branch: `git checkout -b feature/my-amazing-idea`  
2. Commit your changes: `git commit -m "✨ Add amazing idea"`  
3. Push to the branch: `git push origin feature/my-amazing-idea`  
4. Open a **Pull Request**.

> **Coding style**: keep functions < 80 LOC, format with *black*, and run *flake8*.

---

## 📜 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for more information.

---

## 🙏 Acknowledgements

- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) — modern Tkinter widgets
- [OpenCV](https://opencv.org/) — real‑time computer vision
- [Pillow](https://python-pillow.org/) — image handling
- [CTkMessagebox](https://github.com/Akascape/CTkMessagebox) — nicer dialogs

<p align="center">
  Made with ❤️ & ☕ by **VV / KUZEY**
</p>
