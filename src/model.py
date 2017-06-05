"""
The definition of the model, which will be trained on collected data
to predict song similarity

by StasyanG
"""
from __future__ import absolute_import, division, print_function

import sys
import os
import simplejson as json
import tensorflow as tf

import preprocessing

def read_track_data(filename, fields):
    """
    Reads track data from json file

    Parameters
    ----------
        filename (str): Path to the file with track data
        fields (list): Fields of track that we need

    Returns
    ----------
        data_item (dict): Track data (only fields that we need)
    """
    data_item = {}
    try:
        with open(filename) as fp_in:
            track_data = json.load(fp_in)
            for field in fields:
                data_item[field] = track_data[field]
    except json.decoder.JSONDecodeError:
        print('JSON Decoding problem [', filename, ']')

    return data_item

def read_lyrics_data(filename):
    """
    Gets lyrics from file and returns cleaned lyrics as a list of words

    Parameters
    ----------
        filename (str): Path to the file with lyrics

    Returns
    ----------
        data (list): List of strings (words in lyrics)
    """
    with open(filename) as file:
        lyrics = file.read()
        clean_lyrics = preprocessing.clean_lyrics(lyrics)
        data = tf.compat.as_str(clean_lyrics).split()
    return data

def read_data(data_path, lyrics_path, samples_path=None, max_cnt=None):
    """
    Reads track data from data_folder and gets lyrics for it in lyrics_folder

    Parameters
    ----------
        data_path (str): Path to the folder with track data
        lyrics_path (str): Path to the folder with lyrics
        samples_path (str): Path to the folder with audio samples

    Returns
    ----------
        data (list): List of track data items
    """
    data = []
    cnt = 0
    exit_flag = False
    for root, dirs, files in os.walk(data_path):
        for sfile in files:
            if sfile.endswith(".json"):
                filename = sfile[:(sfile.rfind('-') if '-' in sfile else sfile.rfind('.'))]
                path = os.path.join(root, sfile)

                data_item = {}

                # get track data
                fields = ['track_id', 'artist', 'title', 'similars', 'lyrics_url', 'sample_url']
                data_item = read_track_data(path, fields)

                ### TODO: rethink this (because it is used in another files)
                extension = ".txt"
                lyrics_path = os.path.join(lyrics_path, filename + extension)

                # get lyrics data
                if os.path.isfile(lyrics_path):
                    lyrics_data = read_lyrics_data(lyrics_path)
                    if lyrics_data:
                        data_item['lyrics_data'] = lyrics_data
                # if no lyrics -> continue (we can't use this track)
                if not lyrics_data:
                    continue

                ### TODO: get sample data
                if samples_path:
                    None
                    # do something

                data.append(data_item)
                cnt += 1
                if max_cnt and cnt >= max_cnt:
                    exit_flag = True
                    break
        if exit_flag:
            break

    return data

def main(data_path, lyrics_path):
    """ Main function (temporary) """
    print('The model')
    test_data = read_data(data_path, lyrics_path, max_cnt=5)
    print(str(test_data).encode(sys.stdout.encoding, errors='replace'))

if __name__ == "__main__":
    main('data\\test_data', 'data\\test_lyrics')


