#!/usr/bin/env python3

"""
    This is a script for retraining a RNN with LSTM to predict text sentiment
    Model Structure:
        1. Vectorized word embedding encoder
        2. RNN with 2 LSTM layers
"""

import os
from os.path import exists
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.layers import LSTM
import tensorflow as tf
from tensorflow.keras import layers


# CONFIGURE MODEL
BATCH_SIZE = 32
EPOCH_SIZE = 100
N_TRAIN = int(1e4)
STEPS_PER_EPOCH = N_TRAIN // BATCH_SIZE
# CONFIGURE VOCAB ENCODER
VOCAB_SIZE = 2500

ds_path = "datasets/tmp_dataset.csv"
model_path = "models/sentiment_classifier.tf"
log_path = "logs/logging.json"

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
    comments_csv = pd.read_csv(ds_path, sep=";")

    # BUILD TENSOR FROM TEXT COLUMN, Type = String
    sentiment_text = tf.convert_to_tensor(comments_csv["text"],
                                          dtype=tf.string)

    # BUILD TENSOR FROM LABEL COLUMN, 0 = Negative, 1 = Positive
    sentiment_label = tf.convert_to_tensor(comments_csv["label"],
                                           dtype=tf.int32)

    # JOIN TENSORS TO FORM TF.DATASET OBJECT
    init_dataset = tf.data.Dataset.from_tensor_slices(
        (sentiment_text, sentiment_label))

    # SPLIT DATASET FOR TRAINING
    train_ds, valid_ds, test_ds = partition_dataset(ds=init_dataset,
                                                    ds_size=len(init_dataset),
                                                    train_split=0.7,
                                                    val_split=0.15,
                                                    test_split=0.15,
                                                    shuffle=True,
                                                    shuffle_size=len(init_dataset))

    train_ds = train_ds.batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)
    valid_ds = valid_ds.batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)
    test_ds = test_ds.batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)

    return train_ds, valid_ds, test_ds

def load_model(path):
    return tf.keras.models.load_model(path)

def train_model(train_ds, valid_ds, model):
    # ModelCheckpoint to save model in case of interrupting the learning process
    checkpoint = ModelCheckpoint("models/tmp_classifier.tf",
                                monitor="val_loss",
                                mode="min",
                                save_best_only=True,
                                verbose=0)

    # EarlyStopping to find best model with a large number of epochs
    earlystop = EarlyStopping(monitor='val_loss',
                            restore_best_weights=True,
                            patience=10,
                            verbose=1)

    # USED TO DECREASE LR OVER TIME
    lr_schedule = tf.keras.optimizers.schedules.InverseTimeDecay(0.1,
                                                                decay_steps=1.0,
                                                                decay_rate=0.1,
                                                                staircase=False)

    model.compile(
        loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
        optimizer=tf.keras.optimizers.Adam(learning_rate=lr_schedule),
        metrics=['accuracy'])

    callbacks = [earlystop, checkpoint]

    history = model.fit(train_ds,
                        epochs=EPOCH_SIZE,
                        validation_data=valid_ds,
                        callbacks=callbacks)
    return history


def display_results(history, test_loss, test_accuracy):
    plt.figure(figsize=(16, 8))
    plt.subplot(1, 2, 1)
    plot_graphs(history, 'accuracy')
    plt.ylim(None, 1)
    plt.subplot(1, 2, 2)
    plot_graphs(history, 'loss')
    plt.ylim(0, None)

    date = datetime.today().strftime('%Y-%m-%d')
    plt.savefig('log/fig_{}.png'.format(date), bbox_inches='tight')

def compare_models(new_loss, new_accuracy, old_loss, old_accuracy):
    log_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    results = { "timestamp": log_time,
                "winner": "old",
                "new": {"loss": new_loss, "accuracy": new_accuracy},
                "old": {"loss": old_loss, "accuracy": old_accuracy}}
    if (new_accuracy / new_loss) > (old_accuracy / new_loss):
        results["winner"] = "new"
    return results

# WRITE RETRAIN EVENT TO LOGGER
def write_to_log(results):
    if exists(log_path):
        # APPEND RESULTS TO LOGGER
        with open(log_path, 'r+') as fl:
            logs = json.load(fl)
            logs["logs"].append(results)
            file.seek(0)
            json.dump(logs, fl)
    else:
        # CREATE NEW LOG FILE
        with open(log_path, 'r+') as fl:
            logger = {"logs": [results]}
            json.dump(logger, fl)


# if __name__ == "__main__":
def main():
    # LOAD THE DATASET
    train_ds, valid_ds, test_ds = load_dataset(ds_path)
    # LOAD THE SAVED MODEL FOR RETRAINING
    model = load_model(model_path)
    # TRAIN THE MODEL
    history = train_model(train_ds, valid_ds, model)
    # GET MODEL PERFORMANCE
    new_loss, new_accuracy = model.evaluate(test_ds)
    display_results(history, new_loss, new_accuracy)
    # RELOAD THE OLD MODEL FOR COMPARISON
    old_model = load_model(model_path)
    old_loss, old_accuracy = old_model.evaluate(test_ds)
    # COMPARE MODELS AND RETURN WINNER, MEASURED SIMPLY BY ACCURACY
    results = compare_models(new_loss, new_accuracy, old_loss, old_accuracy)
    write_to_log(results)
    if results["winner"] == "new":
        # REPLACE OLD MODEL WITH NEW MODEL
        date = datetime.today().strftime('%Y-%m-%d_%H:%M:%S')
        os.rename(model_path, "models/archive/retired_{}.tf".format(date))
        model.save(model_path, save_format='tf')
        return 1
    return 0
