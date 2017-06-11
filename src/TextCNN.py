"""
The definition of the model, which will be trained on collected data
to predict song similarity

by StasyanG
"""

import math
import tensorflow as tf

class TextCNN:
    """
    A CNN for text classification.
    Embedding Layer -> LSTM -> Softmax
    """
    def __init__(self, sequence_length, num_classes, vocab_size, embedding_size):
        # Placeholders for input, output and dropout
        self.input_x = tf.placeholder(tf.int32, [None, sequence_length], name="input_x")
        self.output_y = tf.placeholder(tf.float32, [None, num_classes], name="output_y")

        with tf.device('/cpu:0'), tf.name_scope("embedding"):
            W = tf.Variable(
                tf.random_uniform([vocab_size, embedding_size], -1.0, 1.0),
                name="W")

        with tf.name_scope("lstm"):
            print()

        with tf.name_scope("output_softmax"):
            print()

        with tf.name_scope("loss"):
            print()

        with tf.name_scope("accuracy"):
            print()
