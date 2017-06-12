"""
Notebook file
"""

import numpy as np
import tensorflow as tf
from DatasetBuilder import DatasetBuilder

# Hyperparams
SEQUENCE_LENGTH = 200 # max text length
NUM_CLASSES = 2
BATCH_SIZE = 64 # TODO: ...

# Read data

FLDS = ['track_id', 'artist', 'title', 'similars', 'lyrics_url', 'sample_url']
DATASET = DatasetBuilder(True,
                         'D:\\PROJECT\\data\\train_data', 'D:\\PROJECT\\data\\train_lyrics',
                         'D:\\PROJECT\\data\\test_data', 'D:\\PROJECT\\data\\test_lyrics',
                         FLDS, 0.5)

DATASET.load_from_file('../data/db_test.neg', False, False)
DATASET.load_from_file('../data/db_test.pos', False, True)
DATASET.load_from_file('../data/db_train.neg', True, False)
DATASET.load_from_file('../data/db_train.pos', True, True)
DATASET.info()

#DATASET.read_data(False, 1000)
#DATASET.read_data(True, 10000)
#DATASET.dump('../data/db')
#DATASET.info()

# Join all text data into 2 lists to build vocabulary out of them
TRAIN_DATA = [data_item['data_1'] for data_item in DATASET.train_data['pos']] + \
             [data_item['data_2'] for data_item in DATASET.train_data['pos']] + \
             [data_item['data_1'] for data_item in DATASET.train_data['neg']] + \
             [data_item['data_2'] for data_item in DATASET.train_data['neg']]

TEST_DATA = [data_item['data_1'] for data_item in DATASET.test_data['pos']] + \
            [data_item['data_2'] for data_item in DATASET.test_data['pos']] + \
            [data_item['data_1'] for data_item in DATASET.test_data['neg']] + \
            [data_item['data_2'] for data_item in DATASET.test_data['neg']]

# Build vocabulary
def build_vocab(data, max_seq_length):
    """
    Builds vocabulary from texts and saves it into a file

    Parameters
    ----------
        data (list of str): texts on which vocabulary will be built
        max_seq_length (int): Maximum sequence length

    Returns
    ----------
        None
    """
    vocab_proc = tf.contrib.learn.preprocessing.VocabularyProcessor(max_seq_length)
    vocab_proc.fit(data)

    # Save VocabularyProcessor
    vocab_proc.save('vocab_proc.vp')
    print('Vocabulary\'s saved.')

# build_vocab(TRAIN_DATA + TEST_DATA, SEQUENCE_LENGTH)

# Transform texts using pre-built vocabulary
def transform_data(vocab_proc, data):
    """
    Transforms text data into Word-id matrix using VocabularyProcessor

    Parameters
    ----------
        vocab_processor (VocabularyProcessor): tf.contrib.learn.preprocessing.
        data (list of str): texts to transform

    Returns
    ----------
        t_data: Word-id matrix
    """
    t_data = np.array(list(vocab_proc.transform(data)))
    return t_data

# Initialize VocabularyProcessor
VOCAB_PROCESSOR = tf.contrib.learn.preprocessing.VocabularyProcessor(SEQUENCE_LENGTH)
VOCAB_PROCESSOR.restore('vocab_proc.vp')
print('Vocabulary Size:', len(VOCAB_PROCESSOR.vocabulary_))
# Transform texts
X = transform_data(VOCAB_PROCESSOR, TRAIN_DATA + TEST_DATA)

# Create dataset from transformed texts
X_INPUT_TRAIN_DATA_1 = []
X_INPUT_TRAIN_DATA_2 = []
X_INPUT_TRAIN_SCORE = []

LEN = len(DATASET.train_data['pos'])
for i in range(0, LEN):
    X_INPUT_TRAIN_DATA_1.append(X[i])
    X_INPUT_TRAIN_DATA_2.append(X[i + LEN])
    X_INPUT_TRAIN_SCORE.append(DATASET.train_data['pos'][i]['score'])
for i in range(2 * LEN, 3 * LEN):
    X_INPUT_TRAIN_DATA_1.append(X[i])
    X_INPUT_TRAIN_DATA_2.append(X[i + LEN])
    X_INPUT_TRAIN_SCORE.append(DATASET.train_data['neg'][i - 2 * LEN]['score'])

X_INPUT_TEST_DATA_1 = []
X_INPUT_TEST_DATA_2 = []
X_INPUT_TEST_SCORE = []

LEN2 = len(DATASET.test_data['pos'])
for i in range(4 * LEN, 4 * LEN + LEN2):
    X_INPUT_TEST_DATA_1.append(X[i])
    X_INPUT_TEST_DATA_2.append(X[i + LEN2])
    X_INPUT_TEST_SCORE.append(DATASET.test_data['pos'][i - 4 * LEN]['score'])
for i in range(4 * LEN + 2 * LEN2, 4 * LEN + 3 * LEN2):
    X_INPUT_TEST_DATA_1.append(X[i])
    X_INPUT_TEST_DATA_2.append(X[i + LEN2])
    X_INPUT_TEST_SCORE.append(DATASET.test_data['neg'][i - (4 * LEN + 2 * LEN2)]['score'])

print('Train Dataset Size:', len(X_INPUT_TRAIN_SCORE))
print('Test Dataset Size:', len(X_INPUT_TEST_SCORE))


# We need to cut vocabulary size, because it is too big
VOCAB_SIZE = 40000
