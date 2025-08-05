import customtkinter as ctk
from utils import load_data, reset_if_needed
import threading
import time

label = None
tooltip_label = None
tracker = None

def make_draggable(widget):
    def start_move(event):
        widget.x = event.x
        widget.y = event.y

    def do_move(event):
        x = widget.winfo_x() + event.x - widget.x
        y = widget.winfo_y() + event.y - widget.y
        widget.geometry(f"+{x}+{y}")

    widget.bind("<Button-1>", start_move)
    widget.bind("<B1-Motion>", do_move)

def show_tooltip(event):
    global tooltip_label
    data = load_data()
    reset_if_needed(data)
    remaining = [url for url in data['websites'] if url not in data['visited_today']]
    text = "\n".join(remaining) if remaining else "✅ All visited!"

    if tooltip_label:
        tooltip_label.destroy()

    tooltip_label = ctk.CTkLabel(
        tracker,
        text=text,
        font=ctk.CTkFont(size=12),
        fg_color="gray20",
        text_color="white",
        corner_radius=6
    )
    tooltip_label.place(relx=0.5, rely=1.0, anchor="n", y=5)

def hide_tooltip(event):
    global tooltip_label
    if tooltip_label:
        tooltip_label.destroy()
        tooltip_label = None

def start_tracker():
    global label, tracker

    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    tracker = ctk.CTkToplevel()
    tracker.title("Tracker")
    tracker.geometry("0+60")
    tracker.minsize(100, 50)
    tracker.resizable(True, True)
    tracker.attributes("-topmost", True)
    tracker.configure(fg_color="black")

    label = ctk.CTkLabel(
        tracker,
        text="0/0",
        font=ctk.CTkFont(size=20, weight="bold"),
        fg_color="black",
        text_color="white"
    )
    label.pack(padx=10, pady=10, fill="both", expand=True)

    # Tooltip hover
    label.bind("<Enter>", show_tooltip)
    label.bind("<Leave>", hide_tooltip)

    make_draggable(tracker)

    def update_loop():
        while True:
            update_tracker_label()
            time.sleep(30)

    threading.Thread(target=update_loop, daemon=True).start()

def update_tracker_label():
    global label
    if label:
        data = load_data()
        reset_if_needed(data)
        total = len(data["websites"])
        visited = len(data["visited_today"])
        label.configure(text=f"{visited}/{total}")
        label.configure(text_color="green" if visited == total and total > 0 else "red")

# For standalone test
if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    root.withdraw()
    start_tracker()
    root.mainloop()
