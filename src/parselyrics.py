"""
Script to parse Genius song page with lyrics
The task is to get only text

by StasyanG
"""
from __future__ import absolute_import, division, print_function

import argparse
import sys
import os
import json

from bs4 import BeautifulSoup

import utils

def get_lyrics_text(lyrics_url):
    """
    Overview
    ----------
    Gets lyrics text from the page that can be accessed via given URL

    Parameters
    ----------
    lyrics_url (string): \n
    \t Lyrics page URL \n

    Returns
    ----------
    lyrics_text (string): \n
    \t Lyrics text \n
    """

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'
    }

    page_html = utils.get_request(lyrics_url, headers=headers)
    bsoup = BeautifulSoup(page_html, "lxml")
    lyrics_text = bsoup.find('div', {'class': 'lyrics'}).text
    return utils.ascii_string(lyrics_text)

def store_lyrics_text(target_path, track_id, text):
    """
    Overview
    ----------
    Stores lyrics text into a file

    Parameters
    ----------
    target_path (string): \n
    \t Absolute path to the target folder \n
    track_id (string): \n
    \t Track ID (LastFM dataset) \n
    text (string): \n
    \t Lyrics text to write \n

    Returns
    ----------
    None
    """
    file_path = os.path.join(target_path, track_id + '.txt')
    print(file_path)
    with open(file_path, 'w') as fp_out:
        fp_out.write(text)

def main(data_path, target_path, start_index=None):
    """
    Overview
    ----------
    Goes through data folder with json files containing track data with lyrics URLs inside.
    Then gets lyrics page and extract only text from it. After that it stores this text
    in a file in target folder (target_path) \n
    (e.g. TRBBBNA12903CB336B.json ==> TRBBBNA12903CB336B-lyrics.txt)

    Parameters
    ----------
    data_path (string): \n
    \t Absolute path to the folder with tracks data \n
    target_fodler (string): \n
    \t Absolute path to the folder where to put files with lyrics \n

    Returns
    ----------
    None
    """

    sindex = start_index
    for root, dirs, files in os.walk(data_path):
        for sfile in files:
            if sfile.endswith(".json"):
                # get file name (track id) to compare with start_index
                if sindex is not None:
                    filename = sfile[:(sfile.rfind('-') if '-' in sfile else sfile.rfind('.'))]
                    if sindex == filename:
                        sindex = None
                    else:
                        continue

                path = os.path.join(root, sfile)
                # get data from .json file
                track_data = None
                with open(path) as fp_in:
                    track_data = json.load(fp_in)
                print('...')

                track_id = None
                lyrics_url = None
                if track_data and 'lyrics_url' in track_data.keys():
                    track_id = track_data['track_id']
                    lyrics_url = track_data['lyrics_url']
                else:
                    print('No lyrics data')
                    continue

                if lyrics_url:
                    print(lyrics_url)
                    lyrics_text = get_lyrics_text(lyrics_url)
                    store_lyrics_text(target_path, track_id, lyrics_text)
                else:
                    print('No lyrics data')
                    continue

    return

if __name__ == "__main__":
    print(sys.argv[0])
    print('\nScript to parse Genius song page with lyrics')

    PARSER = argparse.ArgumentParser()
    PARSER.add_argument("-d", "--data", help="Path to the folder with tracks' data")
    PARSER.add_argument("-t", "--target", help="Path to the folder where to put files with lyrics")
    PARSER.add_argument("-s", "--start", help="Track ID to start from (e.g. TRARYTX128F145F6AA)")
    ARGS = PARSER.parse_args()

    DATA_PATH = ARGS.data
    TARGET_PATH = ARGS.target
    START_INDEX = ARGS.start

    print('\nData folder:', DATA_PATH)
    print('Target folder:', TARGET_PATH, end='\n\n')
    if START_INDEX:
        print('Start index:', START_INDEX, end='\n\n')
    else:
        print()

    main(DATA_PATH, TARGET_PATH, START_INDEX)
