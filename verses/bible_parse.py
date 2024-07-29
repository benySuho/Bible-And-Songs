import os
import xml.etree.ElementTree as ET
from verses.bookNames import *


class Bible:
    def __init__(self):
        """
        Initialize Bible class with translations and book names.

        self.languages: Dictionary to store Bible translations.
        self.book_names: Dictionary to store book names in different languages.
        """
        self.languages = {}
        self.book_names = {'heb': [bible_books_hebrew, bible_books_hebrew_abbreviations],
                           'eng': [bible_books_english, bible_books_english_abbreviations],
                           'rus': [bible_books_russian, bible_books_russian_abbreviations],
                           'spa': [bible_books_spanish, bible_books_spanish_abbreviations]}
        for file in os.listdir('Bible'):
            translation = ET.parse(f"Bible\\{file}").getroot()
            self.languages[translation[0].find('title').text] = translation
        self.order = list(self.languages.keys())

    def find_verse(self, lang, b, c, v):
        """
        Find a specific verse in a given translation.

        Parameters:
        lang (ElementTree): The translation to search in.
        b (int): The book number.
        c (int): The chapter number.
        v (int): The verse number.

        Returns:
        str: The verse text if found, otherwise None.
        """
        for book in lang.findall('BIBLEBOOK'):
            if int(book.get('bnumber')) != b:
                continue
            for chapter in book.findall('CHAPTER'):
                if int(chapter.get('cnumber')) != c:
                    continue
                for vers in chapter.findall('VERS'):
                    if int(vers.get('vnumber')) == v:
                        return vers.text[:len(vers.text) - 1]

    def verse_in_languages(self, b, c, v):
        """
        Get a verse in all available translations.

        Parameters:
        b (int): The book number.
        c (int): The chapter number.
        v (int): The verse number.

        Returns:
        dict: A dictionary containing the verse text in each translation.
        """
        verse = {}
        for translation in self.order:
            vers = self.find_verse(self.languages[translation], b, c, v)
            if vers:
                if self.languages[translation][0].find('language').text.lower() in self.book_names.keys():
                    book = self.book_names[self.languages[translation][0].find('language').text.lower()][0][b - 1]
                    abbr = self.book_names[self.languages[translation][0].find('language').text.lower()][1][b - 1]
                else:
                    book = self.book_names['eng'][0][b - 1]
                    abbr = self.book_names['eng'][1][b - 1]
                verse[translation] = {
                    'language': self.languages[translation][0].find('language').text.lower(),
                    'book': book,
                    'abbr': abbr,
                    'verse': self.find_verse(self.languages[translation], b, c, v)}
        return verse

    def number_of_verses(self, b, c):
        """
        Get the number of verses in a specific chapter.

        Parameters:
        b (int): The book number.
        c (int): The chapter number.

        Returns:
        int: The number of verses in the chapter.
        """
        for book in self.languages['Modern Hebrew Bible'].findall('BIBLEBOOK'):
            if int(book.get('bnumber')) != b:
                continue
            for chapter in book.findall('CHAPTER'):
                if int(chapter.get('cnumber')) != c:
                    continue
                return len(chapter.findall('VERS'))

    def get_verse_hebrew(self, b, c, v, translations=None):
        """
        Get a verse in Hebrew translation.

        Parameters:
        b (int): The book number.
        c (int): The chapter number.
        v (int): The verse number.
        translations (list, optional): A list of translations to search in. Defaults to all available translations.

        Returns:
        str: The verse text in Hebrew if found, otherwise None.
        """
        if translations is None:
            translations = list(self.languages.keys())
        hebrew = []
        for translation in translations:
            if 'heb' in self.languages[translation][0].find('language').text.lower():
                hebrew.append(translation)
        for heb in hebrew:
            verse = self.find_verse(self.languages[heb], b, c, v)
            if verse:
                return verse

    def get_bible_descriptions(self):
        """
        Get a list of Bible translation descriptions.

        Returns:
        list: A list of Bible translation descriptions.
        """
        desc = []
        for lang in self.languages:
            desc.append(self.languages[lang][0].find('title').text)
        return desc
