from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import numpy as np


class APP():
    def __init__(self):
        self.on1 = False
        self.on2 = False
        self.window = Tk()
        self.window.title("WaterMark Program")
        self.window.minsize(width=400, height=370)
        self.window.config(padx=0, pady=0)
        #inser_theme_img_______________________________________#
        self.canvas = Canvas(self.window, width=400, height=200, highlightthickness=0)
        self.bg_image = PhotoImage(file="logo.png")
        self.canvas.create_image(200, 100, image=self.bg_image)
        self.canvas.grid(column=0, row=0, columnspan=2,pady=5)
        # ___________upload_image_________________________________________#
        self.button = Button(text="Upload your image", command=self.upload_image, width=20)
        self.button.grid(row=1, column=1)
        self.path_entry = Entry(width=30)
        self.path_entry.insert(END, string="path")  # starting string
        self.path_entry.grid(row=1, column=0)
        # ___________radio_button________________________________________#
        self.var1 = IntVar()
        self.r1 = Radiobutton(self.window, text='Logo', variable=self.var1, value=1, command=self.different_function)
        self.r1.grid(row=2, column=0)
        self.r2 = Radiobutton(self.window, text='Text', variable=self.var1, value=2, command=self.different_function)
        self.r2.grid(row=2, column=1)

    def upload_image(self):
        filePath = filedialog.askopenfilename(initialdir="C:/Users/DUAN/Desktop", title="Select file", filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
        self.path_entry.config(state='normal')
        self.path_entry.delete(0, 'end')
        self.path_entry.insert(END, string=filePath)
        self.path_entry.config(state='disabled')

    def upload_logo(self):
        filePath = filedialog.askopenfilename(initialdir="C:/Users/DUAN/Desktop", title="Select file", filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
        self.w_path_entry.config(state='normal')
        self.w_path_entry.delete(0, 'end')
        self.w_path_entry.insert(END, string=filePath)
        self.w_path_entry.config(state='disabled')


    def image_add_watermark(self):
        back_im = Image.open(self.path_entry.get())
        # when rotation is needed
        # if back_im.size[0] > back_im.size[1]:
        #     back_im = back_im.rotate(-90, Image.NEAREST, expand=1)
        back_im.convert("RGBA")
        watermark = Image.open(self.w_path_entry.get()).convert("RGBA")
        # Resize the watermark if necessary
        watermark = watermark.resize((int(back_im.width/5), int(back_im.height/5)))
        # numpy is easier to operate, so once in numpy
        watermark = np.array(watermark)
        alpha = 255# changed alpha channel value 0-255
        watermark[watermark[..., 3] != 0, 3] = alpha
        watermark = Image.fromarray(watermark)
        # Paste the watermark  # Second watermark makes it transparent
        back_im.paste(watermark, (int(back_im.width-(back_im.width/5)), int(back_im.height-(back_im.height/5))),watermark)
        self.w_path_entry.config(state='normal')
        self.w_path_entry.delete(0, 'end')
        self.w_path_entry.config(state='disabled')
        self.save_image(back_im)


    def add_text_on_image(self):
        image = Image.open(self.path_entry.get())
        back_im = image.copy()
        draw = ImageDraw.Draw(back_im)
        text = self.text_entry.get()
        font = ImageFont.truetype('arial.ttf', 72)
        textwidth, textheight = draw.textsize(text, font)

        margin = 10
        # draw watermark in the bottom right corner
        draw.text(((back_im.width - textwidth - margin), (back_im.height - textheight - margin)), text, font=font)
        self.text_entry.delete(0, 'end')
        self.save_image(back_im)

    def different_function(self):
        # ___________upload_logo_________________________________________#
        self.clean()
        if self.var1.get() == 1:
            self.button_w = Button(text="Upload your logo", command=self.upload_logo, width=20)
            self.button_w.grid(row=3, column=1)

            self.w_path_entry = Entry(width=30)
            self.w_path_entry.insert(END, string="watermark path")  # starting string
            self.w_path_entry.grid(row=3, column=0)

            # save new_image________________________________________________#
            self.button_save = Button(text="Save image with watermark", command=self.image_add_watermark)
            self.button_save.grid(row=4, column=0, columnspan=2, pady=20)
            self.on1 = True

        elif self.var1.get() == 2:
            # text
            self.text_entry = Entry(width=54)
            self.text_entry.insert(END, string="text")  # starting string
            self.text_entry.grid(row=3, column=0, columnspan=2,pady=3)
            self.button_save2 = Button(text="Save image with watermark", command=self.add_text_on_image)
            self.button_save2.grid(row=4, column=0, columnspan=2, pady=21)
            self.on2 = True

    def clean(self):
        if self.on1:
            self.button_w.grid_forget()
            self.w_path_entry.grid_forget()
            self.button_save.grid_forget()
            self.on1 = False

        elif self.on2:
            self.text_entry.grid_forget()
            self.button_save2.grid_forget()
            self.on1 = False

    def save_image(self, back_im):
        # _____save_path____________________#
        directory = filedialog.askdirectory(initialdir="C:/Users/DUAN/Desktop")
        save_path = directory + "/watermark.jpg"
        # _____save_image___________________#
        back_im.save(save_path, quality=100)
        self.path_entry.config(state='normal')
        self.path_entry.delete(0, 'end')
        self.path_entry.config(state='disabled')
        messagebox.showinfo(title="Save Image", message=("The image is saved in following path;\n" + save_path))


if __name__ == "__main__":
    app = APP()
    app.window.mainloop()
