import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb
from verses.VersesTab import VersesTab
from songs_control.SongsTab import SongsTab
from settings.Settings import Settings
from songs_editor.SongsEdit import SongsEdit
from pictures.PicturesTab import PicturesTab
from about.About import About
import pickle
import os
import control


class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.controller = control.Controller()
        self.check_create_folders()
        self.title("פסוקים ושירים")
        self.tab_control = tb.Notebook(self)
        s = ttk.Style(self.tab_control)
        s.theme_create("MyStyle", parent="alt", settings={
            "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0], "tabposition": 'ne'}},
            "TNotebook.Tab": {"configure": {"padding": [44, 10]}}})
        s.theme_use("MyStyle")
        self.controller.set_tabs(self.tab_control)
        self.verses_tab = VersesTab(self.tab_control, self.controller)
        self.controller.set_verses(self.verses_tab)
        self.songs_tab = SongsTab(self.tab_control, self.controller)
        self.controller.set_songs(self.songs_tab)
        self.pictures_tab = PicturesTab(self.tab_control, self.controller)
        self.songs_edit = SongsEdit(self.tab_control, self.controller)
        self.controller.set_songs_edit(self.songs_edit)
        self.settings_tab = Settings(self.tab_control, self.controller)
        self.controller.set_settings(self.settings_tab)
        self.about_tab = About(self.tab_control, self.verses_tab)

        self.tab_control.add(self.about_tab, text='אודות')
        self.tab_control.add(self.settings_tab, text='הגדרות')
        self.tab_control.add(self.songs_edit, text='עריכת שירים')
        self.tab_control.add(self.pictures_tab, text='תמונות')
        self.tab_control.add(self.songs_tab, text='שירים')
        self.tab_control.add(self.verses_tab, text='פסוקים')
        self.tab_control.select(self.verses_tab)
        self.tab_control.pack(expand=True, fill="both")
        # self.tab_control.bind("<<NotebookTabChanged>>", self.tab_selected)
        self.geometry("800x600")
        self.minsize(800, 400)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def start(self):
        self.controller.hide()
        self.import_settings()
        # self.settings_tab.load_values()
        self.mainloop()

    def on_closing(self):
        configs = {'projector': self.controller.get_projector_settings(),
                   'verses': self.controller.get_verses_settings(), 'songs': self.controller.get_songs_settings(),
                   'interface_font': self.controller.get_interface_font(),
                   'current_tab': self.tab_control.select().removeprefix('.!notebook.!')}
        with open('configurations', 'wb') as file:
            pickle.dump(configs, file)
        self.destroy()

    def import_settings(self):
        try:
            file = open('configurations', 'rb')
        except:
            return
        configs = pickle.load(file)
        file.close()
        if 'interface_font' in configs.keys():
            self.controller.apply_interface_font(configs['interface_font'])
        if 'projector' in configs.keys():
            self.controller.set_projector_settings(configs['projector'])
        if 'verses' in configs.keys():
            self.controller.set_verses_settings(configs['verses'])
            self.controller.update_translation_order()
        self.verses_tab.current_verse()
        if self.controller.verses_active():
            self.verses_tab.show_verse()

        if 'songs' in configs.keys():
            self.controller.set_songs_settings(configs['songs'])
        if self.controller.song_active():
            self.songs_tab.show_slide()

        if 'current_tab' in configs.keys():
            if configs['current_tab'] == 'versestab':
                self.tab_control.select(self.verses_tab)
            elif configs['current_tab'] == 'songstab':
                self.tab_control.select(self.songs_tab)
            elif configs['current_tab'] == 'songsedit':
                self.tab_control.select(self.songs_edit)
            elif configs['current_tab'] == 'settings':
                self.tab_control.select(self.settings_tab)
            elif configs['current_tab'] == 'picturestab':
                self.tab_control.select(self.pictures_tab)
            elif configs['current_tab'] == 'about':
                self.tab_control.select(self.about_tab)

    def check_create_folders(self):
        folders = ['Songs', 'Images', 'Bible', 'Presentations']
        for folder in folders:
            if not os.path.exists(folder):
                os.makedirs(folder)
