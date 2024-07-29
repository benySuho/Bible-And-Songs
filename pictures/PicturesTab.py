import ttkbootstrap as tb
import tkinter as tk
from PIL import ImageTk, Image
import os

class PicturesTab(tb.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.pack(fill='both', expand=True)
        self.controller = controller
        self.master = master
        self.pictures = [file for file in os.listdir('Images')]
        self.image = None
        self.scale = 1

        #  Left panel
        self.leftFrame = tb.Frame(master=self, width=300, height=600)
        self.leftFrame.pack(fill=tb.Y, side=tb.LEFT, expand=False)

        self.input_picture = tk.StringVar()
        # creating text box
        e = tb.Entry(self.leftFrame, textvariable=self.input_picture)
        e.pack(fill=tb.BOTH)
        e.bind('<KeyRelease>', self.checkkey)
        e.bind('<Return>', self.choose_picture)

        # creating list box
        self.lb = tk.Listbox(self.leftFrame)
        self.lb.pack(fill=tb.BOTH, expand=True)
        self.update_box(self.pictures, self.lb)
        self.lb.bind('<Double-Button-1>', self.choose_picture)
        self.lb.bind('<Return>', self.choose_picture)

        self.right_frame = tb.Frame(master=self)
        self.right_frame.pack(fill=tb.BOTH, side=tb.RIGHT, expand=True)
        self.top_frame = tb.Frame(self.right_frame)
        self.top_frame.pack()

        self.bottom_frame = tb.Frame(self.right_frame)
        self.bottom_frame.pack(side=tk.BOTTOM)

        but2 = tb.Button(self.bottom_frame, text="הסתר תצוגה", command=self.hide_second_screen)
        but2.grid(row=0, column=1, sticky=tk.NSEW, padx=2, pady=2)
        but = tb.Button(self.bottom_frame, text="הצג", command=self.show_picture_second_screen, bootstyle='success')
        but.grid(row=0, column=2, sticky=tk.NSEW, padx=2, pady=2)
        but2 = tb.Button(self.bottom_frame, text="+", command=self.scale_increase)
        but2.grid(row=0, column=3, sticky=tk.NSEW, padx=2, pady=2)
        but = tb.Button(self.bottom_frame, text="איפוס", command=self.scale_reset)
        but.grid(row=0, column=4, sticky=tk.NSEW, padx=2, pady=2)
        but = tb.Button(self.bottom_frame, text="-", command=self.scale_decrease)
        but.grid(row=0, column=5, sticky=tk.NSEW, padx=2, pady=2)

        self.right_frame.bind("<MouseWheel>", self.on_mouse_wheel)

    def hide_second_screen(self):
        self.controller.hide()

    def show_picture_second_screen(self):
        if self.image:
            self.controller.show_picture(self.image, self.scale)

    def show_picture(self):
        if not self.image:
            return
        for widget in self.top_frame.winfo_children():
            widget.destroy()
        height = self.right_frame.winfo_height() - self.bottom_frame.winfo_reqheight()
        width = self.right_frame.winfo_width()
        if height < self.image.height or width < self.image.width:
            auto_scale = min(height / self.image.height, width / self.image.width)
        else:
            auto_scale = 1

        resize_image = self.image.resize((int(self.image.width * auto_scale * self.scale),
                                          int(self.image.height * auto_scale * self.scale)))
        if self.scale > 1:
            left = int((resize_image.width - width) / 2)
            if left < 0:
                left = 0
            right = left + width
            top = int((resize_image.height - height) / 2)
            if top < 0:
                top = 0
            bottom = top + height
            resize_image = resize_image.crop((left, top, right, bottom))
        self.img = ImageTk.PhotoImage(resize_image)

        # Create a Label Widget to display the text or Image
        label = tk.Label(self.top_frame, image=self.img, borderwidth=0)
        label.pack()
        label.bind("<MouseWheel>", self.on_mouse_wheel)

    def update_box(self, data, lb):
        # clear previous data
        lb.delete(0, 'end')

        # put new data
        for item in data:
            lb.insert('end', item)

    def checkkey(self, event):
        value = event.widget.get()
        source = value.split()
        if value == '':
            data = self.pictures
        else:
            data = []
            for item in self.pictures:
                if source[0].lower() in item.lower():
                    data.append(item)

        # update data in listbox
        self.update_box(data, self.lb)

    def choose_picture(self, event):
        try:
            self.image = Image.open(f"Images/{self.lb.get(tk.ACTIVE)}")
        except:
            return
        self.show_picture()
        if self.controller.picture_active():
            self.show_picture_second_screen()

    def scale_increase(self):
        self.scale = self.scale + 0.1
        self.show_picture()
        if self.controller.picture_active():
            self.show_picture_second_screen()

    def scale_decrease(self):
        self.scale = self.scale - 0.1
        if self.scale < 0.1:
            self.scale = 0.1
        self.show_picture()
        if self.controller.picture_active():
            self.show_picture_second_screen()

    def scale_reset(self):
        self.scale = 1
        self.show_picture()
        if self.controller.picture_active():
            self.show_picture_second_screen()

    def on_mouse_wheel(self, event):
        if event.delta > 0:
            self.scale_increase()
        elif event.delta < 0:
            self.scale_decrease()
