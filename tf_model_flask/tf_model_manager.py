#!/usr/bin/env python3

"""
    TF Model Manager
    Module containing a TF_Manager class for managing TF Model Operations

    Created by: Andrew O'Shei
    Date: 12/03/2022
"""

import time, logging
from tensorflow import keras
import tensorflow as tf
import numpy as np

import tf_model_retrain as tf_retrain

class TF_Manager:
    def __init__(self, model_path):
        logging.basicConfig(
            format='%(asctime)s-TF_Model_Server{%(levelname)s}: %(message)s',
            level=logging.INFO,
            datefmt='%H:%M:%S')
        self.model_path = model_path
        self.model = None
        self.model_online = False
        self.retrain_lock = False
        self.load_inference_model()

    def load_inference_model(self):
        test_text = "I'm loving it!"
        logging.info("Loading Tensorflow inference model...")
        try:
            self.model = tf.keras.models.load_model(self.model_path)
            logging.info("Loaded model: {}".format(self.model_path))
            logging.debug("Running test inference: \"{}\"".format(test_text))
            prediction = self.predict_sentiment(test_text)
            logging.debug("Test result: {}".format(prediction))
            self.model_online = True
            logging.info("Model Online: {}".format(self.model_path))
        except OSError:
            logging.error("Error: Cannot locate tensorflow model.")
            logging.error("Check path: {}".format(self.model_path))
            sys.exit(1)

    def predict_sentiment(self, text):
        prediction = self.model.predict(np.array([(text)]))
        p_val = prediction[0]
        logging.debug("Input text: {}".format(text))
        logging.debug("Inference: {}".format(p_val))
        if p_val < 0:
            return "negative"
        else:
            return "positive"

    def model_retrainer(self):
        self.retrain_lock = True
        logging.info("Starting model retrain...")
        if tf_retrain.main():
                logging.info("TF Model retrain complete!")
                self.model_online = False
                logging.info("TF Model Offline.")
                self.load_inference_model()
        else:
            logging.info("TF Model retrain failed.")
        self.retrain_lock = False

    def model_timeout(self):
        timeout = 0
        while not self.model_online:
            time.sleep(1)
            timeout += 1
            if timeout > 5:
                return 1
        return 0
