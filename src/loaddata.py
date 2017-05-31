"""
Script to complete LastFM dataset with samples from Deezer and lyrics from Genius

by StasyanG
"""
from __future__ import absolute_import, division, print_function

import sys
import os
import simplejson as json
import utils

def get_sample_url(track_data):
    """
    Overview
    ----------
    Gets URL of sample file from Deezer using its API

    Parameters
    ----------
    track_data (dict):
        Track data from LastFM dataset

    Returns
    ----------
    url (string):
        Sample file URL
    """
    artist = track_data['artist']
    title = track_data['title']
    params = {
        'q': artist + ' ' + title
    }
    response = utils.get_request(
        'http://api.deezer.com/search', parameters=params
        )
    obj = json.loads(response.decode())
    if 'error' in obj.keys():
        print('Could not get sample URL for "' + utils.ascii_string(artist) + ' - ' + utils.ascii_string(title) + '"')
        print('Error code:', obj['error']['code'])
        print('Error message:', obj['error']['message'])
        return None
    else:
        data = obj['data']
        if len(data) is 0:
            return None
        else:
            track = data[0]
            return track['preview'] if 'preview' in track.keys() else None

def get_lyrics_url(track_data, client_access_token):
    """
    Overview
    ----------
    Gets lyrics page URL from Genius using its API

    Parameters
    ----------
    track_data (dict):
        Track data from LastFM dataset
    client_access_token (string):
        Client Access Token for Genius API

    Returns
    ----------
    url (string):
        Lyrics page URL
    """
    artist = track_data['artist']
    title = track_data['title']
    params = {
        'access_token': client_access_token,
        'q': artist + ' ' + title,
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'
        }
    response = utils.get_request(
        'https://api.genius.com/search', parameters=params, headers=headers
        )
    obj = json.loads(response.decode())
    status = obj['meta']['status']
    if status == 200:
        hits = obj['response']['hits']
        if len(hits) is 0:
            print('Could not get lyrics for "' + utils.ascii_string(artist) + ' - ' + utils.ascii_string(title) + '"')
            print('Track not found')
            return None
        else:
            url = None
            for hit in hits:
                track = hit['result']
                art = track['primary_artist']['name']
                tit = track['title']
                #print(utils.ascii_string(art))
                #print(utils.ascii_string(artist))
                #print(utils.ascii_string(tit))
                #print(utils.ascii_string(title))
                if art == artist and tit == title:
                    url = track['url']
                    break

            if url is not None:
                return url
            else:
                print('Could not get lyrics for "' + utils.ascii_string(artist) + ' - ' + utils.ascii_string(title) + '"')
                print('Lyrics not found')
                return None
    else:
        print('Could not get lyrics for "' + utils.ascii_string(artist) + ' - ' + utils.ascii_string(title) + '"')
        print('Status code:', status)
        return None

def load_data(src_folder, target_folder, client_access_token):
    """
    Overview
    ----------
    Goes through data folder (LastFM dataset) and for each track tries to get
    sample file URL (from Deezer) and lyrics page URL (from Genius)
    If sample URL and lyrics are found then we create new .json file with
    updated track data
    It does not overwrite LastFM dataset - it creates files with the same name
    plus suffix (e.g. TRBBBNA12903CB336B.json ==> TRBBBNA12903CB336B-upd.json)

    Parameters
    ----------
    src_folder (string):
        Absolute path to the folder with LastFM dataset
    target_fodler (string):
        Absolute path to the folder where to put new track data

    Returns
    ----------
    None
    """
    for root, dirs, files in os.walk(src_folder):
        for file in files:
            if file.endswith(".json"):
                path = os.path.join(root, file)
                # get data from .json file
                track_data = None
                with open(path) as fp_in:
                    track_data = json.load(fp_in)
                print('...')
                # get sample URL from Deezer
                sample_url = get_sample_url(track_data)
                if sample_url is not None:
                #print('Sample URL "' + track_data['artist'] + ' - ' + track_data['title'] + '"')
                    print(sample_url)
                else:
                    continue
                # get lyrics from Genius
                lyrics_url = get_lyrics_url(track_data, client_access_token)
                if lyrics_url is not None:
                #print('Lyrics URL "' + track_data['artist'] + ' - ' + track_data['title'] + '"')
                    print(lyrics_url)
                else:
                    continue

                # add new fields to track_data dict
                track_data['sample_url'] = sample_url
                track_data['lyrics_url'] = lyrics_url

                # store new track_data to a new file
                new_path = os.path.join(target_folder, file[:file.rfind('.')] + '-upd.json')
                with open(new_path, 'w+') as fp_out:
                    json.dump(track_data, fp_out)
        for dirname in dirs:
            load_data(os.path.join(src_folder, dirname), target_folder, client_access_token)


if __name__ == "__main__":
    print(sys.argv[0])
    print('\nScript to complete LastFM dataset with samples (Deezer) and lyrics (Genius)')

    DATA_PATH = sys.argv[1] # relative to root path
    TARGET_PATH = sys.argv[2] # relative to root path
    GENIUS_CLIEN_ACCESS_TOKEN = sys.argv[3] # client access token for Genius API

    print('\nData folder:', DATA_PATH)
    print('Target folder:', TARGET_PATH)
    print('Genius client access token:', GENIUS_CLIEN_ACCESS_TOKEN, end='\n\n')

    load_data(DATA_PATH, TARGET_PATH, GENIUS_CLIEN_ACCESS_TOKEN)

