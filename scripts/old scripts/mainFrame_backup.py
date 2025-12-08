import math
import customtkinter as ctk
import numpy as np
from PIL import Image, ImageTk, ImageEnhance

class mainFrame(ctk.CTkFrame):
    def __init__(self, master, switch_callback):
        super().__init__(master)

        self.tile_img = Image.open("./sprites/Grey_background_13.png")
        self.variants = []
        for brightness in np.linspace(1.5, 1.0, 15):
            self.altered_tile = ImageEnhance.Brightness(self.tile_img).enhance(brightness)
            self.variants.append(ImageTk.PhotoImage(self.altered_tile))
        self.canvas = ctk.CTkCanvas(self, highlightthickness=0, borderwidth=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self.draw_tiles)

        screen_width = int(self.winfo_screenwidth()/2)
        screen_height = int(self.winfo_screenheight()/2)
        center_frame = ctk.CTkFrame(self.canvas, width=screen_width, height=screen_height, corner_radius=20)
        center_frame.place(relx="0.5", rely="0.5", anchor="center")
        
        label = ctk.CTkLabel(center_frame, text="Logo", font=("Arial", 24))
        label.pack(pady="10px", padx="60px")
        
        button = ctk.CTkButton(center_frame, text="Camera", command=lambda: switch_callback("cameraFrame"))
        button.pack(pady="10px")

        button = ctk.CTkButton(center_frame, text="Files", command=lambda: switch_callback("filesFrame"))
        button.pack(pady="10px")
    
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
