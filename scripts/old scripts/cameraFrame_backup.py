import math
import os, sys
import time
import cv2
import tkinter as tk
import numpy as np
from PIL import Image, ImageTk, ImageEnhance

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):  # Running from exe
        base_path = sys._MEIPASS
    else:  # Running from source
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

directory = resource_path("images")
#directory = "./images/"
os.makedirs(directory, exist_ok=True)

class cameraFrame(tk.Frame):
    def __init__(self, master, switch_callback):
        super().__init__(master)

        self.captured = False

        self.tile_img = Image.open("./sprites/Grey_background_2.png")
        self.variants = []
        for brightness in np.linspace(1.5, 1.0, 15):
            self.altered_tile = ImageEnhance.Brightness(self.tile_img).enhance(brightness)
            self.variants.append(ImageTk.PhotoImage(self.altered_tile))
        self.canvas = tk.Canvas(self, highlightthickness=0, borderwidth=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self.draw_tiles)

        screen_width = int(self.winfo_screenwidth()/2)
        screen_height = int(self.winfo_screenheight()/2)
        center_frame = tk.Frame(self.canvas, width=screen_width, height=screen_height, bg="white")
        center_frame.place(relx="0.5", rely="0.5", anchor="center")
        
        rowFrame1 = tk.Frame(center_frame)
        rowFrame1.pack(pady=20)

        self.camera_frame = tk.Label(rowFrame1, width=screen_width, height=screen_height, bg="gray")
        self.camera_frame.pack(side="left", padx=20)

        self.cap = cv2.VideoCapture(0)
        self.update_frame()
        self.bind("<Destroy>", self.on_closing)
        
        self.scroll_canvas = tk.Canvas(rowFrame1, width=200, height=screen_height, bg="gray", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(rowFrame1, orient="vertical", command=self.scroll_canvas.yview)
        self.scroll_canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.scroll_canvas.pack(side="left", fill="both", expand=True)

        self.analysis_box = tk.Frame(self.scroll_canvas, bg="gray")
        self.scroll_canvas.create_window((0, 0), window=self.analysis_box, anchor="nw")

        self.analysis = tk.Label(self.analysis_box, text="", font=("Arial", 12), justify="left", wraplength=175, bg="gray")
        self.analysis.pack(anchor="w", pady="10px", padx="10px")
        self.analysis_box.bind("<Configure>", self.update_scroll)
        
        rowFrame2 = tk.Frame(center_frame)
        rowFrame2.pack()

        self.capture_button = tk.Button(rowFrame2, text="Capture", command=lambda: self.capturePhoto(switch_callback))
        self.capture_button.pack(side="left", padx=5)
        
        self.back_button = tk.Button(rowFrame2, text="Main Menu", command=lambda: self.returnToMain(switch_callback))
        self.back_button.pack(side="left", padx=5)

        self.scroll_canvas.pack_forget()
        self.scrollbar.pack_forget()
    
    def update_scroll(self, event=None):
        self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all"))
        self.scroll_canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def capturePhoto(self, switch_callback):
        self.captured = True
        self.capture_button.config(text="Predict")
        self.back_button.config(text="Back")
        self.capture_button.config(command=lambda: self.confirmPhoto(switch_callback))
        self.back_button.config(command=lambda: self.cancelPhoto(switch_callback))

    def confirmPhoto(self, switch_callback):
        self.scroll_canvas.pack(side="left", fill="both", expand=True, padx=20)
        self.scrollbar.pack(side="right", fill="y")
        self.capture_button.config(text="Save")
        self.capture_button.config(command=lambda: self.savePhoto(switch_callback))
        self.back_button.config(text="Capture Again")

    def savePhoto(self, switch_callback):
        timestamp = int(time.time())
        save_path = os.path.join(directory, f"image_{timestamp}.jpg")

        ret, frame = self.cap.read()
        if ret:
            cv2.imwrite(save_path, frame)
            self.analysis.config(text=f"Saved to: {save_path}")

    
    def cancelPhoto(self, switch_callback):
        self.captured = False
        self.update_frame()
        self.analysis_box.pack_forget()
        self.capture_button.config(text="Capture")
        self.capture_button.config(command=lambda: self.capturePhoto(switch_callback))
        self.back_button.config(text="Main Menu")
        self.back_button.config(command=lambda: switch_callback("mainFrame"))
        self.scroll_canvas.pack_forget()
        self.scrollbar.pack_forget()
    
    def draw_tiles(self, event=None):
        self.canvas.delete("bg")
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        target_width = self.variants[0].width()
        target_height = self.variants[0].height()
        center_width = canvas_width // (2 * target_width)
        center_height = canvas_height // (2 * target_height)
        max_dist = math.hypot(center_width, center_height)

        for ix, x in enumerate(range(0, canvas_width, target_width)):
            for iy, y in enumerate(range(0, canvas_height, target_height)):
                dist_tiles = max(abs(ix - center_width), abs(iy - center_height))
                idx = min(dist_tiles, len(self.variants) - 1)
                tile = self.variants[idx]
                self.canvas.create_image(x, y, image=tile, anchor="nw", tags="bg")
    
    def update_frame(self):
        if not self.captured:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)

                self.camera_frame.imgtk = imgtk
                self.camera_frame.configure(image=imgtk)

            self.after(10, self.update_frame)

    def returnToMain(self, switch_callback):
        self.cap.release()
        switch_callback("mainFrame")

    def on_closing(self):
        self.cap.release()
        self.root.destroy()