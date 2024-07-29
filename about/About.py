# import tkinter as tk
import ttkbootstrap as tb
import webbrowser


class About(tb.Frame):
    def __init__(self, master, verses_tab):
        super().__init__(master)
        self.pack()
        self.verses_tab = verses_tab
        label1 = tb.Label(self, text="טקסט תנ\"ך וברית החדשה בשימוש ממקורות פתוחים", justify=tb.RIGHT, anchor=tb.E)
        label1.pack(fill=tb.X)
        #
        label2 = tb.Label(self, text="https://sourceforge.net/projects/zefania-sharp/", justify=tb.RIGHT, anchor=tb.E,
                          foreground='blue', font=tb.font.Font(underline=True))
        label2.pack(fill=tb.X)
        label2.bind("<Button-1>", lambda e: webbrowser.open_new_tab("https://sourceforge.net/projects/zefania-sharp/"))
        label3 = tb.Label(self, text=":תרגומים", justify=tb.RIGHT, anchor=tb.E)
        label3.pack(fill=tb.X)
        for translation in self.verses_tab.get_bible_descriptions():
            label = tb.Label(self, text=translation, justify=tb.RIGHT, anchor=tb.E)
            label.pack(fill=tb.X)
            # print(translation)
        label4 = tb.Label(self, text="תודה לאישתי היקרה מיכל סוחוצ'ב על התמיכה והאהבה", justify=tb.RIGHT, anchor=tb.E)
        label4.pack(fill=tb.X)
