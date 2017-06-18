"""
Helper class to create dataset containing equal
amount of positive and negative examples.
"""

import os
import simplejson as json

import preprocessing
import utils

class DatasetBuilder:
    """
    Helper class to create dataset containing equal
    amount of positive and negative examples.
    """
    def __init__(self, is_text,
                 train_data_folder, train_lyrics_folder,
                 test_data_folder, test_lyrics_folder,
                 data_fields, pos_neg_threshold):
        self.train_data_folder = train_data_folder
        self.train_lyrics_folder = train_lyrics_folder
        self.test_data_folder = test_data_folder
        self.test_lyrics_folder = test_lyrics_folder
        self.data_fields = data_fields
        self.is_text = is_text

        self.pos_neg_threshold = pos_neg_threshold

        self.train_data = {
            'pos': [],
            'neg': []
        }
        self.test_data = {
            'pos': [],
            'neg': []
        }

        print('DataBuilder initialized.')

    def info(self):
        """
        Prints dataset info
        """
        print('Dataset Info')
        print('> Train set:')
        print('> > Positive:', len(self.train_data['pos']))
        print('> > Negative:', len(self.train_data['neg']))
        print('> Test set:')
        print('> > Positive:', len(self.test_data['pos']))
        print('> > Negative:', len(self.test_data['neg']))

    def dump(self, name):
        """
        Dumps dataset into 4 files
        """
        with open(name + '_train.pos', 'w') as fp_out:
            json.dump(self.train_data['pos'], fp_out)
        with open(name + '_train.neg', 'w') as fp_out:
            json.dump(self.train_data['neg'], fp_out)
        with open(name + '_test.pos', 'w') as fp_out:
            json.dump(self.test_data['pos'], fp_out)
        with open(name + '_test.neg', 'w') as fp_out:
            json.dump(self.test_data['neg'], fp_out)

    def read_data(self, is_train, max_pos=None, verbose=False):
        """
        Fills self.train_data or self.test_data structures with train/test samples.

        Parameters
        ----------
            is_train (boolean): True if train data, False if test data
            max_pos (int): Maximum of positive/negative samples in dataset
            verbose (boolean): Show info on each addition to dataset

        Returns
        ----------
            None
        """

        cnt = 0
        cnt2 = 0

        if is_train is True:
            data_path = self.train_data_folder
            lyrics_path = self.train_lyrics_folder
            cnt = len(self.train_data['pos'])
            cnt2 = len(self.train_data['neg'])
        elif is_train is False:
            data_path = self.test_data_folder
            lyrics_path = self.test_lyrics_folder
            cnt = len(self.test_data['pos'])
            cnt2 = len(self.test_data['neg'])
        else:
            print('Please, provide train parameter')
            return -1

        if cnt >= max_pos and cnt2 >= max_pos:
            print('Dataset is full (', max_pos, ')')
            return -1

        for root, _, files in os.walk(data_path):
            for sfile in files:
                if sfile.endswith(".json"):
                    filename = sfile[:(sfile.rfind('-') if '-' in sfile else sfile.rfind('.'))]
                    path = os.path.join(root, sfile)

                    data_item = {}

                    # get track data
                    data_item = self._read_track_data(path)

                    if self.is_text is True:
                        ### TODO: Rethink this (because it is used in another files)
                        extension = ".txt"

                        lyrics_file = os.path.join(lyrics_path, filename + extension)

                        # get lyrics data
                        if os.path.isfile(lyrics_file):
                            lyrics_data = self._read_lyrics_data(lyrics_file)
                            if lyrics_data:
                                data_item['lyrics_data'] = lyrics_data
                        # if no lyrics -> continue (we can't use this track)
                        if 'lyrics_data' not in data_item or not lyrics_data:
                            continue
                    else:
                        ### TODO: Maybe there is a better way of getting sample data
                        sample_url = data_item['sample_url']
                        if sample_url:
                            s_data = self._read_sample_data(sample_url)
                            data_item['sample_data'] = s_data

                    for similar in data_item['similars']:

                        score = similar[1]
                        similar = similar[0]

                        if score >= self.pos_neg_threshold and max_pos and cnt >= max_pos:
                            continue
                        elif score < self.pos_neg_threshold and max_pos and cnt2 >= max_pos:
                            continue


                        if is_train is True:
                            is_data_pos = self._is_in_dataset(
                                self.train_data['pos'], 'pair', (data_item['track_id'], similar)
                                )
                            is_data_pos = is_data_pos or self._is_in_dataset(
                                self.train_data['pos'], 'pair', (similar, data_item['track_id'])
                                )
                            is_data_neg = self._is_in_dataset(
                                self.train_data['neg'], 'pair', (data_item['track_id'], similar)
                                )
                            is_data_neg = is_data_neg or self._is_in_dataset(
                                self.train_data['neg'], 'pair', (similar, data_item['track_id'])
                                )
                        else:
                            is_data_pos = self._is_in_dataset(
                                self.test_data['pos'], 'pair', (data_item['track_id'], similar)
                                )
                            is_data_pos = is_data_pos or self._is_in_dataset(
                                self.test_data['pos'], 'pair', (similar, data_item['track_id'])
                                )
                            is_data_neg = self._is_in_dataset(
                                self.test_data['neg'], 'pair', (data_item['track_id'], similar)
                                )
                            is_data_neg = is_data_neg or self._is_in_dataset(
                                self.test_data['neg'], 'pair', (similar, data_item['track_id'])
                                )
                        if is_data_pos or is_data_neg:
                            continue

                        sim_filename = similar + \
                            sfile[(sfile.rfind('-') if '-' in sfile else sfile.rfind('.')):]
                        sim_path = os.path.join(root, sim_filename)
                        sim_data = self._read_track_data(sim_path)

                        if not sim_data:
                            continue

                        if self.is_text is True:
                            sim_lyrics_path = os.path.join(lyrics_path, similar + extension)
                            sim_lyrics_data = None
                            if os.path.isfile(sim_lyrics_path):
                                sim_lyrics_data = self._read_lyrics_data(sim_lyrics_path)
                                if sim_lyrics_data:
                                    sim_data['lyrics_data'] = sim_lyrics_data
                            # if no lyrics -> continue (we can't use this track)
                            if not sim_lyrics_data:
                                continue
                        else:
                            sim_sample_url = sim_data['sample_url']
                            if sim_sample_url:
                                s_data = self._read_sample_data(sim_sample_url)
                                sim_data['sample_data'] = s_data

                        new_item = {
                            'pair': (data_item['track_id'], similar),
                            'data_1': data_item['lyrics_data'] if self.is_text is True else data_item['sample_data'],
                            'data_2': sim_data['lyrics_data'] if self.is_text is True else sim_data['sample_data'],
                            'score': 1 if score >= self.pos_neg_threshold else 0
                        }
                        if score >= self.pos_neg_threshold:
                            if is_train is True:
                                self.train_data['pos'].append(new_item)
                            else:
                                self.test_data['pos'].append(new_item)
                            cnt += 1
                            if verbose:
                                print()
                                self.info()
                        else:
                            if is_train is True:
                                self.train_data['neg'].append(new_item)
                            else:
                                self.test_data['neg'].append(new_item)
                            cnt2 += 1
                            if verbose:
                                print()
                                self.info()
                        if max_pos and cnt >= max_pos and cnt2 >= max_pos:
                            break
                    if max_pos and cnt >= max_pos and cnt2 >= max_pos:
                        break
            if max_pos and cnt >= max_pos and cnt2 >= max_pos:
                break

    def load_from_file(self, filename, is_train, is_pos):
        """
        Reads dataset data from file
        """
        with open(filename) as fp_in:
            data = json.load(fp_in)
            if is_train is True:
                if is_pos is True:
                    self.train_data['pos'] = data
                else:
                    self.train_data['neg'] = data
            else:
                if is_pos is True:
                    self.test_data['pos'] = data
                else:
                    self.test_data['neg'] = data

    def _read_track_data(self, filename):
        """
        Reads track data from json file

        Parameters
        ----------
            filename (str): Path to the file with track data

        Returns
        ----------
            data_item (dict): Track data (only fields that we need)
        """
        data_item = {}
        try:
            with open(filename) as fp_in:
                track_data = json.load(fp_in)
                for field in self.data_fields:
                    data_item[field] = track_data[field]
        except FileNotFoundError:
            # print('Warning: File not found [', filename, ']')
            return None
        except json.decoder.JSONDecodeError:
            print('JSON Decoding problem [', filename, ']')

        return data_item

    def _read_lyrics_data(self, filename):
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
            #data = tf.compat.as_str(clean_lyrics).split()
            data = clean_lyrics
        return data

    def _read_sample_data(self, url):
        """
        Gets sample file from URL and returns its' representation as audio spectrum data
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko)'
                          + ' Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'
        }
        data = utils.get_request(url, headers=headers)
        if data:
            with open('tmp.mp3', 'wb') as f_out:
                f_out.write(data)

            data = preprocessing.read_audio_spectrogram('tmp.mp3')
            os.remove('tmp.mp3')
        return data

    def _is_in_dataset(self, dataset, field, value):

        res = False
        for item in dataset:
            if item[field] is value:
                res = True
                break
        return res
