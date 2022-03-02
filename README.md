# SNTP

## TF Inference Server

This is a component server for the backend. Messages sent to port 9909 will be processed by the Tensorflow Inference Model and the predicted result will be returned to sender.<br />
Port 9919 is dedicated to control messages, which allow for reloading the inference model live. This allows the old tensorflow model to be updated without an interruption in service.<br />
**Note:**
The Tensorflow model was developed with Tensorflow version 2.8.0 and Python 3.8.10

## TF Model Trainer

This contains the cleaned dataset and training algorithm for the TF Sentiment Classifier Model.
