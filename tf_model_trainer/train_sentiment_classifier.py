#!/usr/bin/env python3

"""
    This is a script for training a RNN with LSTM to predict text sentiment
    Model Structure:
        1. Vectorized word embedding encoder
        2. RNN with 2 LSTM layers
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.layers import LSTM
import tensorflow_datasets as tfds
import tensorflow as tf
from tensorflow.keras import layers


# CONFIGURE MODEL
BATCH_SIZE = 32
EPOCH_SIZE = 100
N_TRAIN = int(1e4)
STEPS_PER_EPOCH = N_TRAIN // BATCH_SIZE
# CONFIGURE VOCAB ENCODER
VOCAB_SIZE = 2500


def plot_graphs(history, metric):
    plt.plot(history.history[metric])
    plt.plot(history.history['val_' + metric], '')
    plt.xlabel("Epochs")
    plt.ylabel(metric)
    plt.legend([metric, 'val_' + metric])


def partition_dataset(ds, ds_size,
                      train_split=0.8,
                      val_split=0.1,
                      test_split=0.1,
                      shuffle=True,
                      shuffle_size=10000):
    assert (train_split + test_split + val_split) == 1

    if shuffle:
        # Specify seed to always have the same split distribution between runs
        ds = ds.shuffle(shuffle_size, seed=12)

    train_size = int(train_split * ds_size)
    val_size = int(val_split * ds_size)

    train_ds = ds.take(train_size)
    val_ds = ds.skip(train_size).take(val_size)
    test_ds = ds.skip(train_size).skip(val_size)

    return train_ds, val_ds, test_ds


def load_dataset(ds_path):
    # LOAD DATASET as PANDAS DATA_FRAME
    comments_csv = pd.read_csv(ds_path,
                               sep=";")

    print()
    print("Full Dataset")
    print(comments_csv)
    print()

    # BUILD TENSOR FROM TEXT COLUMN, Type = String
    sentiment_text = tf.convert_to_tensor(comments_csv["text"],
                                          dtype=tf.string)

    # BUILD TENSOR FROM LABEL COLUMN, 0 = Negative, 1 = Positive
    sentiment_label = tf.convert_to_tensor(comments_csv["label"],
                                           dtype=tf.int32)

    # JOIN TENSORS TO FORM TF.DATASET OBJECT
    init_dataset = tf.data.Dataset.from_tensor_slices(
        (sentiment_text, sentiment_label))

    print()
    print(init_dataset)
    print()

    # SPLIT DATASET FOR TRAINING
    train_ds, valid_ds, test_ds = partition_dataset(ds=init_dataset,
                                                    ds_size=len(init_dataset),
                                                    train_split=0.7,
                                                    val_split=0.15,
                                                    test_split=0.15,
                                                    shuffle=True,
                                                    shuffle_size=len(init_dataset))
    print()
    print("Split dataset sizes:")
    print("Train_DS Size: {}".format(len(train_ds)))
    print("Valid_DS Size: {}".format(len(valid_ds)))
    print("Test_DS Size: {}".format(len(test_ds)))
    print()

    train_ds = train_ds.batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)
    valid_ds = valid_ds.batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)
    test_ds = test_ds.batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)

    return train_ds, valid_ds, test_ds


def build_model(train_ds):
    # CREATE INPUT ENCODER
    encoder = tf.keras.layers.TextVectorization(
        max_tokens=VOCAB_SIZE)
    encoder.adapt(train_ds.map(lambda text, label: text))

    vocab = np.array(encoder.get_vocabulary())

    # ASSEMBLE THE MODEL
    model = tf.keras.Sequential([
        encoder,
        tf.keras.layers.Embedding(
            len(encoder.get_vocabulary()), 64, mask_zero=True),
        tf.keras.layers.Bidirectional(LSTM(64,
                                return_sequences=True)),
        tf.keras.layers.Bidirectional(LSTM(32, dropout=0.2)),
        tf.keras.layers.Dense(64, activation='relu'),
        #tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(1)
    ])
    print(model.summary())
    return model


def train_model(train_ds, valid_ds, model):
    # ModelCheckpoint to save model in case of interrupting the learning process
    checkpoint = ModelCheckpoint(
        "sentiment_checkpoint.tf",
        monitor="val_loss",
        mode="min",
        save_best_only=True,
        verbose=0)

    # EarlyStopping to find best model with a large number of epochs
    earlystop = EarlyStopping(
        monitor='val_loss',
        restore_best_weights=True,
        patience=10,
        verbose=1)

    # USED TO DECREASE LR OVER TIME
    lr_schedule = tf.keras.optimizers.schedules.InverseTimeDecay(
        0.1,
        decay_steps=1.0,
        decay_rate=0.1,
        staircase=False)

    model.compile(
        loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
        optimizer=tf.keras.optimizers.Adam(learning_rate=lr_schedule),
        metrics=['accuracy'])

    callbacks = [earlystop, checkpoint]

    history = model.fit(
        train_ds,
        epochs=EPOCH_SIZE,
        validation_data=valid_ds)
        callbacks=callbacks)
    return history


def display_results(history, test_loss, test_accuracy):
    print('Test Loss:', test_loss)
    print('Test Accuracy:', test_accuracy)

    plt.figure(figsize=(16, 8))
    plt.subplot(1, 2, 1)
    plot_graphs(history, 'accuracy')
    plt.ylim(None, 1)
    plt.subplot(1, 2, 2)
    plot_graphs(history, 'loss')
    plt.ylim(0, None)

    plt.savefig('fig_1.png', bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

    ds_path = "sentiment_dataset.csv"
    train_ds, valid_ds, test_ds = load_dataset(ds_path)
    model = build_model(train_ds)
    history = train_model(train_ds, valid_ds, model)
    # SAVE THE TRAINED MODEL
    model.save("sentiment_classifier.tf", save_format='tf')
    test_loss, test_accuracy = model.evaluate(test_ds)

    display_results(history, test_loss, test_accuracy)
