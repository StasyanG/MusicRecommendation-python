"""
Data Preprocessing

by StasyanG
"""

import os
import re
import numpy as np
import librosa

def clean_lyrics(text):
    """
    Cleans lyrics text

    Parameters
    ----------
        text (str): Lyrics text

    Returns
    ----------
        clean_text (str): Cleaned text
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
    clean_text = re.sub('([.,!?()])', r' ', clean_text)
    # replace newlines with whitespace
    clean_text = re.sub('\r\n', ' ', clean_text)
    # replace repeating whitespaces by one whitespace
    clean_text = re.sub(r'\s{2,}', ' ', clean_text)
    
    clean_text = clean_text.strip()

    return clean_text

def read_audio_spectrogram(filename):
    """
    Reads spectrogram data from the given audio file

    Parameters
    ----------
        filename (str): Path to the audio file

    Returns
    ----------
        stft_matrix (array): ** See Docs for ibrosa.core.stft
    """
    # loading audio data
    audio_data, _ = librosa.load(filename)
    # Short-time Fourier transform
    stft_matrix = librosa.stft(audio_data)
    ### TODO: Think about audio representation as a spectrogram
    # Get only phases
    phase_matrix = np.abs(stft_matrix)

    return phase_matrix
