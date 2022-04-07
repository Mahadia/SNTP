# SNTP

## SNTP Angular Frontend

This is the frontend of the application. In order to run the frontend first run the command `npm install` to install the project dependecies. Then launch with `npm start`.

## TF Model Flask

This is a reimplementation of the 'TF Inference Server', using the Flask backend micro-framework. Launch 'tf\_model\_flask/tf\_model\_server.py' to start the Flask server. This provides a RESTful API for running predictions on the AI Model, Adding new records to the dataset and retrieving monitor information. After 1000 new labeled text samples have been added to the dataset the AI retraining process will trigger automatically. The newly trained model will be compared with the old model. If the new model is better the old model will be archived and the new model will go live.

![](tf_model_flask/assets/tf_flask_server_schema.png)

### Included Files - DIR: tf\_model\_flask
1. tf\_model\_server.py - This is the main function of the backend, it also serves as the entry point for the frontend. The backend server is started by running this fie. This program also manages the logging functions provided by the backend.
2. dataset\_manager.py - This module, as the name suggests, manages the dataset. It writes new comments to a "live" dataset, which when full, is transfered to a temporary training database, and is then finally archived in the primary dataset if retraining is completed successfully. If retraining fails the dataset manager maintains data in the "live" dataset until a successful retraining is completed (note: success, refers to the operation not the performance of the retrained model).
3. tf\_model\_manager.py - This module manages the active AI model and handles model retraining and validation. Incoming comments are sent to this module for sentiment prediction operations. When retraining the manager is responsible for starting the process, evaluating the results of retraining, selecting the best performing model and reloading the best performing model into active memory.
4. tf\_model\_retrain.py - This module contains the actual algorithm used to retrain the AI model. It simply runs the algorithm and returns the results to the tf\_model\_manager.
5. DIR: datasets
  1. live\_dataset.csv - The active "live" dataset, used to store new text entries while waiting for the next retraining.
  2. tmp\_dataset.csv - This is a temporary dataset only used for retraining operations, depending on the result at the conclusion of a retraining process, the data is either transferred to archive\_dataset.csv or live\_dataset.csv.
  3. archive\_dataset.csv - This contains the full dataset used to train the current active AI model. It is intended as the final permanent storage location for our dataset.
  4. sentiment\_dataset.csv - This is the original starting dataset used to train the first AI model used.
6. DIR: logs
  1. logging.json - This file contains all log data.
  2. init\_log.py - This is a small script used to generate a new loggin.json file in the event one is not found by the backend server on startup.
  3. DIR: graphs - Contains images of the training analysis graphs generated during AI model retraining. These can be viewed by the system admin on the frontend.
7. DIR: models
  1. sentiment\_classifier.tf - The current active AI model running on the backend.
  2. DIR: archive - Contains all the old AI models previously used by our application.
8. DIR: assets - Contains image content for README documentation. 

### REST API

#### 1. Make Prediction
- POST:		{action: "predict", text: "I'm lovin it"}
- RESPONSE:	{prediction: "positive", text: "I'm lovin it"}

#### 2. Record Data to Dataset
- POST:		{action: "record", prediction: "positive", text: "I'm lovin it"}
- RESPONSE:	{status: "success"}

#### 3. Retrieve Monitor Data
- GET:		{params: {target: "monitor_data"}}
- RESPONSE:	{logs: [ { timestamp: "2022-03-11 12:28:23", winner: "new", old: {loss: 0.32, accuracy: 0.87}, new: {loss: 0.29, accuracy: 0.89} }, ...] }

#### 4. Retrieve Most Recent Training Graph
- GET:		{params: {target: "monitor_graph"}}
- RESPONSE:	< PNG IMAGE >

## TF Model Trainer

This contains the cleaned dataset and training algorithm for the TF Sentiment Classifier Model.
