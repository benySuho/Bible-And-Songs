import tkinter as tk
import unicodedata
from verses.bible_parse import Bible
from widgets.dd_list import DragDropListbox as DDLB
from verses.gematria import hebrew_gematria_value
import ttkbootstrap as tb
import re
from widgets import entry_list_box as elb


class VersesTab(tk.Frame):
    """
    Initialize a new instance of the VersesTab class.

    Parameters:
    master (tk.Widget): The parent widget for this instance.
    controller (VersesController): The controller for this instance.
    """

    def __init__(self, master, controller):
        super().__init__(master)
        self.pack(fill='both', expand=True)
        self.controller = controller
        self.bible = Bible()
        self.old_testament_order = list(self.bible.languages.keys())
        self.new_testament_order = list(self.bible.languages.keys())
        self.abbr = True
        # Variables
        self.book = 1
        self.chapter = 1
        self.verse = 1

        #  Right panel
        self.right_panel = tk.Frame(master=self, width=600, height=1000)
        self.right_panel.pack(fill=tk.BOTH, side=tk.RIGHT, expand=True)
        self.right_panel.grid_columnconfigure(0, weight=1)
        self.right_panel.grid_rowconfigure(0, weight=2)
        self.right_panel.grid_rowconfigure(1, weight=1)
        self.bind_controls(self.right_panel)

        self.middleFrame = tk.Frame(master=self.right_panel, height=200)
        self.middleFrame.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
        self.middleFrame.grid_columnconfigure(0, weight=8)
        self.middleFrame.grid_columnconfigure(1, weight=1)
        self.middleFrame.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
        self.middleFrame.grid_propagate(False)
        self.verses_near = []
        for i in range(7):
            self.verses_near.append([])
            self.verses_near[i] = tk.Label(self.middleFrame,
                                           text=self.get_verse(self.book, self.chapter, self.verse - 4 + i),
                                           wraplength=500, anchor=tk.E, justify=tk.RIGHT)
            self.verses_near[i].grid(row=i, column=0, sticky=tk.E)
            self.bind_controls(self.verses_near[i])
            if i == 3:
                self.verses_near[i].configure(font=tk.font.Font(weight="bold"), anchor=tk.E, justify=tk.RIGHT)
                self.middleFrame.grid_rowconfigure(i, weight=2)

        self.source = tk.StringVar()
        self.source_label = tk.Label(self.middleFrame, textvariable=self.source)
        self.source_label.grid(row=3, column=1)
        self.bind_controls(self.source_label)
        self.current_verse()
        self.bind_controls(self.middleFrame)

        self.bottomFrame = tk.Frame(master=self.right_panel)
        self.bottomFrame.pack(fill=tk.X, side=tk.BOTTOM)
        self.bottomFrame.grid_columnconfigure(0, weight=6)
        self.bottomFrame.grid_columnconfigure(1, weight=1)
        self.bottomFrame.grid_columnconfigure((2, 3), weight=2)
        self.bottomFrame.grid_rowconfigure((0, 1, 2), weight=1)
        self.bottomFrame.grid_rowconfigure(3, weight=3)
        self.bind_controls(self.bottomFrame)
        but = tb.Button(self.bottomFrame, text="הבא", command=self.next_verse)
        but.grid(row=1, column=3, sticky=tk.NSEW, padx=2, pady=2)
        but = tb.Button(self.bottomFrame, text="קודם", command=self.prev_verse)
        but.grid(row=1, column=2, sticky=tk.NSEW, padx=2, pady=2)
        but = tb.Button(self.bottomFrame, text="פרק הבא", command=self.next_chapter)
        but.grid(row=2, column=3, sticky=tk.NSEW, padx=2, pady=2)
        but = tb.Button(self.bottomFrame, text="פרק קודם", command=self.prev_chapter)
        but.grid(row=2, column=2, sticky=tk.NSEW, padx=2, pady=2)
        but = tb.Button(self.bottomFrame, text="הסתר תצוגה", command=self.hide_second_screen)
        but.grid(row=0, column=2, sticky=tk.NSEW, padx=2, pady=2)
        but = tb.Button(self.bottomFrame, text="הצג פסוק", command=self.show_verse, bootstyle='success')
        but.grid(row=0, column=3, sticky=tk.NSEW, padx=2, pady=2)

        for widget in self.bottomFrame.winfo_children():
            self.bind_controls(widget)

        self.queue = DDLB(self.bottomFrame, command_set=self.set_from_queue, command_get=self.get_source)
        self.queue.grid(row=0, rowspan=4, column=0, sticky=tk.NSEW)
        self.verses_frame = elb.EntryListBox(master=self, search_method='prefix',
                                             members=self.bible.book_names['heb'][0],
                                             command=self.item_selected, font=['Helvetica', 12], notify_one=True)

    def show_verse(self):
        """
        Displays the current verse in all available translations.
        """
        if self.book < 40:
            order = self.old_testament_order
        else:
            order = self.new_testament_order
        verse = self.bible.verse_in_languages(self.book, self.chapter, self.verse)
        text = ""
        for translation in order:
            try:
                if verse[translation]['language'] == 'heb':
                    text = (text +
                            f"{verse[translation]['abbr']}({self.chapter}:{self.verse}) ")
                    nor = unicodedata.normalize('NFKD', verse[translation]['verse'])
                    flattened = ''.join([c for c in nor if not unicodedata.combining(c)])
                    # print(flattened)
                    text = (text + flattened + '\n\n')

                else:
                    text = (text +
                            f"{verse[translation]['abbr' if self.abbr else 'book']}({self.chapter}:{self.verse}) {verse[translation]['verse']}" +
                            '\n\n')
            except:
                pass
        self.controller.show_verse(text)

    def select_source(self, source):
        """
        Selects a source (book, chapter, verse) and updates the current verse.
    
        Parameters:
        source (dict): A dictionary containing the source details. It should have keys 'book', 'chapter', and 'verse'.
        """
        chapter = self.get_number(source['chapter'])
        verse = self.get_number(source['verse'])
        self.book = 1 + self.bible.book_names['heb'][0].index(source['book'])

        # Try to select the exact verse
        if self.get_verse(self.book, chapter, verse):
            self.chapter = chapter
            self.verse = verse
        # If the exact verse is not available, try to select the first verse of the chapter
        elif self.get_verse(self.book, chapter, 1):
            self.chapter = chapter
            self.verse = 1
        # If the chapter is not available, try to select the first verse of the book
        elif self.get_verse(self.book, 1, 1):
            self.chapter = 1
            self.verse = 1

        # Update the current verse display
        self.current_verse()

    def hide_second_screen(self):
        self.controller.hide()

    def next_verse(self):
        """
        Advances the current verse by one and updates the display.
        """
        if not self.bible.get_verse_hebrew(self.book, self.chapter, self.verse + 1):
            return
        self.verse = self.verse + 1
        self.current_verse()
        if self.controller.verses_active():
            self.show_verse()

    def prev_verse(self):
        """
        This function is responsible for moving to the previous verse in the Bible.
        """
        if not self.bible.get_verse_hebrew(self.book, self.chapter, self.verse - 1):
            return
        self.verse = self.verse - 1
        self.current_verse()
        if self.controller.verses_active():
            self.show_verse()

    def current_verse(self):
        """
        Updates the current verse display in the GUI.
        """
        if not self.bible.get_verse_hebrew(self.book, self.chapter, self.verse):
            return
        self.source.set("(" + str(self.chapter) + ":" + str(self.verse) + ") " +
                        self.bible.book_names['heb'][0][self.book - 1])
        self.verses_around()

    def next_chapter(self):
        """
        This function is responsible for moving to the next chapter in the Bible.
        """
        if self.get_verse(self.book, self.chapter + 1, 1):
            self.chapter = self.chapter + 1
            self.verse = 1
            self.current_verse()
            if self.controller.verses_active():
                self.show_verse()

    def prev_chapter(self):
        """
        This function is responsible for moving to the previous chapter in the Bible.
        """
        if self.chapter < 2:
            return
        self.chapter = self.chapter - 1
        self.verse = self.bible.number_of_verses(self.book, self.chapter)
        self.current_verse()
        if self.controller.verses_active():
            self.show_verse()

    def get_verse(self, book, chapter, verse):
        """
        Retrieves a verse from the Bible based on the given book, chapter, and verse number.
    
        Parameters:
        book (int): The book number in the Bible.
        chapter (int): The chapter number in the Bible.
        verse (int): The verse number in the Bible.
    
        Returns:
        str: The verse text if found, otherwise None.
        """
        if book < 40:
            text = self.bible.get_verse_hebrew(book, chapter, verse, self.old_testament_order)
        else:
            text = self.bible.get_verse_hebrew(book, chapter, verse, self.new_testament_order)
        if text:
            return text

    def verses_around(self):
        """
        This function retrieves and displays verses around the current verse in the GUI.
        """
        for i in range(7):
            text = self.get_verse(self.book, self.chapter, self.verse - 3 + i)
            if not text:
                if (self.verse - 3 + i) < 1 < self.chapter:
                    vs = self.bible.number_of_verses(self.book, self.chapter - 1) + self.verse - 3 + i
                    text = self.get_verse(self.book, self.chapter - 1, vs)
                elif (self.verse - 3 + i) > 1:
                    text = self.get_verse(self.book, self.chapter + 1,
                                          (self.verse - 3 + i) - self.bible.number_of_verses(self.book, self.chapter))
                if not text:
                    text = " "
            self.verses_near[i].configure(text=text)
            if i == 3:
                self.verses_near[i].configure(font=tk.font.Font(weight="bold"))

    def mouse_wheel(self, event):
        # respond to Linux or Windows wheel event
        if event.num == 5 or event.delta == -120:
            self.next_verse()
        if event.num == 4 or event.delta == 120:
            self.prev_verse()

    def get_bible_descriptions(self):
        return self.bible.get_bible_descriptions()

    def get_number(self, string):
        """
        Converts a string to a number. If the string represents a number, it is converted to an integer.
        If the string represents a Hebrew Gematria value, it is converted to an integer.
    
        Parameters:
        string (str): The input string to be converted to a number.
    
        Returns:
        int: The converted number. If the input string cannot be converted to a number, the function returns None.
        """
        try:
            return int(string)
        except:
            return hebrew_gematria_value(string)

    def set_from_queue(self, source):
        """
        Sets the current book, chapter, and verse based on the source from the queue.
    
        Parameters:
        source (str): The source string from the queue, which contains the book, chapter, and verse information.
        """
        if not source:
            return
        source = source.split(') ')
        self.book = self.bible.book_names['heb'][0].index(source[1]) + 1
        source[0] = source[0][1:].split(':')
        self.chapter = int(source[0][0])
        self.verse = int(source[0][1])
        self.current_verse()
        if self.controller.verses_active():
            self.show_verse()

    def get_source(self):
        return f"({self.chapter}:{self.verse}) {self.bible.book_names['heb'][0][self.book - 1]}"

    def get_settings(self):
        """
        Retrieves the current settings of the VersesTab instance.

        Returns:
        dict: A dictionary containing the current settings. The dictionary includes the following keys:
            - 'book': The current book number in the Bible.
            - 'chapter': The current chapter number in the Bible.
            - 'verse': The current verse number in the Bible.
            - 'queue': A list of sources from the queue.
            - 'old_testament_order': A list of translations for the Old Testament.
            - 'new_testament_order': A list of translations for the New Testament.
            - 'abbreviations': A boolean indicating whether abbreviations should be used for the translations.
        """
        settings = {'book': self.book, 'chapter': self.chapter, 'verse': self.verse, 'queue': self.queue.get(0, tk.END),
                    'old_testament_order': self.old_testament_order, 'new_testament_order': self.new_testament_order,
                    'abbreviations': self.abbr}
        return settings

    def set_settings(self, settings):
        """
        Sets the current settings of the VersesTab instance.
    
        Parameters:
        settings (dict): A dictionary containing the settings to be applied. The dictionary should include the following keys:
            - 'old_testament_order' (optional): A list of translations for the Old Testament.
            - 'new_testament_order' (optional): A list of translations for the New Testament.
            - 'book' (optional): The current book number in the Bible.
            - 'chapter' (optional): The current chapter number in the Bible.
            - 'verse' (optional): The current verse number in the Bible.
            - 'abbreviations' (optional): A boolean indicating whether abbreviations should be used for the translations.
            - 'queue' (optional): A list of sources from the queue.
        """
        if 'old_testament_order' in settings.keys():
            self.old_testament_order = settings['old_testament_order']
        if 'new_testament_order' in settings.keys():
            self.new_testament_order = settings['new_testament_order']
        if 'book' in settings.keys():
            self.book = settings['book']
        if 'chapter' in settings.keys():
            self.chapter = settings['chapter']
        if 'verse' in settings.keys():
            self.verse = settings['verse']
        if 'abbreviations' in settings.keys():
            self.abbr = settings['abbreviations']
        if 'queue' in settings.keys():
            for item in settings['queue']:
                self.queue.add_item(item=item)

    def item_selected(self, item):
        """
        This function is called when an item is selected in the GUI. It extracts the book, chapter, and verse from the selected item and calls the `select_source` function to navigate to the selected verse.

        Parameters:
        item (dict): A dictionary containing the selected item. It should have a key 'input' containing the selected item's text.

        Returns:
        None
        """
        res = re.findall(r'\w+', item['input'])
        if len(res) > 2:
            self.select_source({'book': item['selected'], 'chapter': res[-2], 'verse': res[-1]})
        elif len(res) == 2:
            self.select_source({'book': item['selected'], 'chapter': res[-1], 'verse': 1})
        else:
            self.select_source(
                {'book': item['selected'], 'chapter': self.chapter, 'verse': self.verse})

    def bind_controls(self, widget):
        widget.bind('<Up>', lambda event: self.prev_verse())
        widget.bind('<Down>', lambda event: self.next_verse())
        widget.bind('<Left>', lambda event: self.prev_chapter())
        widget.bind('<Right>', lambda event: self.next_chapter())
        widget.bind('<MouseWheel>', self.mouse_wheel)
        widget.bind('<Button-1>', lambda event: self.middleFrame.focus_set())

    def get_all_translation(self):
        return list(self.bible.languages.keys())
