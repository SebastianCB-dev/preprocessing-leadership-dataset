import re

def delete_accented_chars(text):
    """
    Removes accented characters from the given text and converts it to lowercase.

    Args:
        text (str): The input text.

    Returns:
        str: The text with accented characters removed and converted to lowercase.
    """
    text = text.lower()
    text = text.replace('á', 'a')
    text = text.replace('é', 'e')
    text = text.replace('í', 'i')
    text = text.replace('ó', 'o')
    text = text.replace('ú', 'u')
    return text

def delete_spanish_letters(text):
    """
    Deletes Spanish letters from the given text.

    Args:
        text (str): The input text.

    Returns:
        str: The text with Spanish letters removed.
    """
    text = text.lower()
    text.replace('ñ', 'n')
    return text

def delete_spaces(text):
    """
    Deletes spaces from the given text.

    Args:
        text (str): The input text.

    Returns:
        str: The text with spaces removed.
    """
    text_split = text.split(' ')
    # filter removes empty strings
    text_split = list(filter(None, text_split))
    text_split = list(filter(lambda x: x != ' ', text_split))

    return ' '.join(text_split)

def delete_not_vocabulary_words(text: str) -> str:
    """
    Deletes non-vocabulary words from the given text.

    Args:
        text (str): The input text.

    Returns:
        str: The text with non-vocabulary words removed.
    """
    text = text.lower()
    regex = re.compile(r'[^a-z\s]')
    text = re.sub(regex, '', text)
    return text