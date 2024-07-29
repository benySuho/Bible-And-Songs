import tkinter as tk


class MiniSlide(tk.LabelFrame):
    def __init__(self, master, name, num, text, font=None, command_active=None, command_show=None):
        self.master = master
        self.name = name
        self.number = num
        self.text = text
        super().__init__(self.master, text=f"{self.name} {self.number+1}", labelanchor='s')
        self.command_show = command_show
        self.command_active = command_active

        self.label = tk.Label(self, text=self.text, font=font, wraplength=self.winfo_reqwidth()-10)
        self.label.pack(fill=tk.BOTH, expand=True)

        self.label.bind('<Button-1>', self.set_active)
        self.bind('<Button-1>', self.set_active)
        self.bind('<Double-Button-1>', self.set_active_show)
        self.label.bind('<Double-Button-1>', self.set_active_show)

    def set_active(self, event=None):
        if self.command_active:
            self.command_active(self, self.name, self.number)

    def set_active_show(self, event=None):
        if self.command_show:
            self.command_show(self, self.name, self.number)
