import tensorflow as tf
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

with tf.Session() as sess:
    new_saver = tf.train.import_meta_graph('./my_test_model.meta')
    new_saver.restore(sess, tf.train.latest_checkpoint('./'))
    print(sess.run('w1:0'))
    print(sess.run('w2:0'))