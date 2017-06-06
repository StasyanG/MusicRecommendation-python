"""
The definition of the model, which will be trained on collected data
to predict song similarity
AND
helper-functions

by StasyanG
"""
from __future__ import absolute_import, division, print_function

import sys
import os
import simplejson as json
import tensorflow as tf

import preprocessing
import utils

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

def read_sample_data(url):
    """
    Gets sample file from URL and returns its' representation as audio spectrum data
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                      + 'AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'
    }
    data = utils.get_request(url, headers=headers)
    with open('tmp.mp3', 'wb') as f_out:
        f_out.write(data)

    s_data = preprocessing.read_audio_spectrogram('tmp.mp3')
    os.remove('tmp.mp3')
    return s_data

def read_data(data_path, lyrics_path, fields, max_cnt=None):
    """
    Reads track data from data_folder and gets lyrics for it in lyrics_folder

    Parameters
    ----------
        data_path (str): Path to the folder with track data
        lyrics_path (str): Path to the folder with lyrics

    Returns
    ----------
        data (list): List of track data items
    """
    data = []
    cnt = 0
    for root, _, files in os.walk(data_path):
        for sfile in files:
            if sfile.endswith(".json"):
                filename = sfile[:(sfile.rfind('-') if '-' in sfile else sfile.rfind('.'))]
                path = os.path.join(root, sfile)

                data_item = {}

                # get track data
                data_item = read_track_data(path, fields)

                ### TODO: Rethink this (because it is used in another files)
                extension = ".txt"

                lyrics_file = os.path.join(lyrics_path, filename + extension)

                # get lyrics data
                if os.path.isfile(lyrics_file):
                    lyrics_data = read_lyrics_data(lyrics_file)
                    if lyrics_data:
                        data_item['lyrics_data'] = lyrics_data
                # if no lyrics -> continue (we can't use this track)
                if not lyrics_data:
                    continue

                ### TODO: Maybe there is a better way of getting sample data
                sample_url = data_item['sample_url']
                if sample_url:
                    s_data = read_sample_data(sample_url)
                    data_item['sample_data'] = s_data

                data.append(data_item)
                cnt += 1
                if max_cnt and cnt >= max_cnt:
                    break
        if max_cnt and cnt >= max_cnt:
            break

    return data

def main(data_path, lyrics_path):
    """ Main function (temporary) """
    print('The model')

    fields = ['track_id', 'artist', 'title', 'similars', 'lyrics_url', 'sample_url']
    test_data = read_data(data_path, lyrics_path, fields, max_cnt=5)

    print(str(test_data).encode(sys.stdout.encoding, errors='replace'))

if __name__ == "__main__":
    main('data\\test_data', 'data\\test_lyrics')


