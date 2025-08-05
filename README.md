# 🧠 DoTask – Smart Daily Website Visit Tracker

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Tkinter](https://img.shields.io/badge/UI-CustomTkinter-brightgreen)
![Status](https://img.shields.io/badge/Status-Completed-success)
![License](https://img.shields.io/badge/License-MIT-blue.svg)

> A lightweight, always-on-top productivity app with a floating tracker, alarm system, system tray integration, and Chrome extension support — built to help you complete your daily website visits on time.

---

## ✨ Features

- ✅ Add or remove your daily websites
- 🌐 Mark websites as visited or open all at once
- 🔗 Chrome extension integration for automatic site tracking
- 🚦 Floating always-on-top **progress tracker** (e.g., `2/5`)
- 🖱️ Hover over tracker to see remaining websites
- ⏰ Triggers **alarm** if not completed within 2 hours
- 💻 Runs in the background via **System Tray**
- 🧩 Built-in Chrome extension setup guide
- ⚡ Self-contained executable (via PyInstaller)

---


## 🧩 Chrome Extension Setup

1. **Download** the [`dotask-extension`](./dotask-extension) folder from this repository  
   *(Or clone the full repo and locate the folder)*

2. Open **Google Chrome** and go to: `chrome://extensions`

3. **Enable** Developer Mode (top-right corner)

4. Click **"Load unpacked"**

5. Select the `dotask-extension` folder you downloaded

✅ You're done! The extension is now active and will track your visited websites through the DoTask app.

---


## 💻 DoTask App Setup (`.exe`)

1. **Download** the latest `DoTask.exe` file from the [Releases](./releases) section  

2. Double-click to **install and run** the app

3. You’ll see it minimized in the **System Tray** (bottom-right)

4. Use the main window to:
   - ➕ Add websites
   - ❌ Remove websites
   - 🌐 Visit and mark websites
   - 🔗 Open all at once
   - 📋 View remaining for today

🟢 Tracker window shows your daily progress (hover to see what’s left to visit!)

⏰ Alarm will alert you if you don’t finish your visits within 2 hours of reset time.

> 💡 Tip: Set the app to auto-run on startup for daily consistency.

### 📁 Clone the Project

```bash
git clone https://github.com/Fa-him/DoTask.git
cd DoTask
