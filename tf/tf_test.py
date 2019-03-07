from __future__ import print_function
import tensorflow as tf

welcome = tf.constant('Welcome to tensorflow.')

with tf.Session() as sess:
    sess.run(welcome)
sess.close()