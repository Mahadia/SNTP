#!/usr/bin/env python3

import os, sys, logging
from datetime import datetime
import numpy as np
from tensorflow import keras
import tensorflow as tf
import socket, select, queue
from _thread import *

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

model_path = "sentiment_classifier.tf"
model = None

host = '127.0.0.1'
modl_port = 9909
ctrl_port = 9919
inputs = []
outputs = []

infr_queues = {}
ctrl_queues = {}

def load_inference_model():
    global model
    test_text = "I'm loving it!"
    logging.info("Loading Tensorflow inference model...")
    try:
        model = tf.keras.models.load_model(model_path)
        logging.info("Loaded model: {}".format(model_path))
        logging.debug("Running test inference: \"{}\"".format(test_text))
        prediction = predict_sentiment(test_text, model)
        logging.debug("Test result: {}".format(prediction))
    except OSError:
        logging.error("Error: Cannot locate tensorflow model.")
        logging.error("Check path: {}".format(model_path))
        sys.exit(1)


def create_server_sockets(modl_port, ctrl_port):
    logging.info("Binding server sockets...")
    # Create Sockets
    modl_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ctrl_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    modl_socket.setblocking(0)
    ctrl_socket.setblocking(0)
    try:
        # Bind the sockets
        modl_socket.bind((host, modl_port))
        ctrl_socket.bind((host, ctrl_port))
        # Set to Listen
        modl_socket.listen(5)
        ctrl_socket.listen(5)
        inputs.append(modl_socket)
        inputs.append(ctrl_socket)
        logging.info("Serving TF Model at: {}:{}".format(host, modl_port))
        logging.info("Serving Control at: {}:{}".format(host, ctrl_port))
        return modl_socket, ctrl_socket
    except socket.error as e:
        print(str(e))
        sys.exit(1)

def predict_sentiment(text, model):
    prediction = model.predict(np.array([(text)]))
    p_val = prediction[0]
    logging.debug("Input text: {}".format(text))
    logging.debug("Inference: {}".format(p_val))
    if p_val < 0:
        return "negative"
    else:
        return "positive"

def server_start(modl_socket, ctrl_socket):
    while inputs:
        readable, writable, exceptional = select.select(
            inputs, outputs, inputs)
        for s in readable:
            readable_handler(s, modl_socket, ctrl_socket)

        for s in writable:
            writable_handler(s)

        # Handles exceptions in sockets
        for s in exceptional:
            exception_handler(s)

def readable_handler(s, modl_socket, ctrl_socket):
    if s is modl_socket:
        connection, client_address = s.accept()
        connection.setblocking(0)
        inputs.append(connection)
        infr_queues[connection] = queue.Queue()
    elif s is ctrl_socket:
        connection, client_address = s.accept()
        connection.setblocking(0)
        inputs.append(connection)
        ctrl_queues[connection] = queue.Queue()
    else:
        target = s.getsockname()[1]
        data = s.recv(1024)
        logging.debug("Data rcvd: {}".format(data))
        if data:
            if target == modl_port:
                infr_queues[s].put(data)
            if target == ctrl_port:
                ctrl_queues[s].put(data)
            if s not in outputs:
                outputs.append(s)
        else:
            exception_handler(s)

def writable_handler(s):
    target = s.getsockname()[1]
    peer = s.getpeername()
    if target == modl_port:
        try:
            next_msg = infr_queues[s].get_nowait()
            logging.info("Message rcvd {}: \'{}\'".format(peer, next_msg.decode('UTF-8')))
            prediction = predict_sentiment(next_msg.decode('UTF-8'), model)
            logging.info("Prediction result: {}".format(prediction))
        except queue.Empty:
            outputs.remove(s)
        else:
            s.send(prediction.encode())
    elif target == ctrl_port:
        try:
            next_msg = ctrl_queues[s].get_nowait()
            logging.info("Control rcvd: {}".format(next_msg.decode('UTF-8')))
        except queue.Empty:
            outputs.remove(s)
        else:
            logging.info("Control message {}: {}".format(peer, str(next_msg)))
            if next_msg == b"shutdown":
                s.send(b"Shutting down server...")
                logging.warning("Shutting down server...")
                shutdown_server()
            elif next_msg == b"reloadTF":
                s.send(b"Reloading TF inference model...")
                logging.warning("Reloading TF inference model...")
                load_inference_model()
                exception_handler(s)
            else:
                logging.warning(
                    "Invalid control command received.".format(peer))
                s.send(b"Error: Invalid command")

def exception_handler(s):
    target = s.getsockname()[1]
    inputs.remove(s)
    if s in outputs:
        outputs.remove(s)
    s.close()
    if target == modl_port:
        del infr_queues[s]
    if target == ctrl_port:
        del ctrl_queues[s]


def shutdown_server():
    for s in inputs:
        logging.info("Closing: {}".format(s.getsockname()))
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()
    logging.info("TF Model Server Shutdown.")
    sys.exit(0)

if __name__ == "__main__":
    # SETUP LOGGING
    logging.basicConfig(
        format='%(asctime)s-TF_Model_Server{%(levelname)s}: %(message)s',
        level=logging.INFO,
        datefmt='%H:%M:%S')
    load_inference_model()
    modl_socket, ctrl_socket = create_server_sockets(modl_port, ctrl_port)
    logging.info("TF Model Server Online!")
    server_start(modl_socket, ctrl_socket)
