import os
import pickle
import tkinter as tk
from tkinter import ttk
from widgets.dd_list import DragDropListbox as DDLB

from songs_control.SlidesMiniShow import SlidesMiniShow
import ttkbootstrap as tb
from widgets import entry_list_box as elb


class SongsTab(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.pack(fill='both', expand=True)
        self.controller = controller
        self.songNames = []  # List to store song names in Songs folder
        self.songs = {}  # Loaded songs
        self.import_names()
        self.active_slide = None
        self.active_song = None
        self.interface_font = None

        # Right panel
        self.rightFrame = tk.Frame(master=self)
        self.rightFrame.pack(fill=tk.BOTH, side=tk.RIGHT, expand=True)
        self.top_frame = tk.Frame(master=self.rightFrame)
        self.top_frame.pack(fill=tk.BOTH, expand=True)
        self.top_frame.rowconfigure(0, weight=1)
        self.top_frame.columnconfigure(0, weight=1)
        self.slides = SlidesMiniShow(master=self.top_frame, songs=self.songs,
                                     command_active=self.set_active_song, command_show=self.show_slide)
        self.slides.grid(row=0, column=0, sticky=tk.NSEW)
        self.slides.enable_scrolling()

        self.bottomFrame = tk.Frame(master=self.rightFrame)
        self.bottomFrame.pack(fill=tk.X, side=tk.BOTTOM)
        self.bottomFrame.grid_columnconfigure(0, weight=2)
        self.bottomFrame.grid_columnconfigure(1, weight=1)
        self.bottomFrame.grid_columnconfigure(2, weight=1)
        self.bottomFrame.grid_columnconfigure(3, weight=3)

        but = tb.Button(self.bottomFrame, text="הבא", command=self.next)
        but.grid(row=0, column=2, sticky=tk.NSEW, padx=2, pady=2)
        but = tb.Button(self.bottomFrame, text="קודם", command=self.previous)
        but.grid(row=0, column=1, sticky=tk.NSEW, padx=2, pady=2)
        but2 = tb.Button(self.bottomFrame, text="הסתר תצוגה", command=self.hide_second_screen)
        but2.grid(row=1, column=1, sticky=tk.NSEW, padx=2, pady=2)
        but = tb.Button(self.bottomFrame, text="הצג", command=self.show_slide, bootstyle='success')
        but.grid(row=1, column=2, sticky=tk.NSEW, padx=2, pady=2)
        but2 = tb.Button(self.bottomFrame, text="ערוך",
                         command=lambda e=None: self.controller.edit_songs(self.active_song))
        but2.grid(row=2, column=1, sticky=tk.NSEW, padx=2, pady=2)

        #  Left panel
        self.songs_list = elb.EntryListBox(self, members=self.songNames, font=['Helvetica', 12], command=self.add_song)
        self.queue = DDLB(self.bottomFrame, font=['Helvetica', 12], command_get=lambda: self.songs_list.get(tk.ACTIVE),
                          command_update=self.rearrange_frames, command_set=self.set_active_song)
        self.queue.grid(row=0, column=0, rowspan=4, sticky=tk.NSEW)

    def add_song(self, song=None):
        if not song:
            return
        if song['selected'] in self.songs.keys():
            return
        self.queue.add_item(song['selected'])
        self.import_song(song['selected'])
        self.rearrange_frames()

    def hide_second_screen(self):
        self.controller.hide()

    def show_slide(self):
        if not self.active_song in self.songs.keys():
            return
        if not self.active_slide:
            self.active_slide = 0
        text = self.songs[self.active_song]
        self.controller.show_slide(text[self.active_slide])

    def import_names(self):
        self.songNames = []
        for file in os.listdir('Songs'):
            self.songNames.append(file.split('.')[0])

    def import_song(self, file):
        with open(f"Songs\\{file}.txt", 'rb') as f:
            self.songs[file] = pickle.load(f)

    def rearrange_frames(self):
        song_names = self.queue.get(0, tk.END)
        songs = {}
        for song_name in song_names:
            if song_name in self.songs.keys():
                songs[song_name] = self.songs[song_name]
            else:
                self.import_song(song_name)
                songs[song_name] = self.songs[song_name]
        self.songs = songs
        if not self.active_song in song_names:
            self.active_song = self.queue.get(tk.ACTIVE)
            self.active_slide = 0
        self.slides.update_songs(songs, {'name': self.active_song, 'number': self.active_slide, 'slide': None})

    def next(self):
        if not self.active_song:
            return
        if self.active_slide < len(self.songs[self.active_song]) - 1:
            self.active_slide += 1
        else:
            songs_in_queue = self.queue.get(0, tk.END)
            index = songs_in_queue.index(self.active_song)
            if index >= len(songs_in_queue) - 1:
                return
            self.active_song = self.queue.get(index + 1)
            self.active_slide = 0
        self.slides.update_songs(
            self.songs, {'name': self.active_song, 'number': self.active_slide, 'slide': None})
        if self.controller.song_active():
            self.show_slide()

    def previous(self):
        if not self.active_song:
            return
        if self.active_slide > 0:
            self.active_slide -= 1
        else:
            songs_in_queue = self.queue.get(0, tk.END)
            index = songs_in_queue.index(self.active_song)
            if index <= 0:
                return
            self.active_song = self.queue.get(index - 1)
            self.active_slide = len(self.songs[self.active_song]) - 1
        self.slides.update_songs(
            self.songs, {'name': self.active_song, 'number': self.active_slide, 'slide': None})
        if self.controller.song_active():
            self.show_slide()

    def get_settings(self):
        settings = {'songs': self.queue.get(0, tk.END), 'active_song': self.active_song,
                    'active_slide': self.active_slide}
        return settings

    def set_settings(self, settings):
        songs = self.songs_list.get(0, tk.END)
        if 'songs' in settings:
            for song in settings['songs']:
                if song in songs:
                    self.queue.add_item(song)
                    self.import_song(song)
            if 'active_song' in settings:
                if settings['active_song'] in songs:
                    self.active_song = settings['active_song']
                    if 'active_slide' in settings:
                        self.active_slide = settings['active_slide']
                    else:
                        self.active_slide = 0
                else:
                    self.active_song = self.queue.get(tk.ACTIVE)
                    self.active_slide = 0
        self.rearrange_frames()

    def set_active_song(self, song=None, number=None):
        self.active_song = song
        if not song:
            self.active_song = self.queue.get(tk.ACTIVE)
        if not number:
            self.active_slide = 0
        else:
            self.active_slide = number

    def update_songs(self):
        self.import_names()
        self.songs_list.update_box(self.songNames)

    def update_song(self, old_song, new_song):
        if old_song in self.songs.keys():
            if old_song != new_song:
                self.songs.pop(old_song)
                self.queue.add_item(new_song, self.queue.get(0, tk.END).index(old_song))
                self.queue.delete_item(old_song)
            self.import_song(new_song)
            self.slides.set_songs(self.songs)
        self.update_songs()

    def delete_song(self, song):
        self.songs.pop(song)
        self.songs_list.delete_item(song)
        self.queue.delete_item(song)

    def apply_interface_font(self, font=None):
        if font:
            self.slides.font = font
