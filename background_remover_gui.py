#!/usr/bin/env python3

import tkinter as tk
from tkinter import messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageTk
import os
import sys


class BackgroundRemoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Background Remover")
        self.root.geometry("400x500")
        self.root.resizable(False, False)

        self.current_image_path = None
        self.preview_image = None
        self.threshold_value = 255

        self._create_widgets()

    def _create_widgets(self):
        self.drop_frame = tk.Frame(
            self.root,
            width=350,
            height=300,
            bg="#f0f0f0",
            relief=tk.RIDGE,
            borderwidth=2
        )
        self.drop_frame.pack(pady=20, padx=25)
        self.drop_frame.pack_propagate(False)

        self.drop_frame.drop_target_register(DND_FILES)
        self.drop_frame.dnd_bind('<<Drop>>', self._on_drop)

        self.hint_label = tk.Label(
            self.drop_frame,
            text="Drag and drop\nan image here",
            font=("Arial", 12),
            bg="#f0f0f0",
            fg="#888888"
        )
        self.hint_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.preview_label = tk.Label(self.drop_frame, bg="#f0f0f0")
        self.preview_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.slider_frame = tk.Frame(self.root)
        self.slider_frame.pack(pady=10)

        self.slider_label = tk.Label(
            self.slider_frame,
            text="White transparency: 0%",
            font=("Arial", 10)
        )
        self.slider_label.pack()

        self.threshold_slider = tk.Scale(
            self.slider_frame,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            length=300,
            command=self._update_threshold,
            showvalue=False
        )
        self.threshold_slider.set(0)
        self.threshold_slider.pack()

        self.process_button = tk.Button(
            self.root,
            text="Remove Background",
            font=("Arial", 12, "bold"),
            command=self._process_image,
            width=25,
            height=2,
            bg="#2196F3",
            fg="white",
            cursor="hand2",
            state=tk.DISABLED
        )
        self.process_button.pack(pady=15)

    def _update_threshold(self, value):
        percentage = int(value)
        self.threshold_value = int(255 - (255 * percentage / 100))
        self.slider_label.config(text=f"White transparency: {percentage}%")

    def _on_drop(self, event):
        file_path = event.data

        if file_path.startswith('{') and file_path.endswith('}'):
            file_path = file_path[1:-1]

        self._load_image(file_path)

    def _load_image(self, file_path):
        try:
            if not os.path.exists(file_path):
                messagebox.showerror("Error", f"File not found:\n{file_path}")
                return

            img = Image.open(file_path)

            self.current_image_path = file_path

            img.thumbnail((320, 270), Image.Resampling.LANCZOS)

            self.preview_image = ImageTk.PhotoImage(img)

            self.hint_label.place_forget()
            self.preview_label.config(image=self.preview_image)
            self.preview_label.image = self.preview_image

            self.process_button.config(state=tk.NORMAL)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image:\n{str(e)}")

    def _process_image(self):
        if not self.current_image_path:
            messagebox.showwarning("Warning", "Please select an image first")
            return

        try:
            self.process_button.config(state=tk.DISABLED, text="Processing...")
            self.root.update()

            img = Image.open(self.current_image_path)

            grayscale = img.convert("L")
            gray_data = grayscale.getdata()

            result = Image.new("RGBA", img.size)
            new_data = []

            for gray_value in gray_data:
                if gray_value >= self.threshold_value:
                    alpha = 0
                else:
                    alpha = 255 - gray_value
                new_data.append((0, 0, 0, alpha))

            result.putdata(new_data)

            base_name = os.path.splitext(self.current_image_path)[0]
            output_path = f"{base_name}_transparent.png"

            result.save(output_path, "PNG", optimize=True)

            self.process_button.config(state=tk.NORMAL, text="Remove Background")

            messagebox.showinfo(
                "Done",
                f"Saved: {os.path.basename(output_path)}"
            )

        except Exception as e:
            self.process_button.config(state=tk.NORMAL, text="Remove Background")
            messagebox.showerror("Error", f"Failed to process image:\n{str(e)}")


def main():
    try:
        root = TkinterDnD.Tk()
        app = BackgroundRemoverApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Startup error: {e}")
        print("\ntkinterdnd2 module may not be installed")
        print("Install it: pip install tkinterdnd2")
        input("\nPress Enter to exit...")
        sys.exit(1)


if __name__ == "__main__":
    main()
