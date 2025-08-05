import customtkinter as ctk
import webbrowser
import os
import threading
import subprocess
from flask import Flask, jsonify, request
from utils import load_data, save_data, reset_if_needed
from tracker import start_tracker, update_tracker_label
from alarm import start_alarm

from PIL import Image
import pystray
import sys

# --- Path handling for PyInstaller ---
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# --- Flask app setup ---
flask_app = Flask(__name__)

@flask_app.route('/websites')
def get_websites():
    data = load_data()
    return jsonify({"websites": data.get("websites", [])})

@flask_app.route('/visited', methods=['POST'])
def mark_visited():
    req_data = request.get_json()
    url = req_data.get('url')
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    data = load_data()
    if url not in data['visited_today']:
        data['visited_today'].append(url)
        save_data(data)
        update_tracker_label()
    return jsonify({"success": True, "visited": data['visited_today']})

def run_flask():
    flask_app.run(port=5000, debug=False, use_reloader=False)

# --- GUI Setup ---
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("DoTask")
app.geometry("400x550")
app.resizable(False, False)

frames = {}
data = load_data()
reset_if_needed(data)

# Frames
main_frame = ctk.CTkFrame(app)
add_frame = ctk.CTkFrame(app)
remove_frame = ctk.CTkFrame(app)
visit_frame = ctk.CTkFrame(app)
remaining_frame = ctk.CTkFrame(app)

frames['main'] = main_frame
frames['add'] = add_frame
frames['remove'] = remove_frame
frames['visit'] = visit_frame
frames['remaining'] = remaining_frame

def show_frame(name):
    for f in frames.values():
        f.pack_forget()
    frames[name].pack(fill="both", expand=True, padx=10, pady=10)

# --- Title ---
ctk.CTkLabel(app, text="DoTask", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=10)

# --- MAIN FRAME ---
ctk.CTkLabel(main_frame, text="What do you want to do?", font=ctk.CTkFont(size=16)).pack(pady=10)
ctk.CTkButton(main_frame, text="➕ Add Websites", command=lambda: show_frame('add')).pack(pady=5)
ctk.CTkButton(main_frame, text="❌ Remove Websites", command=lambda: [refresh_remove(), show_frame('remove')]).pack(pady=5)
ctk.CTkButton(main_frame, text="🌐 Visit Websites", command=lambda: [refresh_visit_list(), show_frame('visit')]).pack(pady=5)
ctk.CTkButton(main_frame, text="💋 Open All Websites", command=lambda: [open_all_websites()]).pack(pady=5)
ctk.CTkButton(main_frame, text="📜 Remaining Today", command=lambda: [refresh_remaining_list(), show_frame('remaining')]).pack(pady=5)

ctk.CTkLabel(
    main_frame,
    text="\n📌 Steps to Load the Extension in Chrome:\n\n"
         "1. Open Chrome and go to: chrome://extensions\n"
         "2. Enable 'Developer Mode'\n"
         "3. Click 'Load Unpacked'\n"
         "4. Select the 'dotask-extension' folder\n\n"
         "✅ Done!",
    wraplength=350,
    font=ctk.CTkFont(size=12)
).pack(pady=5)

# --- ADD FRAME ---
add_entries = []
add_counter = ctk.CTkLabel(add_frame, text="0", font=ctk.CTkFont(size=14))
add_counter.place(relx=0.95, rely=0.02, anchor="ne")

input_holder = ctk.CTkFrame(add_frame)
input_holder.pack(pady=10, fill="both", expand=True)

def add_input():
    entry = ctk.CTkEntry(input_holder, width=300, placeholder_text="Enter website URL")
    entry.pack(pady=5)
    add_entries.append(entry)
    add_counter.configure(text=str(len(add_entries)))

def save_added():
    global data
    for entry in add_entries:
        url = entry.get().strip()
        if url and url not in data['websites']:
            data['websites'].append(url)
    save_data(data)
    update_tracker_label()
    show_frame('main')

add_input()
ctk.CTkButton(add_frame, text="+ Add Another", command=add_input).pack(pady=5)
ctk.CTkButton(add_frame, text="Add", command=save_added).pack(pady=10)
ctk.CTkButton(add_frame, text="⬅ Back", command=lambda: show_frame('main')).pack(pady=5)

# --- REMOVE FRAME ---
def refresh_remove():
    global data
    data = load_data()
    for widget in remove_frame.winfo_children():
        widget.destroy()

    ctk.CTkLabel(remove_frame, text="Remove Websites", font=ctk.CTkFont(size=16)).pack(pady=10)
    holder = ctk.CTkFrame(remove_frame)
    holder.pack(pady=10, fill="both", expand=True)

    def remove_site(url, frame):
        data['websites'].remove(url)
        if url in data['visited_today']:
            data['visited_today'].remove(url)
        save_data(data)
        frame.destroy()
        update_tracker_label()

    for url in data['websites']:
        row = ctk.CTkFrame(holder)
        row.pack(fill="x", pady=3)

        label = ctk.CTkLabel(row, text=url, anchor="w")
        label.pack(side="left", padx=5, fill="x", expand=True)

        btn = ctk.CTkButton(row, text="❌", width=30, command=lambda u=url, r=row: remove_site(u, r))
        btn.pack(side="right", padx=5)

    ctk.CTkButton(remove_frame, text="⬅ Back", command=lambda: show_frame('main')).pack(pady=10)

# --- VISIT FRAME ---
def refresh_visit_list():
    global data
    data = load_data()
    for widget in visit_frame.winfo_children():
        widget.destroy()

    ctk.CTkLabel(visit_frame, text="Visit & Mark", font=ctk.CTkFont(size=16)).pack(pady=10)
    holder = ctk.CTkFrame(visit_frame)
    holder.pack(pady=10, fill="both", expand=True)

    def visit_site(url):
        webbrowser.open(url)
        if url not in data['visited_today']:
            data['visited_today'].append(url)
            save_data(data)
            update_tracker_label()
            refresh_visit_list()

    for url in data['websites']:
        visited = url in data['visited_today']
        row = ctk.CTkFrame(holder)
        row.pack(fill="x", pady=3)

        label = ctk.CTkLabel(row, text=("✅ " if visited else "") + url, anchor="w")
        label.pack(side="left", padx=5, fill="x", expand=True)

        btn = ctk.CTkButton(row, text="Go", width=40, command=lambda u=url: visit_site(u))
        btn.pack(side="right", padx=5)

    ctk.CTkButton(visit_frame, text="⬅ Back", command=lambda: show_frame('main')).pack(pady=10)

# --- REMAINING FRAME ---
def refresh_remaining_list():
    global data
    data = load_data()
    for widget in remaining_frame.winfo_children():
        widget.destroy()

    ctk.CTkLabel(remaining_frame, text="Remaining Today", font=ctk.CTkFont(size=16)).pack(pady=10)
    holder = ctk.CTkFrame(remaining_frame)
    holder.pack(pady=10, fill="both", expand=True)

    def visit_site(url):
        webbrowser.open(url)
        if url not in data['visited_today']:
            data['visited_today'].append(url)
            save_data(data)
            update_tracker_label()
            refresh_remaining_list()

    remaining = [url for url in data['websites'] if url not in data['visited_today']]
    if not remaining:
        ctk.CTkLabel(holder, text="✅ All done for today!", font=ctk.CTkFont(size=14)).pack(pady=20)
    else:
        for url in remaining:
            row = ctk.CTkFrame(holder)
            row.pack(fill="x", pady=3)

            label = ctk.CTkLabel(row, text=url, anchor="w")
            label.pack(side="left", padx=5, fill="x", expand=True)

            btn = ctk.CTkButton(row, text="Go", width=40, command=lambda u=url: visit_site(u))
            btn.pack(side="right", padx=5)

    ctk.CTkButton(remaining_frame, text="⬅ Back", command=lambda: show_frame('main')).pack(pady=10)

# --- Open All Websites ---
def open_all_websites():
    global data
    data = load_data()
    for url in data.get('websites', []):
        webbrowser.open(url)

# --- System Tray ---
def quit_app(icon, item):
    icon.stop()
    app.destroy()
    sys.exit()

def show_window(icon, item):
    app.after(0, lambda: app.deiconify())

def hide_window():
    app.withdraw()

def create_tray():
    icon_path = resource_path("icon.ico")
    image = Image.open(icon_path)

    menu = pystray.Menu(
        pystray.MenuItem('Show DoTask', show_window),
        pystray.MenuItem('Exit', quit_app)
    )

    icon = pystray.Icon("DoTask", image, "DoTask Running", menu)
    threading.Thread(target=icon.run, daemon=True).start()

app.protocol("WM_DELETE_WINDOW", hide_window)

# --- Start Services ---
threading.Thread(target=run_flask, daemon=True).start()
start_tracker()
start_alarm()

# --- Show GUI ---
show_frame('main')
create_tray()
app.mainloop()
