import tkinter as tk
import widgets.fonts_box as fbox
from widgets.dd_list import DragDropListbox as DDLB
from ttkbootstrap.scrolled import ScrolledFrame
from tkinter import ttk


class Settings(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.pack(fill='both', expand=True)
        self.controller = controller
        self.songs = controller.songs
        self.grid_columnconfigure(0, weight=1)
        self.interface_font = ['Helvetica', 10, 'roman', 'normal']

        self.main_frame = tk.Frame(self)
        # self.main_frame.vscroll.pack(side=tk.LEFT, fill=tk.Y)
        self.main_frame.pack(fill='both', expand=True)
        self.main_frame.columnconfigure(0, weight=1)

        self.fonts_frame = tk.Frame(self.main_frame)
        self.fonts_frame.grid(row=0, column=1, sticky=tk.NE)
        self.but = tk.Button(self.fonts_frame, text="בחר איזור תצוגה", command=self.set_effective_area, padx=10,
                             pady=10, font=self.interface_font[0])
        self.but.grid(row=0, column=0)
        self.interface_fbox = fbox.FontBox(self.fonts_frame, self.get_font_settings, self.set_font_settings,
                                           text='ממשק')
        self.interface_fbox.color_button['state'] = 'disabled'
        self.interface_fbox.grid(row=0, column=2, padx=3)
        self.verses_fbox = fbox.FontBox(self.fonts_frame, self.get_font_settings, self.set_font_settings, text='פסוקים')
        self.verses_fbox.grid(row=0, column=1, padx=3)
        self.songs_heb_fbox = fbox.FontBox(self.fonts_frame, self.get_font_settings, self.set_font_settings,
                                           text='שירים: עברית')
        self.songs_heb_fbox.grid(row=1, column=2, padx=3)
        self.songs_lan_fbox = fbox.FontBox(self.fonts_frame, self.get_font_settings, self.set_font_settings,
                                           text='שירים: אנגלית ורוסית')
        self.songs_lan_fbox.grid(row=1, column=1, padx=3)
        self.songs_tra_fbox = fbox.FontBox(self.fonts_frame, self.get_font_settings, self.set_font_settings,
                                           text='שירים: תרגום')
        self.songs_tra_fbox.grid(row=1, column=0, padx=3)

        self.verses_configurations = tk.Frame(self.main_frame,)
        self.verses_configurations.grid(row=0, column=0, sticky=tk.NE)
        # add check boxes
        self.verses_auto_adjustment = tk.BooleanVar()
        self.white_background = tk.BooleanVar()
        self.abbreviations = tk.BooleanVar()
        self.add_verses_configurations()

        self.translations_frame = tk.Frame(self.main_frame)
        self.translations_frame.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW)
        self.translations_frame.columnconfigure((0, 1), weight=1)
        tk.Label(self.translations_frame, text='תרגומים: תנ"ך').grid(row=0, column=1)
        tk.Label(self.translations_frame, text='תרגומים: ברית החדשה').grid(row=0, column=0)
        self.old_testament_order = DDLB(self.translations_frame,
                                        command_set=lambda x=None: self.set_translation_order('old'),
                                        command_update=lambda: self.set_translation_order('old'))
        self.old_testament_order.grid(row=1, column=1, sticky=tk.NSEW)
        self.new_testament_order = DDLB(self.translations_frame,
                                        command_set=lambda x=None: self.set_translation_order('new'),
                                        command_update=lambda: self.set_translation_order('new'))
        self.new_testament_order.grid(row=1, column=0, sticky=tk.NSEW)
        self.update_translation_order()

    def get_font_settings(self, topic=None):
        settings = self.controller.get_projector_settings()
        if topic == 'פסוקים':
            settings = settings['text_font']
        elif topic == 'ממשק':
            return [self.interface_font[0], self.interface_font[1], 'black',
                    self.interface_font[2],
                    self.interface_font[3]]
        elif 'שירים' in topic:
            if 'עברית' in topic:
                settings = settings['songs_fonts_heb']
            elif 'תרגום' in topic:
                settings = settings['songs_fonts_tra']
            else:
                settings = settings['songs_fonts_lan']
        else:
            return ['Helvetica', 8, 'black', 'roman', 'normal']
        return [settings[0][0], settings[0][1], settings[1], 'italic' if 'italic' in settings[0] else 'roman',
                'bold' if 'bold' in settings[0] else 'normal']

    def set_font_settings(self, settings):
        topic = settings[0]
        if topic == 'פסוקים':
            self.controller.set_projector_settings({'text_font': settings[1]})
        elif topic == 'ממשק':
            self.interface_font = settings[1][0]
            self.apply_interface_font()
        elif 'שירים' in topic:
            if 'שירים: עברית' == topic:
                self.controller.set_projector_settings({'songs_fonts_heb': settings[1]})
            elif 'תרגום' in topic:
                self.controller.set_projector_settings({'songs_fonts_tra': settings[1]})
            else:
                self.controller.set_projector_settings({'songs_fonts_lan': settings[1]})

    def set_effective_area(self):
        self.controller.set_effective_area()

    def apply_interface_font(self):
        self.controller.apply_interface_font(font=self.interface_font)

    def update_translation_order(self):
        settings = self.controller.get_verses_settings()
        if 'old_testament_order' in settings.keys():
            self.old_testament_order.lb.delete(0, tk.END)
            for translation in settings['old_testament_order']:
                self.old_testament_order.lb.insert(tk.END, translation)
        if 'new_testament_order' in settings.keys():
            self.new_testament_order.lb.delete(0, tk.END)
            for translation in settings['new_testament_order']:
                self.new_testament_order.lb.insert(tk.END, translation)
        if 'abbreviations' in settings.keys():
            self.abbreviations.set(settings['abbreviations'])
        settings = self.controller.get_projector_settings()
        if 'default_white_background' in settings:
            self.white_background.set(settings['default_white_background'])
        if 'auto_adjustment' in settings:
            self.verses_auto_adjustment.set(settings['auto_adjustment'])

    def set_translation_order(self, testament):
        if testament == 'old':
            if len(self.old_testament_order.lb.get(0, tk.END)) == 0:
                self.erase_translation_order('old')
            self.controller.set_verses_settings({'old_testament_order': self.old_testament_order.lb.get(0, tk.END)})
        elif testament == 'new':
            if len(self.new_testament_order.lb.get(0, tk.END)) == 0:
                self.erase_translation_order('new')
            self.controller.set_verses_settings({'new_testament_order': self.new_testament_order.lb.get(0, tk.END)})

    def erase_translation_order(self, testament):
        translations = self.controller.get_all_translation()
        for translation in translations:
            if testament == 'old':
                self.old_testament_order.lb.insert(tk.END, translation)
            elif testament == 'new':
                self.new_testament_order.lb.insert(tk.END, translation)

    def add_verses_configurations(self):
        tk.Label(self.verses_configurations, text="מקרן במצב הסתר").pack(anchor=tk.E)

        tk.Checkbutton(self.verses_configurations, text="רקע לבן", variable=self.white_background, anchor=tk.E,
                       command=lambda: self.controller.set_projector_settings({'default_white_background':
                                                                    self.white_background.get()})).pack(anchor=tk.E)
        tk.Label(self.verses_configurations, text="הגדרות פסוקים").pack(anchor=tk.E)
        # auto adjustment
        tk.Checkbutton(self.verses_configurations, text="גודל גופן אוטומטי", variable=self.verses_auto_adjustment,
                       command=lambda: self.controller.set_projector_settings({'auto_adjustment':
                                                                self.verses_auto_adjustment.get()})).pack(anchor=tk.E)
        # show abbreviations instead of full name
        tk.Checkbutton(self.verses_configurations, text="שם ספר מקוצר", variable=self.abbreviations,
                                                command=lambda: self.controller.set_verses_settings({'abbreviations':
                                                                     self.abbreviations.get()})).pack(anchor=tk.E)
