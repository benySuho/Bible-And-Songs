import tkinter as tk
from ttkbootstrap.scrolled import ScrolledFrame
from songs_control.MiniSlide import MiniSlide


class SlidesMiniShow(ScrolledFrame):
    def __init__(self, master, songs, font=None, command_show=None, command_active=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.songs_names = []  # List to store the loaded page images
        self.command_show = command_show
        self.command_active = command_active
        self.songs = songs
        self.font = font
        self.active_slide = {'name': None, 'number': None, 'slide': None}

        self.master.bind("<Configure>", self.update_grid)  # Bind window resize event to rearrange mini slides
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def update_songs(self, songs, active_slide=None):
        self.active_slide = active_slide
        self.songs = songs
        self.update_grid()

    def update_grid(self, event=None):
        self.update_idletasks()
        width = 15 * int(self.font[1])
        for widget in self.winfo_children():
            widget.destroy()
        available_width = self.winfo_width() - 15
        max_cols = max(1, available_width // width)

        row = 0
        index = 0
        row_frame = tk.Frame(self)
        row_frame.grid_columnconfigure(list(range(max_cols)), minsize=width, uniform='True', weight=1)
        for song in self.songs:
            if len(self.songs[song]) == 0:
                continue
            slide_index = 0
            for slide in self.songs[song]:
                if len(slide) == 0:
                    continue
                text = "\n".join(slide[0])
                ms = MiniSlide(row_frame, song, slide_index, text, font=self.font,
                               command_active=self.set_active, command_show=self.set_active_show)
                ms.grid(row=0, column=index % max_cols, sticky=tk.NSEW, padx=4, pady=4)
                if song == self.active_slide['name'] and slide_index == self.active_slide['number']:
                    self.active_slide['slide'] = ms
                    ms.configure(bg='sky blue')
                    ms.label.configure(bg='sky blue')
                index += 1
                slide_index += 1
                if index % max_cols == 0:
                    row += 1
                    self.rowconfigure(row, weight=1)
                    row_frame.pack(side=tk.TOP, fill=tk.X)
                    row_frame = tk.Frame(self)
                    row_frame.grid_columnconfigure(list(range(max_cols)), minsize=width, uniform='True', weight=1)

        row_frame.pack(side=tk.TOP, fill=tk.X)

    def set_active(self, slide=None, name=None, number=None):
        if self.active_slide['slide']:
            self.active_slide['slide'].configure(bg='#ffffff')
            self.active_slide['slide'].label.configure(bg='#ffffff')
        if slide:
            slide.configure(bg='sky blue')
            slide.label.configure(bg='sky blue')
        self.active_slide = {'name': name, 'number': number, 'slide': slide}
        self.command_active(name, number)

    def set_active_show(self, slide, name, number):
        self.set_active(slide, name, number)
        if self.command_show:
            self.command_show()

    def set_songs(self, songs):
        self.songs = songs
        self.update_grid()
