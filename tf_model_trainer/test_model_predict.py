#!/usr/bin/env python3

"""
	This program accepts a "string" as an argument
	It then loads a tensorflow model and runs an inference
"""

import os
import sys

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
from tensorflow import keras

import numpy as np


def get_args():
	try:
		if isinstance(sys.argv[1], str):
			return sys.argv[1]
	except IndexError:
		pass
	print("Error: Program requires a string argument")
	print('Usage: python3 test_model_predict.py "Hello world"')
	sys.exit(1)


def predict_sentiment(comment):
	print("TensorFlow Version {}".format(tf.version.VERSION))

	print("Loading AI Model...")
	model = tf.keras.models.load_model('sentiment_classifier.tf')

	predictions = model.predict(np.array([(comment)]))
	val = predictions[0]

	print('Input String: "' + comment + '"')

	print("Prediction Value: {:.6f}".format(val[0]))

	if val < 0:
		print("Predicted Sentiment: negative.")
	else:
		print("Predicted Sentiment: positive")
	sys.exit(0)

if __name__=="__main__":
	comment = get_args()
	predict_sentiment(comment)
