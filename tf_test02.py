"""
Autoencoder

Ref:Tensorflow in action chapter 4
"""

import numpy as np
import sklearn.preprocessing as prep
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data


def xavier_init(fan_in, fan_out, constant=1):
    """
    function to initialize weight. The weights initialized by xavier_init should have 2/(fan_in+fan_out) as it's variance
    :param fan_in: number of input node
    :param fan_out: number of output node
    :param constant:
    :return:
    """
    low = -constant * np.sqrt(6.0 / (fan_in+fan_out))
    high = constant * np.sqrt(6.0/(fan_in+fan_out))
    return tf.random_uniform((fan_in,fan_out), minval= low, maxval=high, dtype=tf.float32)


class AdditiveGaussianNoiseAutoencoder(object):


    def __init__(self,n_input, n_hidden, transfer_function = tf.nn.softplus, optimizer = tf.train.AdamOptimizer(), scale = 0.1):
        """

        :param n_input: input number
        :param n_hidden: hidden layer node number
        :param transfer_function: activation function, use softplus as default
        :param optimizer: use adam as default
        :param scale: scale of gaussian noise
        """
        self.n_input = n_input
        self.n_hidden = n_hidden
        self.transfer = transfer_function
        self.scale = tf.placeholder(tf.float32)
        self.training_scale = scale
        network_weights = self._initialize_weights()
        self.weights = network_weights

        # defination of the architecture of the neural network
        self.x = tf.placeholder(tf.float32,[None, self.n_input])
        self.hidden = self.transfer(tf.add(tf.matmul(
            self.x + scale * tf.random_normal((n_input,)),
            self.weights['w1']),self.weights['b1']
        ))
        self.reconstruction = tf.add(tf.matmul(self.hidden, self.weights['w2']), self.weights['b2'])