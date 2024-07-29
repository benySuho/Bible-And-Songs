import tkinter as tk
from tkinter import ttk

class EntryListBox(tk.Frame):
    def __init__(self, master, command=None, members=None, search_method=None, font=None, notify_one=False, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        if members is None:
            self.members = []
        else:
            self.members = members
        self.master = master
        self.command = command
        self.notify_one = notify_one
        if search_method == 'prefix':
            self.find = self.find_prefix
        else:
            self.find = self.find_containing
        self.input = tk.StringVar()
        self.font = font

        # creating text box
        self.e = tk.Entry(self.master, textvariable=self.input, font=self.font)
        self.e.pack(fill=tk.BOTH)
        self.e.bind('<KeyRelease>', self.checkkey)
        self.e.bind('<Up>', self.lb_up)
        self.e.bind('<Down>', self.lb_down)
        self.e.bind('<Return>', self.select_item)
        # creating list box
        self.lb = tk.Listbox(self.master, font=self.font)
        self.lb.pack(fill=tk.BOTH, expand=True)
        self.update_box(self.members)
        self.lb.bind('<Double-Button-1>', self.select_item)
        self.lb.bind('<Return>', self.select_item)
        self.get = self.lb.get

    def update_box(self, data):
        active = self.lb.get(tk.ACTIVE)
        self.lb.delete(0, 'end')  # clear previous data
        # put new data
        for item in data:
            self.lb.insert('end', item)
        if active in data:
            self.lb.activate(data.index(active))
            self.lb.selection_set(data.index(active))
        else:
            self.lb.selection_set(0)

    def checkkey(self, event):
        if event.keysym in ('Up', 'Down'):
            return
        value = event.widget.get()
        if len(value) == 0:
            data = self.members
        else:
            data = self.find(value)
        # update data in listbox
        self.update_box(data)
        if len(data) == 1 and self.notify_one:
            self.notify_controller()

    def lb_up(self, event):
        options = self.lb.get(0, tk.END)
        if not len(options):
            return
        current = options.index((self.lb.get(tk.ACTIVE)))
        if current:
            self.lb.activate(current - 1)
            self.lb.selection_clear(current)
            self.lb.selection_set(current - 1)
            self.e.icursor(tk.END)

    def lb_down(self, event):
        options = self.lb.get(0, tk.END)
        if not len(options):
            return
        current = options.index((self.lb.get(tk.ACTIVE)))
        if current < len(options) - 1:
            self.lb.activate(current + 1)
            self.lb.selection_clear(current)
            self.lb.selection_set(current + 1)
            self.e.icursor(tk.END)

    def select_item(self, event):
        self.e.icursor(tk.END)
        self.notify_controller()

    def find_prefix(self, value):
        data = []
        for item in self.members:
            if item.lower().startswith(value.lower()):
                data.append(item)
        if len(data) == 0 and len(value) > 0:
            data = self.find_prefix(value[:-1])
        return data

    def find_containing(self, value):
        data = []
        for item in self.members:
            if value.lower() in item.lower():
                data.append(item)
        if len(data) == 0 and len(value) > 1:
            data = self.find_containing(value[:-1])
        return data

    def notify_controller(self):
        if self.command is not None:
            self.command({'input': self.input.get(), 'selected': self.lb.get(tk.ACTIVE)})

    def delete_item(self, item):
        self.members.remove(item)
        self.update_box(self.members)

    def configure(self, *args, **kwargs):
        self.lb.configure(*args, **kwargs)
        self.e.configure(*args, **kwargs)
