"""
Data Preprocessing

by StasyanG
"""

import os
import re

def clean_lyrics(text):
    """
    Cleans lyrics text

    Parameters
    ----------
    text (string):
        Lyrics text

    Returns
    ----------
    clean_text (string):
        Cleaned text
    """

    # to lower
    clean_text = text.lower()
    # remove parts of text in brackets [...], because it is
    # usually something like [Chorus], [Verse 1] etc.
    # we don't need that
    clean_text = re.sub(r'\[(?:[^\]|]*\|)?([^\]|]*)\]', ' ', clean_text)
    # remove empty lines and lines containing only whitespaces
    clean_text = os.linesep.join([s for s in clean_text.splitlines() if s.strip()])
    # add whitespaces around punctuation
    clean_text = re.sub('([.,!?()])', r' \1 ', clean_text)
    # replace newlines with whitespace
    clean_text = re.sub('\r\n', ' ', clean_text)
    # replace repeating whitespaces by one whitespace
    clean_text = re.sub(r'\s{2,}', ' ', clean_text)

    return clean_text
