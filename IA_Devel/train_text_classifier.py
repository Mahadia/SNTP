#!/usr/bin/env python3

"""
    This is a script for training a RNN with LSTM to predict text sentiment
    Model Structure:
        1. Vectorized word embedding encoder
        2. RNN with 2 LSTM layers
"""

from tensorflow.keras import layers
import tensorflow as tf
import tensorflow_datasets as tfds
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

np.set_printoptions(precision=3, suppress=True)


def plot_graphs(history, metric):
    plt.plot(history.history[metric])
    plt.plot(history.history['val_' + metric], '')
    plt.xlabel("Epochs")
    plt.ylabel(metric)
    plt.legend([metric, 'val_' + metric])


# LOAD COMMENTS CSV DATASET
comments_csv = pd.read_csv(
    "comments.csv",
    names=["text", "label"],
    sep=";")

comments_text = tf.convert_to_tensor(comments_csv["text"], dtype=tf.string)
comments_label = tf.convert_to_tensor(comments_csv["label"], dtype=tf.int64)

comments_ds = tf.data.Dataset.from_tensor_slices(
    (comments_text, comments_label))

# LOAD IMDB REVIEWS DATASET
imdb_ds, info = tfds.load('imdb_reviews',
                          split='train+test',
                          with_info=True,
                          as_supervised=True)

print(imdb_ds)
print('imdb size: {}'.format(len(imdb_ds)))

full_dataset = comments_ds.concatenate(imdb_ds)

print()
print(full_dataset)
print("Full_Size: {}".format(len(full_dataset)))
print()

DATASET_SIZE = len(full_dataset)

train_size = int(0.6 * DATASET_SIZE)
val_size = int(0.25 * DATASET_SIZE)
test_size = int(0.15 * DATASET_SIZE)


full_dataset = full_dataset.shuffle(DATASET_SIZE)
train_dataset = full_dataset.take(train_size)
test_dataset = full_dataset.skip(train_size)
val_dataset = test_dataset.skip(val_size)
test_dataset = test_dataset.take(test_size)

print()
print('Full Dataset: ' + str(len(full_dataset)))
print("Train Dataset: " + str(len(train_dataset)))
print(train_dataset)
print("Validation Dataset: " + str(len(val_dataset)))
print(val_dataset)
print("Test Dataset: " + str(len(test_dataset)))
print(test_dataset)
print()

# CONFIGURE MODEL
BUFFER_SIZE = 10000
BATCH_SIZE = 64

train_dataset = train_dataset.batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)
val_dataset = val_dataset.batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)
test_dataset = test_dataset.batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)

# CREATE INPUT ENCODER
VOCAB_SIZE = 1000
encoder = tf.keras.layers.TextVectorization(
    max_tokens=VOCAB_SIZE)
encoder.adapt(train_dataset.map(lambda text, label: text))

vocab = np.array(encoder.get_vocabulary())


# THE MODEL
model = tf.keras.Sequential([
    encoder,
    tf.keras.layers.Embedding(
        len(encoder.get_vocabulary()), 64, mask_zero=True),
    tf.keras.layers.Bidirectional(
        tf.keras.layers.LSTM(64,  return_sequences=True)),
    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(32)),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(1)
])

model.compile(loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
              optimizer=tf.keras.optimizers.Adam(1e-4),
              metrics=['accuracy'])

history = model.fit(train_dataset, epochs=10,
                    validation_data=val_dataset,
                    validation_steps=30)

model.save_weights("test_weights", save_format='tf')
model.save_weights("test_classifier", save_format='tf')

test_loss, test_acc = model.evaluate(test_dataset)

print('Test Loss:', test_loss)
print('Test Accuracy:', test_acc)

plt.figure(figsize=(16, 8))
plt.subplot(1, 2, 1)
plot_graphs(history, 'accuracy')
plt.ylim(None, 1)
plt.subplot(1, 2, 2)
plot_graphs(history, 'loss')
plt.ylim(0, None)

plt.show()
