#!/usr/bin/env python3

import os, threading, logging, glob, json
from os.path import exists

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from flask import Flask, request, jsonify, send_file, abort
from flask_cors import CORS, cross_origin
import requests

from tf_model_manager import TF_Manager
from dataset_manager import DS_Manager

# PATH TO TF MODEL
model_path = "models/sentiment_classifier.tf"
tf = TF_Manager(model_path)

# HOLDS DATA THAT HAS NOT BEEN USED YET FOR TRAINING
live_ds_path = "datasets/live_dataset.csv"
# HOLDS DATA ALREADY USED IN TRAINING
archive_ds_path = "datasets/archive_dataset.csv"
# HOLDS DATA DURING RETRAINING
tmp_ds_path = "datasets/tmp_dataset.csv"
ds = DS_Manager(live_ds_path, archive_ds_path, tmp_ds_path)

log_path = "logs/logging.json"
stats_path = "logs/stats.json"
monitor_graph_path = "logs/graphs/"


# TRIGGER RETRAINING SEQUENCE
def retrain():
    ds.transfer_to_tmp()
    tf.retrain_model()

# GET PATH FOR LATEST GRAPH IMAGE
def get_latest_graph():
    folder_path = monitor_graph_path
    file_type = r'*png'
    files = glob.glob(folder_path + file_type)
    max_file = max(files, key=os.path.getctime)
    return max_file

# HANDLE ALL POST REQUESTS
def post_handler(data):
    # If making a sentiment prediction on text
    if data["action"] == "predict":
        # BLOCK IF LOADING NEW MODEL
        if tf.model_timeout():
            abort(404)
        # ELSE RUN PREDICTION
        else:
            response = {"prediction": None, "text": data['text']}
            prediction = tf.predict_sentiment(data["text"])
            response["prediction"] = prediction
            return jsonify(**response)
    # If saving a new prediction record
    if data["action"] == "save_record":
        try:
            # Save the record to the database
            while ds.live_lock:
                pass
            ds.live_lock = True
            predict_val = 0
            if data["prediction"] == "positive":
                predict_val += 1
            ds_record = "\"{}\"; {}\n".format(data["text"], str(predict_val))
            trig_retrain = ds.record_entry(ds_record)
            ds.live_lock = False
            #
            if trig_retrain:
                if not tf.retrain_lock:
                    retrain_thread = threading.Thread(target=retrain)
                    retrain_thread.start()
            return jsonify({"status": "Success"})
        # If save record should fail for any reason
        except Exception as e:
            logging.error(e)
            return jsonify({"status": "Failure"})
    abort(404)

# HANDLE ALL GET REQUESTS
def get_handler(target):
    logging.info("Get target: {}".format(target))
    # If requesting monitor data return log
    if target == "monitor_data":
        if exists(log_path):
            with open(log_path, 'r') as fl:
                logs = json.load(fl)
                return jsonify(logs)
        else:
            empty_log = {"logs": []}
            return jsonify(empty_log)
    # If requesting monitor graph
    if target == "monitor_graph":
        g_path = get_latest_graph()
        if exists(g_path):
            return send_file(g_path, mimetype='image/png')
    abort(404)

# Handle requests sent to Flask server
def api_hook():
    # Handle a POST Request
    if request.method == 'POST':
        # Get data as dictionar
        data = request.get_json()
        logging.info("Received request: {}, {}".format(request.method, data))
        return post_handler(data)
    # Handle a GET Request
    elif request.method == 'GET':
        target = request.args.get("target")
        return get_handler(target)
    abort(404)


class MyFlask(Flask):
    def run(self, host=None, port=None, debug=None, load_dotenv=True, **options):
        if not self.debug or os.getenv('WERKZEUG_RUN_MAIN') == 'true':
            with self.app_context():
                logging.basicConfig(
                    format='%(asctime)s-TF_Model_Server{%(levelname)s}: %(message)s',
                    level=logging.INFO,
                    datefmt='%H:%M:%S')
                logging.info("TF Model Server Online!")
        super(MyFlask, self).run(host=host, port=port, debug=debug, load_dotenv=load_dotenv, **options)

if __name__=="__main__":
    app = MyFlask(__name__)
    app.add_url_rule('/api/', view_func=api_hook, methods=['POST', 'GET'])
    CORS(app)
    app.run()
