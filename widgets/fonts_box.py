import tkinter as tk
from tkinter import font
from tkinter import ttk
from tkinter.colorchooser import askcolor


class FontBox(tk.LabelFrame):
    def __init__(self, master, command_get, command_set, text=None, *args, **kwargs):
        super().__init__(master, labelanchor='ne', text=text, *args, **kwargs)
        self.master = master
        self.command_set = command_set
        self.command_get = command_get
        self.fonts = [ele for ele in font.families() if not ele.startswith('@')] + ['Helvetica']
        self.fonts.sort()
        self.text = text
        self.font_combo = tk.ttk.Combobox(self, values=self.fonts, width=20)
        self.font_combo.set("Arial")  # default value
        self.font_combo.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        self.font_size = tk.StringVar()
        self.size_spinbox = tk.Spinbox(self, from_=8, to=72, width=5, textvariable=self.font_size)
        self.size_spinbox.grid(row=1, column=0, padx=5, pady=5, sticky=tk.NSEW)

        self.color_var = tk.StringVar(value="#000000")  # default color: black
        self.color_button = tk.Button(self, text="בחר צבע", command=self.choose_color)
        self.color_button.grid(row=1, column=1, padx=5, pady=5)

        self.bold_var = tk.BooleanVar()
        self.bold_check = tk.Checkbutton(self, text="Bold", variable=self.bold_var, command=self.apply_changes)
        self.bold_check.grid(row=2, column=0, padx=5, pady=5)

        self.italic_var = tk.BooleanVar()
        self.italic_check = tk.Checkbutton(self, text="Italic", variable=self.italic_var, command=self.apply_changes)
        self.italic_check.grid(row=2, column=1, padx=5, pady=5)

        self.apply_button = tk.Button(self, text="החל", command=self.apply_changes)
        self.apply_button.grid(row=3, column=0, columnspan=2, pady=5)
        self.bind("<Configure>", self.get_values)
        # self.get_values()

    def apply_changes(self):
        selected_font = self.font_combo.get()
        selected_size = self.size_spinbox.get()
        selected_color = self.color_var.get()
        weight = 'bold' if self.bold_var.get() else 'normal'
        slant = 'italic' if self.italic_var.get() else 'roman'
        if self.command_set:
            self.command_set([self.text, [[selected_font, selected_size, weight, slant], selected_color]])

    def choose_color(self):
        color_code = askcolor(title="בחר צבע")
        if color_code[1]:
            self.color_var.set(color_code[1])
            self.apply_changes()

    def get_values(self, event=None):
        if not self.command_get:
            return
        selected_font, selected_size, selected_color, weight, slant = self.command_get(self.text)
        self.font_combo.set(selected_font)
        self.font_size.set(selected_size)
        self.color_var.set(selected_color)
        self.bold_var.set(weight == 'bold' or slant == 'bold')
        self.italic_var.set(weight == 'italic' or slant == 'italic')
