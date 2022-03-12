# SNTP

## TF Model Flask

Launch 'tf\_model\_flask/tf\_model\_server.py' to start the Flask server. This provides a RESTful API for retraining the AI Model, Adding new records to the dataset and retrieving monitor information.

## TF Model Trainer

This contains the cleaned dataset and training algorithm for the TF Sentiment Classifier Model.

### TF Inference Server (Depricated)

This is a component server for the backend. Messages sent to port 9909 will be processed by the Tensorflow Inference Model and the predicted result will be returned to sender.<br />
Port 9919 is dedicated to control messages, which allow for reloading the inference model live. This allows the old tensorflow model to be updated without an interruption in service.<br />
**Note:**
The Tensorflow model was developed with Tensorflow version 2.8.0 and Python 3.8.10
