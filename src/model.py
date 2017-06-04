"""
The definition of the model, which will be trained on collected data
to predict song similarity

by StasyanG
"""
from __future__ import absolute_import, division, print_function

import tensorflow as tf
import preprocessing

def read_lyrics_data(filename):
    """
    Gets lyrics from file and returns cleaned lyrics as a list of words

    Parameters
    ----------
    filename (string):
        Path to the file with lyrics

    Returns
    ----------
    data (list):
        List of strings (words in lyrics)
    """
    with open(filename) as file:
        lyrics = file.read()
        clean_lyrics = preprocessing.clean_lyrics(lyrics)
        data = tf.compat.as_str(clean_lyrics).split()
    return data

if __name__ == "__main__":
    print('The model')
