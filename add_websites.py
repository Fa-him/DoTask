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

def open_add_window(parent):
    window = ctk.CTkToplevel(parent)
    window.title("Add Websites")
    window.geometry("400x400")
    window.resizable(False, False)

    entries = []

    # Counter label
    counter_label = ctk.CTkLabel(window, text="0", font=ctk.CTkFont(size=14, weight="bold"))
    counter_label.place(relx=0.95, rely=0.05, anchor="ne")

    # Frame for inputs
    input_frame = ctk.CTkFrame(window)
    input_frame.pack(pady=20, padx=20, fill="both", expand=True)

    def add_input_field():
        entry = ctk.CTkEntry(input_frame, width=300, placeholder_text="Enter website URL")
        entry.pack(pady=5)
        entries.append(entry)
        counter_label.configure(text=str(len(entries)))

    def save_websites():
        data = load_data()
        for entry in entries:
            url = entry.get().strip()
            if url and url not in data["websites"]:
                data["websites"].append(url)
        save_data(data)
        window.destroy()

    # Add first input field
    add_input_field()

    # + button
    add_button = ctk.CTkButton(window, text="+ Add Another", command=add_input_field)
    add_button.pack(pady=5)

    # Submit button
    submit_button = ctk.CTkButton(window, text="Add", command=save_websites)
    submit_button.pack(pady=10)
