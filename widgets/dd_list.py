import tkinter as tk


class DragDropListbox(tk.Frame):
    """ A tk listbox with drag'n'drop reordering of entries. """

    def __init__(self, master, command_get=None, command_set=None, command_update=None, *args, **kwargs):
        super().__init__(master)
        self.lb = tk.Listbox(self, *args, **kwargs)
        self.lb.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        # self.lb.configure(justify=tk.RIGHT)
        self.lb.bind('<Button-1>', self.getState, add='+')
        self.lb.bind('<Button-1>', self.setCurrent, add='+')
        self.lb.bind('<B1-Motion>', self.shiftSelection)
        self.lb.bind('<Delete>', self.delete_item)
        self.lb.bind('<BackSpace>', self.delete_item)
        self.lb.bind('<Double-Button-1>', self.set)
        self.lb.bind('<Return>', self.set)
        self.curIndex = None
        self.curState = None
        self.get = self.lb.get
        self.command_get = command_get
        self.command_set = command_set
        self.command_update = command_update

        self.control_buttons = tk.Frame(self)
        self.control_buttons.pack(side=tk.RIGHT, fill=tk.Y)
        self.but_plus = tk.Button(self.control_buttons, text='+', command=self.add_item)
        self.but_plus.pack(padx=2, pady=2, fill=tk.X)
        self.but_minus = tk.Button(self.control_buttons, text='-', command=self.delete_item)
        self.but_minus.pack(padx=2, pady=2, fill=tk.X)
        self.but_x = tk.Button(self.control_buttons, text='X', command=self.delete_all)
        self.but_x.pack(padx=2, pady=2, fill=tk.X)

    def setCurrent(self, event):
        ''' gets the current index of the clicked item in the listbox '''
        self.curIndex = self.lb.nearest(event.y)

    def getState(self, event):
        ''' checks if the clicked item in listbox is selected '''
        i = self.lb.nearest(event.y)
        self.curState = self.lb.selection_includes(i)

    def shiftSelection(self, event):
        ''' shifts item up or down in listbox '''
        i = self.lb.nearest(event.y)
        if self.curState == 1:
            self.lb.selection_set(self.curIndex)
        else:
            self.lb.selection_clear(self.curIndex)
        if i < self.curIndex:
            # Moves up
            x = self.lb.get(i)
            selected = self.lb.selection_includes(i)
            self.lb.delete(i)
            self.lb.insert(i + 1, x)
            if selected:
                self.lb.selection_set(i + 1)
            self.curIndex = i
        elif i > self.curIndex:
            # Moves down
            x = self.lb.get(i)
            selected = self.lb.selection_includes(i)
            self.lb.delete(i)
            self.lb.insert(i - 1, x)
            if selected:
                self.lb.selection_set(i - 1)
            self.curIndex = i
        if self.command_update:
            self.command_update()

    def delete_item(self, event=None, item=None):
        if item:
            index = self.lb.get(0, tk.END).index(item)
            self.lb.delete(index)
        else:
            self.lb.delete('active')
        if self.command_update:
            self.command_update()

    def delete_all(self, event=None):
        self.lb.delete(0, tk.END)
        if self.command_update:
            self.command_update()

    def add_item(self, item=None, index=tk.END):
        if not self.command_get:
            return
        if not item:
            item = self.command_get()
        if item in self.lb.get(0, tk.END):
            return
        self.lb.insert(index, item)

    def set(self, event=None):
        if not self.command_set:
            return
        self.command_set(self.lb.get('active'))

    def configure(self,  **kwargs):
        self.lb.configure(**kwargs)
        self.but_plus.configure(**kwargs)
        self.but_minus.configure(**kwargs)
        self.but_x.configure(**kwargs)
