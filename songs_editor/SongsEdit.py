import ttkbootstrap as tb
import tkinter as tk
import pickle
from songs_editor.parsePPT import extract_text_from_ppt
import os
from ttkbootstrap.scrolled import ScrolledFrame
import subprocess
import threading


class SongsEdit(tb.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.pack(fill='both', expand=True)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=3)
        self.top_frame = tb.Frame(master=self, )
        self.top_frame.grid(row=0, column=0, sticky=tb.NSEW)
        # self.is_changed = False
        # self.progress = None

        for i in range(5):
            self.top_frame.grid_columnconfigure(i, weight=1)
            if i < 2:
                self.top_frame.grid_rowconfigure(i, weight=1)

        self.song_name = tb.StringVar()
        self.song_name_entry = tb.Entry(self.top_frame, textvariable=self.song_name, justify=tk.RIGHT)
        self.song_name_entry.grid(row=0, column=3, sticky=tb.NE)
        label = tb.Label(self.top_frame, text=':שם ', anchor=tb.E)
        label.grid(row=0, column=4, sticky=tb.N)
        self.songs_list_cb = tb.Combobox(self.top_frame, values=['שיר חדש'] + self.import_names())
        self.songs_list_cb.grid(row=0, column=2, sticky=tb.NE)
        self.songs_list_cb.current(0)
        self.songs_list_cb['state'] = 'readonly'
        self.songs_list_cb.bind('<<ComboboxSelected>>', self.song_chosen)
        but = tb.Button(self.top_frame, text='ייבוא ממצגת', command=self.import_presentations_pop_up)
        but.grid(row=0, column=0)
        but = tb.Button(self.top_frame, text='שמור', command=self.export_song, bootstyle='success')
        but.grid(row=1, column=4)
        but = tb.Button(self.top_frame, text='בטל', command=self.song_chosen)
        but.grid(row=1, column=3)
        but = tb.Button(self.top_frame, text='מחק שיר', command=self.remove_song, bootstyle='danger')
        but.grid(row=1, column=2)

        self.bottom_frame = tb.Frame(master=self)
        self.bottom_frame.grid(row=1, column=0, sticky=tb.NSEW)
        self.bottom_frame.grid_rowconfigure(1, weight=1)
        # Create 5 Text widgets with a width of 200 characters
        # Create a scrollbar
        scrollbar = tb.Scrollbar(self.bottom_frame)
        scrollbar.grid(row=1, column=5, sticky=tb.NSEW)

        # Create 5 Text widgets with a width of 200 characters
        self.song_texts = []
        language = ['English', 'English Translation', 'עברית', 'Русский', 'Русский перевод']
        for i in range(5):
            self.bottom_frame.grid_columnconfigure(i, weight=1)
            label = tb.Label(self.bottom_frame, text=language[i])
            label.grid(row=0, column=i, sticky=tb.N)
            text_widget = tk.Text(self.bottom_frame, wrap=tb.WORD, yscrollcommand=scrollbar.set, width=20, undo=True)
            text_widget.grid(row=1, column=i, sticky=tb.NSEW)
            self.song_texts.append(text_widget)
            but = tk.Button(self.bottom_frame, text='ערוך בכתבן', command=lambda index=i: self.open_notepad(index))
            but.grid(row=2, column=i, sticky=tb.S)
        self.song_texts[2].tag_configure("right", justify='right')
        scrollbar.config(command=self.on_scroll)

    def on_scroll(self, *args):
        for text_widget in self.song_texts:
            text_widget.yview(*args)

    def song_chosen(self, event=None,name=None):
        # self.is_changed = False
        if not name:
            name = self.songs_list_cb.get()
        else:
            self.songs_list_cb.set(name)
        self.song_name.set(name)
        song_text = self.import_song(name)
        for i in range(5):
            self.song_texts[i].delete(1.0, tb.END)
        if song_text:
            self.song_texts[2].insert(tb.END, song_text[0], "right")
            self.song_texts[0].insert(tb.END, song_text[1])
            self.song_texts[1].insert(tb.END, song_text[3])
            self.song_texts[3].insert(tb.END, song_text[2])
            self.song_texts[4].insert(tb.END, song_text[4])

    def remove_song(self, event=None):
        name = self.songs_list_cb.get()
        if name == 'שיר חדש':
            return
        os.remove(f"Songs\\{name}.txt")
        self.songs_list_cb['values'] = ['שיר חדש'] + self.import_names()
        self.songs_list_cb.current(0)
        self.controller.delete_song(name)

    def import_song(self, file):
        if file == 'שיר חדש':
            return None
        with open(f"Songs\\{file}.txt", 'rb') as f:
            imported_text = pickle.load(f)
            song_text = [[], [], [], [], []]
            for slide in imported_text:
                for i, lang in enumerate(slide):
                    song_text[i].append('\n'.join(lang))
            for i in range(5):
                song_text[i] = '\n\n'.join(song_text[i])
            return song_text

    def export_song(self, event=None):
        texts = [[], [], [], [], []]
        for i in range(5):
            lang = self.song_texts[i].get(1.0, tk.END).split("\n\n")
            slide_text = []
            for slide in lang:
                lines = slide.split("\n")
                slide_text.append([i for i in lines if i])
            texts[i] = slide_text
        item = zip(texts[2], texts[0], texts[3], texts[1], texts[4])
        saved_text = []
        for text in list(item):
            saved_text.append(list(text))
        old_name = self.songs_list_cb.get()
        new_name = self.song_name.get()
        if new_name != old_name and old_name != 'שיר חדש':
            os.remove(f"Songs\\{old_name}.txt")
        with open(f"Songs\\{new_name}.txt", 'wb') as f:
            pickle.dump(saved_text, f)
        self.songs_list_cb['values'] = ['שיר חדש'] + self.import_names()
        self.songs_list_cb.current(self.songs_list_cb['values'].index(new_name))
        self.controller.update_song(old_name, new_name)

    def import_presentations_pop_up(self, event=None):
        self.top = tk.Toplevel(self)
        self.top.geometry("250x500")
        self.top.title("ייבוא ממצגת")

        if os.listdir('Presentations'):
            new_songs = []
            existing_songs_to_import = []
            existing_songs = os.listdir('Songs')
            existing_songs = [item.removesuffix('.txt') for item in existing_songs]
            for file in os.listdir('Presentations'):
                name, extension = self.get_file_name_extension(file)
                if extension == '.pptx' or extension == '.ppt':
                    if name in existing_songs:
                        existing_songs_to_import.append(file)
                    else:
                        new_songs.append(file)

            self.name_vars = {}
            if new_songs:
                tk.Label(self.top, anchor='e', justify=tk.RIGHT, text='שירים חדשים', font='Helvetica 14').pack()
                new_frame = ScrolledFrame(master=self.top, autohide=True)
                new_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
                for name in new_songs:
                    self.name_vars[name] = tk.BooleanVar(value=True)

                # Create checkboxes for each name
                checkboxes_new = []
                for file, var in self.name_vars.items():
                    name, _ = self.get_file_name_extension(file)
                    checkbox = tk.Checkbutton(new_frame, text=name, variable=var)
                    checkbox.pack(anchor='center')
                    checkboxes_new.append(checkbox)
            if existing_songs_to_import:
                tk.Label(self.top, anchor='e', justify=tk.RIGHT, text='שירים קיימים', font='Helvetica 14').pack()
                old_frame = ScrolledFrame(master=self.top, autohide=True)
                old_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
                for name in existing_songs_to_import:
                    self.name_vars[name] = tk.BooleanVar()

                # Create checkboxes for each name
                checkboxes_old = []
                for file in existing_songs_to_import:
                    name, _ = self.get_file_name_extension(file)
                    checkbox = tk.Checkbutton(old_frame, text=name, variable=self.name_vars[file])
                    checkbox.pack(anchor='center')
                    checkboxes_old.append(checkbox)

            self.progress = tb.Progressbar(self.top, orient='horizontal', value=0, maximum=100,
                                           mode='determinate', length=250)
            self.progress.pack(side=tb.BOTTOM, fill=tb.BOTH)
            show_button = tk.Button(self.top, text="ייבוא", command=self.add_selected_names)
            show_button.pack(side=tk.BOTTOM)

        else:
            tk.Label(self.top, anchor=tk.E, justify=tk.RIGHT, text='לא נמצאו קבצים').pack()

    def add_selected_names(self):
        selected_names = [name for name, var in self.name_vars.items() if var.get()]
        if not selected_names:
            return
        self.progress['maximum'] = len(selected_names)
        self.progress['value'] = 0

        for file in selected_names:
            extracted_text = extract_text_from_ppt(f"Presentations\\{file}")
            name, _ = self.get_file_name_extension(file)
            with open(f"Songs\\{name}.txt", 'wb') as f:
                pickle.dump(extracted_text, f)
            self.progress.step(1)
            self.progress.update()
        self.songs_list_cb['values'] = ['שיר חדש'] + self.import_names()
        self.controller.update_song()
        self.top.destroy()

    def open_notepad(self, index):
        # Open Notepad with the temporary text file in a separate thread
        subprocess_thread = threading.Thread(target=self.open_notepad_thread, args=(index,))
        subprocess_thread.start()

    def open_notepad_thread(self, index):
        with open(f"Songs\\temp_{index}.txt", "w", encoding="utf-8") as file:
            text = self.song_texts[index].get(1.0, tk.END)
            file.write(text)

        # Open Notepad in the background
        process = subprocess.Popen(["notepad.exe", f"Songs\\temp_{index}.txt"],
                                   creationflags=subprocess.DETACHED_PROCESS)

        # Wait for the process to finish
        process.wait()

        with open(f"Songs\\temp_{index}.txt", "r", encoding="utf-8") as file:
            text = file.read()
            self.song_texts[index].delete(1.0, tb.END)
            if index == 2:
                self.song_texts[2].insert(tb.END, text, "right")
            else:
                self.song_texts[index].insert(tb.END, text)
        os.remove(f"Songs\\temp_{index}.txt")

    def get_file_name_extension(self, file_path):
        name, extension = os.path.splitext(file_path)
        return name, extension

    def import_names(self):
        return [file.removesuffix('.txt') for file in os.listdir('Songs')]
