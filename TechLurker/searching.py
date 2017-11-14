"""Module for finding word frequency."""

from nltk import word_tokenize, FreqDist
from collections import Counter
# from nltk.stem import RegexpStemmer


def count_words(text):
    """Will count all words from inputed text."""
    user_count = 0
    user_word = 'the'
    tokens = word_tokenize(text)
    count = Counter(FreqDist(tokens))
    if user_word in text:
        word_count = count.get(user_word)
        user_count += word_count
    else:
        user_count = 0
    return user_count


# def find_root_word(text):
#     """Will find root words."""
#     st = RegexpStemmer('ing$|s$|able$', min=5)
#     stems.append(st.stems(text))
