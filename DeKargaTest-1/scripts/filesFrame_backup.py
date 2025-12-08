import tkinter as tk
import os, sys

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):  # Running from exe
        base_path = sys._MEIPASS
    else:  # Running from source
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

directory = resource_path("images")
os.makedirs(directory, exist_ok=True)
#directory = "./images/"

class filesFrame(tk.Frame):
    def __init__(self, master, switch_callback):
        super().__init__(master)

        images = [
            file for file in os.listdir(directory)
            if file.lower().endswith((".png", ".jpg", ".jpeg"))
        ]
        
        if len(images) == 0:
            emptyText = tk.Label(self, text="No images found.", font=("Arial", 16))
            emptyText.pack(pady=10)
        else:
            for image in images:
                name, ext = os.path.splitext(image)
                buttonText = f"{name.title()}{ext.lower()}"
                button = tk.Button(self, text=buttonText, command=lambda f=image: switch_callback("predictionFrame", f))
                button.pack()
        
        button = tk.Button(self, text="Back", command=lambda: switch_callback("mainFrame"))
        button.pack(pady=10)