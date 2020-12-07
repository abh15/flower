#!/usr/bin/python3

from typing import Dict, Tuple, cast
from threading import Thread
import subprocess
import numpy as np
import tensorflow as tf

import flwr as fl

from flask import Flask, request

app = Flask(__name__) 

#starts flwr client using received arguments
@app.route('/start', methods=['GET', 'POST'])
def start():
    def configureClient( source : str, model : str, sink : str, server: str) -> None:
        """ Configures and start a client instance """ 

        print("Source is " + source + "\n")
        print("Model is " + model + "\n")
        print("Sink is" + sink + "\n")

        # Build and compile Keras model
        model = tf.keras.models.Sequential(
            [
                tf.keras.layers.Flatten(input_shape=(28, 28)),
                tf.keras.layers.Dense(128, activation="relu"),
                tf.keras.layers.Dropout(0.2),
                tf.keras.layers.Dense(10, activation="softmax"),
            ]
        )
        model.compile(
            optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"]
        )

        # Implement a Flower client
        class MnistClient(fl.client.keras_client.KerasClient):
            def __init__(
                self,
                model: tf.keras.Model,
                x_train: np.ndarray,
                y_train: np.ndarray,
                x_test: np.ndarray,
                y_test: np.ndarray,
            ) -> None:
                self.model = model
                self.x_train, self.y_train = x_train, y_train
                self.x_test, self.y_test = x_test, y_test

            def get_weights(self) -> fl.common.Weights:
                return cast(fl.common.Weights, self.model.get_weights())

            def fit(
                self, weights: fl.common.Weights, config: Dict[str, str]
            ) -> Tuple[fl.common.Weights, int, int]:
                self.model.set_weights(weights)
                self.model.fit(self.x_train, self.y_train, epochs=5)
                return self.model.get_weights(), len(self.x_train), len(self.x_train)

            def evaluate(
                self, weights: fl.common.Weights, config: Dict[str, str]
            ) -> Tuple[int, float, float]:
                self.model.set_weights(weights)
                loss, accuracy = self.model.evaluate(self.x_test, self.y_test)
                return len(self.x_test), loss, accuracy

        # Load MNIST data
        (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
        x_train, x_test = x_train / 255.0, x_test / 255.0

        client= MnistClient(model, x_train, y_train, x_test, y_test)

        fl.client.start_keras_client(server_address=server, client=client)

    numClients = int(request.form.get('num'))
    src= request.form.get('source')
    model= request.form.get('model')
    sink= request.form.get('sink')
    serv= request.form.get('server')   
    prefix = "python3 -m flwr_example.factory.client"
    for client in range(numClients):
        process = subprocess.Popen(prefix+" --server="+serv+" --source="+src+" --model="+model+" --sink="+sink, shell=True)
    return 'ok', 200 

#starts flwr server using received arguments
@app.route('/launch', methods=['GET', 'POST'])
def launch():
    def configureServer(maxNumClients : int) -> None:
        client_manager = fl.server.SimpleClientManager()
        strategy = fl.server.strategy.FedAvg(min_fit_clients = maxNumClients, min_available_clients = maxNumClients)
        server = fl.server.Server(client_manager=client_manager, strategy=strategy)
        # Run server
        fl.server.start_server(
            "localhost:6000",
            server,
            config={"num_rounds": 2},
        )

    thread = Thread(target=configureServer, kwargs={'maxNumClients': int(request.form.get('maxcli'))})
    thread.start()
    return 'ok', 200

    
if __name__=='__main__':
    app.run(host='0.0.0.0')