hebrew_gematria = {
    'א': 1, 'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5, 'ו': 6, 'ז': 7, 'ח': 8, 'ט': 9,
    'י': 10, 'כ': 20, 'ל': 30, 'מ': 40, 'נ': 50, 'ס': 60, 'ע': 70, 'פ': 80,
    'צ': 90, 'ק': 100, 'ר': 200, 'ש': 300, 'ת': 400
}

def hebrew_gematria_value(word):
    """
    Calculate the Hebrew Gematria value of a given word.

    Hebrew Gematria is a system of assigning numerical values to Hebrew letters,
    where each letter corresponds to a specific number. This function calculates the
    total value of a given word by summing up the values of its individual letters.

    Parameters:
    word (str): The Hebrew word for which to calculate the Gematria value.

    Returns:
    int: The calculated Gematria value of the given word.
    """
    value = 0
    for letter in word:
        value += hebrew_gematria.get(letter, 0)
    return value
