import customtkinter as ctk
import json
import os

DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"websites": [], "visited_today": [], "last_reset": "", "reset_time": "00:00"}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def open_remove_window(parent):
    window = ctk.CTkToplevel(parent)
    window.title("Remove Websites")
    window.geometry("400x400")
    window.resizable(False, False)

    def refresh():
        for widget in website_frame.winfo_children():
            widget.destroy()

        data = load_data()

        for url in data["websites"]:
            row = ctk.CTkFrame(website_frame)
            row.pack(pady=5, fill="x")

            label = ctk.CTkLabel(row, text=url, anchor="w")
            label.pack(side="left", padx=5, fill="x", expand=True)

            delete_btn = ctk.CTkButton(row, text="❌", width=40, command=lambda u=url, r=row: remove_website(u, r))
            delete_btn.pack(side="right", padx=5)

    def remove_website(url, frame):
        data = load_data()
        data["websites"].remove(url)
        if url in data["visited_today"]:
            data["visited_today"].remove(url)
        save_data(data)
        refresh()
        if not data["websites"]:
            window.destroy()

    website_frame = ctk.CTkFrame(window)
    website_frame.pack(pady=20, padx=20, fill="both", expand=True)

    refresh()