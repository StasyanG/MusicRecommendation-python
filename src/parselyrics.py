"""
Script to parse Genius song page with lyrics
The task is to get only text

by StasyanG
"""
from __future__ import absolute_import, division, print_function

import sys
import os

def parse_page(html):
    """
    Overview
    ----------
    Parse html page and get only lyrics (as text) from it

    Parameters
    ----------
    html (object):
        Object containing DOM tree of a page

    Returns
    ----------
    (string):
        String containing song lyrics
    """
    return

def main(data_path, target_path):
    """
    Overview
    ----------
    Goes through data folder with json files containing track data with lyrics URLs inside.
    Then gets lyrics page and extract only text from it. After that it stores this text
    in a file in target folder (target_path) \n
    (e.g. TRBBBNA12903CB336B.json ==> TRBBBNA12903CB336B-lyrics.txt)

    Parameters
    ----------
    data_path (string):
        Absolute path to the folder with tracks' data
    target_fodler (string):
        Absolute path to the folder where to put files with lyrics

    Returns
    ----------
    None
    """
    return

if __name__ == "__main__":
    print(sys.argv[0])
    print('\nScript to parse Genius song page with lyrics')

    PARSER = argparse.ArgumentParser()
    PARSER.add_argument("-d", "--data", help="Path to the folder with tracks' data")
    PARSER.add_argument("-t", "--target", help="Path to the folder where to put files with lyrics")
    ARGS = PARSER.parse_args()

    DATA_PATH = ARGS.data
    TARGET_PATH = ARGS.target

    print('\nData folder:', DATA_PATH)
    print('Target folder:', TARGET_PATH, end='\n\n')

    main(DATA_PATH, TARGET_PATH)
