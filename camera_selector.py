import tkinter as tk
from tkinter import simpledialog
import os

def select_camera():
    root = tk.Tk()
    root.withdraw()  # Hide main window

    choice = simpledialog.askstring("Select Camera", "Enter camera index (e.g., 0, 1) or IP camera URL:")
    if choice is not None:
        with open("camera_config.txt", "w") as f:
            f.write(choice.strip())
        print("Camera selection saved.")
    else:
        print(" No camera selected.")

def get_camera_source():
    try:
        with open("camera_config.txt", "r") as f:
            source = f.read().strip()
            if source.startswith("http"):
                return source
            else:
                return int(source)
    except:
        return 0  # Default laptop camera
