import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class ImageCropper(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Image Cropper")
        self.geometry("800x600")

        self.image = None
        self.image_path = None
        self.canvas = tk.Canvas(self, cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.rect = None
        self.start_x = None
        self.start_y = None
        self.cur_x = None
        self.cur_y = None

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        menubar = tk.Menu(self)
        self.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", command=self.open_image)
        file_menu.add_command(label="Save", command=self.save_image)
        file_menu.add_command(label="Exit", command=self.quit)

    def open_image(self):
        self.image_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
        )
        if not self.image_path:
            return
        self.image = Image.open(self.image_path)
        self.display_image(self.image)

    def save_image(self):
        if self.rect:
            x1, y1, x2, y2 = self.canvas.coords(self.rect)
            cropped_image = self.image.crop((x1, y1, x2, y2))
            save_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("PDF files", "*.pdf"), ("All files", "*.*")]
            )
            if save_path:
                file_extension = save_path.split('.')[-1].lower()
                if file_extension in ['jpg', 'jpeg']:
                    cropped_image.save(save_path, 'JPEG')
                elif file_extension == 'png':
                    cropped_image.save(save_path, 'PNG')
                elif file_extension == 'pdf':
                    cropped_image.convert('RGB').save(save_path, 'PDF')
                else:
                    messagebox.showerror("Unsupported Format", "Unsupported file format. Please choose JPG, PNG, or PDF.")

    def display_image(self, image):
        self.canvas.delete("all")
        self.tk_image = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def on_button_press(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        if not self.rect:
            self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red')

    def on_mouse_drag(self, event):
        self.cur_x, self.cur_y = (self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        self.canvas.coords(self.rect, self.start_x, self.start_y, self.cur_x, self.cur_y)

    def on_button_release(self, event):
        pass

if __name__ == "__main__":
    app = ImageCropper()
    app.mainloop()

