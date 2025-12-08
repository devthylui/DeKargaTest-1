import tkinter as tk
from PIL import Image, ImageTk
import os, sys

def resource_path(relative_path):
    """Get the absolute path for PyInstaller exe or dev mode."""
    if hasattr(sys, '_MEIPASS'):  # running from exe
        base_path = sys._MEIPASS
    else:  # running in Python
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class predictionFrame(tk.Frame):
    def __init__(self, master, switch_callback, filename):
        super().__init__(master)

        self.filename = filename
        
        rowFrame1 = tk.Frame(self)
        rowFrame1.pack(pady=20)

        imagePath = resource_path(os.path.join("images", filename))
        imageRaw = Image.open(imagePath)
        #imageRaw = Image.open("./images/" + filename)
        imageRaw = imageRaw.resize((200, 100))
        self.imageTk = ImageTk.PhotoImage(imageRaw)

        self.image_box = tk.Frame(rowFrame1, width=200, height=100)
        self.image_box.pack(side="left", padx=20)
        image_label = tk.Label(self.image_box, image=self.imageTk)
        image_label.pack()

        self.analysis_box = tk.Frame(rowFrame1, width=100, height=100, bg="gray")
        self.analysis_box.pack(side="left", padx=20)
        
        rowFrame2 = tk.Frame(self)
        rowFrame2.pack()

        self.predict_button = tk.Button(rowFrame2, text="Predict")
        self.predict_button.pack(side="left", padx=5)
        
        self.back_button = tk.Button(rowFrame2, text="Back", command=lambda: switch_callback("filesFrame"))
        self.back_button.pack(side="left", padx=5)