import tkinter as tk
from tkinter import messagebox as mb
from tkinter import ttk
import projector_screen.getScreenInfo as screenInfo
from PIL import ImageTk


class SecondWindow(tk.Toplevel):
    def __init__(self):
        self.size = screenInfo.get_second_screen_info()
        super().__init__()
        if not self.size:
            mb.showerror(title="Error", message="Second screen not found")
            self.size = (800, 600, 500, 100)
        else:
            self.overrideredirect(True)
            self.focus_set()  # Restricted access main menu
        self.geometry('%dx%d+%d+%d' % self.size)
        self.configure(background='black')
        self.default_white_background = False
        self.song_active = False
        self.verses_active = False
        self.picture_active = False
        self.verse_text = ""
        self.effective_size = (self.size[0], self.size[1], 0, 0)
        self.effective_area = tk.Frame(self, bg='white', background="white",
                                       width=self.effective_size[0], height=self.effective_size[1])
        self.place_effective_area()
        self.text_font = [["Helvetica", 30], 'black']
        self.songs_fonts = {'songs_fonts_lan': [["Helvetica", 30], 'black'],
                            'songs_fonts_tra': [["Helvetica", 22, "italic"], 'red'],
                            'songs_fonts_heb': [["Helvetica", 30], 'black']}
        self.in_set = False
        self.auto_adjustment = True

    def song_activate(self):
        self.effective_area.configure(bg='white')
        self.verses_active = False
        self.picture_active = False
        self.song_active = True

    def verses_activate(self):
        self.effective_area.configure(bg='white')
        self.verses_active = True
        self.song_active = False
        self.picture_active = False

    def picture_activate(self):
        self.effective_area.configure(bg='black')
        self.verses_active = False
        self.song_active = False
        self.picture_active = True

    def destroy_widgets(self):
        for widget in self.effective_area.winfo_children():
            widget.destroy()

    def hide_second_screen(self):
        self.verses_active = False
        self.song_active = False
        self.picture_active = False
        if self.default_white_background:
            self.effective_area.configure(bg='white')
        else:
            self.effective_area.configure(bg='black')
        self.configure(background='black')
        self.destroy_widgets()

    def show_text(self, text, *args):
        self.verse_text = text
        self.destroy_widgets()
        self.verses_activate()
        self.text_label = ttk.Label(self.effective_area, text=text, font=self.text_font[0],
                                    wraplength=self.effective_size[0] - 40, background="white",
                                    foreground=self.text_font[1])
        self.text_label.configure(justify=tk.CENTER)
        self.text_label.place(x=((self.effective_size[0] - self.text_label.winfo_reqwidth()) / 2), y=20)
        if self.auto_adjustment:
            size = self.text_font[0][1]
            while True:
                if self.text_label.winfo_reqheight() < self.effective_size[1] - 19:
                    return
                size = int(size) - 1
                new_font = self.text_font[0][:]
                new_font[1] = size
                self.text_label.configure(font=new_font)

    def show_slide(self, text):
        self.song_activate()
        self.destroy_widgets()
        self.print_slide(self.effective_area, text)

    def show_picture(self, image, scale=1):
        if not self.picture_active:
            self.picture_activate()
        self.destroy_widgets()
        width = self.effective_size[0]
        height = self.effective_size[1]
        if width < image.width or height < image.height:
            auto_scale = min(width / image.width, height / image.height)
            width = int(image.width * auto_scale * scale)
            height = int(image.height * auto_scale * scale)
        else:
            height = int(image.height * scale)
            width = int(image.width * scale)

        resize_image = image.resize((width, height))
        self.img = ImageTk.PhotoImage(resize_image)

        # Create a Label Widget to display the text or Image
        label = tk.Label(self.effective_area, image=self.img, borderwidth=0)
        label.configure(justify=tk.CENTER)
        label.place(x=((self.effective_size[0] - label.winfo_reqwidth()) / 2),
                    y=((self.effective_size[1] - label.winfo_reqheight()) / 2))

    def set_effective_area(self):
        if self.in_set:
            return
        self.in_set = True
        self.first_coordinate = None
        self.canvas = tk.Canvas(self)
        self.canvas.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        self.bind('<Button-1>', self.button)

    def button(self, event):
        x, y = event.x, event.y
        if not self.first_coordinate:
            self.first_coordinate = (x, y)
            self.bind('<Motion>', self.motion)
        else:
            self.canvas.destroy()
            self.effective_size = (abs(self.first_coordinate[0] - x), abs(self.first_coordinate[1] - y),
                                   min(self.first_coordinate[0], x), min(self.first_coordinate[1], y))
            self.place_effective_area()
            if self.verses_active:
                self.show_text(self.verse_text)
            del self.first_coordinate
            self.unbind('<Button-1>')
            self.unbind('<Motion>')
            self.in_set = False

    def motion(self, event):
        x, y = event.x, event.y
        self.canvas.delete("all")
        self.canvas.create_rectangle(self.first_coordinate[0], self.first_coordinate[1], x, y, fill='red')

    def print_slide(self, song_window, text):
        frame1 = tk.Frame(master=song_window, bg="white", padx=20, pady=20)
        frame1.place(relx=0, rely=0, relheight=1, relwidth=0.34)
        frame2 = tk.Frame(master=song_window, bg="white", pady=20)
        frame2.place(relx=0.33, rely=0, relheight=1, relwidth=0.32)
        frame3 = tk.Frame(master=song_window, bg="white", padx=20, pady=20)
        frame3.place(relx=0.67, rely=0, relheight=1, relwidth=0.34)

        try:
            label2 = ttk.Label(master=frame2, text="\n".join(text[0]), background="white",
                               font=self.songs_fonts['songs_fonts_heb'][0],
                               foreground=self.songs_fonts['songs_fonts_heb'][1],
                               wraplength=(song_window.winfo_reqwidth() // 3 - 20),
                               justify=tk.CENTER)
            label2.pack()
        except:
            pass

        loop = True
        i = 0
        while loop:
            loop = False
            try:
                label11 = ttk.Label(master=frame1, text=text[1][i],
                                    foreground=self.songs_fonts['songs_fonts_lan'][1],
                                    background="white", font=self.songs_fonts['songs_fonts_lan'][0],
                                    wraplength=(song_window.winfo_reqwidth() // 3 - 40))
                label11.pack(anchor="w")
                loop = True
            except:
                pass
            try:
                label12 = ttk.Label(master=frame1, text=" " + text[3][i],
                                    foreground=self.songs_fonts['songs_fonts_tra'][1],
                                    background="white", font=self.songs_fonts['songs_fonts_tra'][0],
                                    wraplength=(song_window.winfo_reqwidth() // 3 - 40))
                label12.pack(anchor="w")
                loop = True
            except:
                pass
            try:
                label31 = ttk.Label(master=frame3, text=text[2][i],
                                    foreground=self.songs_fonts['songs_fonts_lan'][1],
                                    background="white", font=self.songs_fonts['songs_fonts_lan'][0],
                                    wraplength=(song_window.winfo_reqwidth() // 3 - 40))
                label31.pack(anchor="w")
                loop = True
            except:
                pass
            try:
                label32 = ttk.Label(master=frame3, text=" " + text[4][i],
                                    foreground=self.songs_fonts['songs_fonts_tra'][1],
                                    background="white", font=self.songs_fonts['songs_fonts_tra'][0],
                                    wraplength=(song_window.winfo_reqwidth() // 3 - 40))
                label32.pack(anchor="w")
                loop = True
            except:
                pass
            i += 1

    def get_settings(self):
        return {'text_font': self.text_font, 'songs_fonts_heb': self.songs_fonts['songs_fonts_heb'],
                'songs_fonts_tra': self.songs_fonts['songs_fonts_tra'],
                'songs_fonts_lan': self.songs_fonts['songs_fonts_lan'],
                'effective_size': self.effective_size,
                'auto_adjustment': self.auto_adjustment, 'song_active': self.song_active,
                'verses_active': self.verses_active, 'picture_active': self.picture_active,
                'default_white_background': self.default_white_background}

    def set_settings(self, settings):
        if 'text_font' in settings.keys():
            self.text_font = settings['text_font']
        if 'songs_fonts_heb' in settings.keys():
            self.songs_fonts['songs_fonts_heb'] = settings['songs_fonts_heb']
        if 'songs_fonts_tra' in settings.keys():
            self.songs_fonts['songs_fonts_tra'] = settings['songs_fonts_tra']
        if 'songs_fonts_lan' in settings.keys():
            self.songs_fonts['songs_fonts_lan'] = settings['songs_fonts_lan']
        if 'auto_adjustment' in settings.keys():
            self.auto_adjustment = settings['auto_adjustment']
        if 'effective_size' in settings.keys():
            self.effective_size = settings['effective_size']
            self.place_effective_area()
        if 'song_active' in settings.keys():
            self.song_active = settings['song_active']
        if 'verses_active' in settings.keys():
            self.verses_active = settings['verses_active']
        if 'pictures_active' in settings.keys():
            self.picture_active = settings['picture_active']
        if 'default_white_background' in settings.keys():
            self.default_white_background = settings['default_white_background']

    def place_effective_area(self):
        self.effective_area.configure(width=self.effective_size[0], height=self.effective_size[1])
        self.effective_area.place(x=self.effective_size[2], y=self.effective_size[3])
