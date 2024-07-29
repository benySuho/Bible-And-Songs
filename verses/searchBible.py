import os
import xml.etree.ElementTree as ET

languages = {}
for file in os.listdir('Bible'):
    translation = ET.parse(f"Bible\\{file}").getroot()
    languages[translation[0].find('title').text] = translation

def findVerse(lang, b, c, v):
    """
    This function searches for a specific verse in a given Bible translation.

    Parameters:
    lang (xml.etree.ElementTree.Element): The root element of the Bible translation XML file.
    b (int): The book number (1-66) according to the Bible translation.
    c (int): The chapter number within the specified book.
    v (int): The verse number within the specified chapter.

    Returns:
    str: The text of the verse if found, otherwise None.
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


def verseInLanguages(b, c, v):
    """
    This function retrieves verses from multiple Bible translations for a given book, chapter, and verse.

    Parameters:
    b (int): The book number (1-66) according to the Bible translation.
    c (int): The chapter number within the specified book.
    v (int): The verse number within the specified chapter.

    Returns:
    list: A list of verse texts from all translations. 
    """
    text = []
    if findVerse(languages[0], b, c, v):
        text.append(findVerse(languages[0], b, c, v))
    else: # for case the translation doesn't have new testament
        text.append(findVerse(languages[1], b, c, v))
    for language in languages:
        text.append(findVerse(languages[language], b, c, v))
    return text


def number_of_verses(b, c):
    """
    This function calculates the number of verses in a specific chapter of a given book in the Modern Hebrew Bible.

    Parameters:
    b (int): The book number (1-66) according to the Modern Hebrew Bible.
    c (int): The chapter number within the specified book.

    Returns:
    int: The number of verses in the specified chapter.
    """
    for book in languages['Modern Hebrew Bible'].findall('BIBLEBOOK'):
        if int(book.get('bnumber')) != b:
            continue
        for chapter in book.findall('CHAPTER'):
            if int(chapter.get('cnumber')) != c:
                continue
            return len(chapter.findall('VERS'))


def get_verse_hebrew(b, c, v):
    return findVerse(languages['Modern Hebrew Bible'], b, c, v)


def get_bible_descriptions():
    """
    This function retrieves the descriptions of all Bible translations available.

    Returns:
    list: A list of strings, each representing the description of a Bible translation.
          The descriptions are extracted from the 'title' tags of the root elements of the XML files.
    """
    desc = []
    for lang in languages:
        desc.append(languages[lang][0].find('title').text)
    return desc
