import re
import emoji
import stanza
import spacy

stanza.download('es', package='ancora', processors='tokenize,mwt,pos,lemma', verbose=True)
stNLP = stanza.Pipeline(lang='es', processors='tokenize,mwt,pos,lemma', use_gpu=True)
sp = spacy.load('es_core_news_md')
stop_words = sp.Defaults.stop_words

def delete_accented_chars(text: str) -> str:
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

def delete_spanish_letters(text: str) -> str:
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

def delete_spaces(text: str) -> str:
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

def delete_emojis(text: str) -> str:
    """
    Removes emojis from the given text.

    Args:
        text (str): The input text.

    Returns:
        str: The text with emojis removed.
    """
    text = emoji.replace_emoji(text, '')
    return text

def lemma(words: list[str]) -> list[str]:
    """
    Apply lemmatization to a list of words.

    Args:
        words (list[str]): The list of words to be lemmatized.

    Returns:
        list[str]: The lemmatized words.
    """
    new_words = []
    for word in words:
        result = stNLP(word)
        new_words.append(
            [word.lemma for sent in result.sentences for word in sent.words][0]
        )
    return new_words

def delete_stop_words(words: list[str]) -> list[str]:
    """
    Removes stop words from a list of words.

    Args:
        words (list[str]): The list of words to remove stop words from.

    Returns:
        list[str]: The list of words without stop words.
    """
    tokens_without_stopwords = [word for word in words if not word in stop_words]
    return tokens_without_stopwords
   