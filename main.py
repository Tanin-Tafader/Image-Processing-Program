import tkinter as tk
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageFilter

# Define filter functions
def cool_filter(img_arr):
    blue_channel = img_arr[:, :, 2]
    blue_channel[blue_channel < 50] = 0
    blue_channel[blue_channel >= 50] -= 50
    img_arr[:, :, 0] += 25
    img_arr[:, :, 1] += 10
    img_arr[:, :, 2] = blue_channel
    return img_arr

def hot_filter(img_arr):
    red_channel = img_arr[:, :, 0]
    red_channel[red_channel < 50] = 0
    red_channel[red_channel >= 50] -= 50
    img_arr[:, :, 0] = red_channel
    img_arr[:, :, 1] += 25
    img_arr[:, :, 2] += 10
    return img_arr

def blues_filter(img_arr):
    blue_channel = img_arr[:, :, 2]
    blue_channel[blue_channel < 50] = 0
    blue_channel[blue_channel >= 50] -= 50
    img_arr[:, :, 0] += 10
    img_arr[:, :, 1] += 25
    img_arr[:, :, 2] = blue_channel
    return img_arr

# Define blur functions
def blur_effect1(img_arr):
    kernel = np.ones((5, 5)) / 25
    img_arr = np.apply_along_axis(lambda m: np.convolve(m, kernel, mode='same'), axis=0, arr=img_arr)
    img_arr = np.apply_along_axis(lambda m: np.convolve(m, kernel, mode='same'), axis=1, arr=img_arr)
    return img_arr

def blur_effect2(img_arr):
    img_blur = Image.fromarray(img_arr)
    img_blur = img_blur.filter(ImageFilter.BLUR)
    img_arr = np.array(img_blur)
    return img_arr

def blur_effect3(img_arr):
    kernel = np.ones((10, 10)) / 100
    img_arr = np.apply_along_axis(lambda m: np.convolve(m, kernel, mode='same'), axis=0, arr=img_arr)
    img_arr = np.apply_along_axis(lambda m: np.convolve(m, kernel, mode='same'), axis=1, arr=img_arr)
    return img_arr

# Define threshold function
def threshold(img_arr, threshold_value):
    img_arr[img_arr < threshold_value] = 0
    img_arr[img_arr >= threshold_value] = 255
    return img_arr

class ImageProcessingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processing")
        self.img = None
        self.img_arr = None
        self.img_original = None

        # Create widgets
        self.btn_open = tk.Button(self.root, text="Open Image", command=self.open_image)
        self.btn_cool_filter = tk.Button(self.root, text="Cool Filter", state=tk.DISABLED, command=self.apply_cool_filter)
        self.btn_hot_filter = tk.Button(self.root, text="Hot Filter", state=tk.DISABLED, command=self.apply_hot_filter)
        self.btn_blur1 = tk.Button(self.root, text="Blur Effect 1", state=tk.DISABLED, command=self.apply_blur1)
        self.btn_blur2 = tk.Button(self.root, text="Blur Effect 2", state=tk.DISABLED, command=self.apply_blur2)
        self.btn_blur3 = tk.Button(self.root, text="Blur Effect 3", state=tk.DISABLED, command=self.apply_blur3)
        self.btn_threshold = tk.Button(self.root, text="Threshold", state=tk.DISABLED, command=self.apply_threshold)
        self.btn_revert = tk.Button(self.root, text="Revert", state=tk.DISABLED, command=self.revert_changes)
        self.btn_save = tk.Button(self.root, text="Save Image", state=tk.DISABLED, command=self.save_image)
        self.canvas = tk.Canvas(self.root, width=500, height=500)

        # Grid layout
        self.btn_open.grid(row=0, column=0, padx=10, pady=10)
        self.btn_cool_filter.grid(row=0, column=1, padx=10, pady=10)
        self.btn_hot_filter.grid(row=0, column=2, padx=10, pady=10)
        self.btn_blur1.grid(row=1, column=0, padx=10, pady=10)
        self.btn_blur2.grid(row=1, column=1, padx=10, pady=10)
        self.btn_blur3.grid(row=1, column=2, padx=10, pady=10)
        self.btn_threshold.grid(row=2, column=0, padx=10, pady=10)
        self.btn_revert.grid(row=2, column=1, padx=10, pady=10)
        self.btn_save.grid(row=2, column=2, padx=10, pady=10)
        self.canvas.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

    def open_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.img = Image.open(file_path)
            self.img_original = np.array(self.img)
            self.img_arr = np.array(self.img)
            self.show_image()
            self.enable_buttons()

    def show_image(self):
        plt.imshow(self.img_arr)
        plt.axis('off')
        plt.tight_layout()
        self.canvas.delete("all")
        self.canvas.get_tk_widget().pack_forget()
        self.canvas = FigureCanvasTkAgg(plt.gcf(), master=self.root)
        self.canvas.get_tk_widget().pack()

    def enable_buttons(self):
        self.btn_cool_filter.config(state=tk.NORMAL)
        self.btn_hot_filter.config(state=tk.NORMAL)
        self.btn_blur1.config(state=tk.NORMAL)
        self.btn_blur2.config(state=tk.NORMAL)
        self.btn_blur3.config(state=tk.NORMAL)
        self.btn_threshold.config(state=tk.NORMAL)

    def apply_cool_filter(self):
        self.img_arr = cool_filter(self.img_arr)
        self.show_image()

    def apply_hot_filter(self):
        self.img_arr = hot_filter(self.img_arr)
        self.show_image()

    def apply_blur1(self):
        self.img_arr = blur_effect1(self.img_arr)
        self.show_image()

    def apply_blur2(self):
        self.img_arr = blur_effect2(self.img_arr)
        self.show_image()

    def apply_blur3(self):
        self.img_arr = blur_effect3(self.img_arr)
        self.show_image()

    def apply_threshold(self):
        threshold_value = 128
        self.img_arr = threshold(self.img_arr, threshold_value)
        self.show_image()

    def revert_changes(self):
        self.img_arr = self.img_original.copy()
        self.show_image()

    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".jpg")
        if file_path:
            img_save = Image.fromarray(self.img_arr)
            img_save.save(file_path)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessingGUI(root)
    app.run()