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
@app.route('/startcli', methods=['GET', 'POST'])
def startcli():
    numClients = int(request.form.get('num'))
    src= request.form.get('source')
    model= request.form.get('model')
    sink= request.form.get('sink')
    serv= request.form.get('server')   
    prefix = "python3 -m flwr_example.factory.client"
    for client in range(numClients):
        process = subprocess.Popen(prefix+" --server="+serv+" --source="+src+" --model="+model+" --sink="+sink, shell=True)
    return 'ok', 200 

# #starts flwr server using received arguments
# @app.route('/launchserv', methods=['GET', 'POST'])
# def launchserv():
#     def configureServer(maxNumClients : int) -> None:
#         client_manager = fl.server.SimpleClientManager()
#         strategy = fl.server.strategy.FedAvg(min_fit_clients = maxNumClients, min_available_clients = maxNumClients)
#         server = fl.server.Server(client_manager=client_manager, strategy=strategy)
#         # Run server
#         fl.server.start_server(
#             "0.0.0.0:6000",
#             server,
#             config={"num_rounds": 2},
#         )

#     thread = Thread(target=configureServer, kwargs={'maxNumClients': int(request.form.get('maxcli'))})
#     thread.start()
#     return 'ok', 200

    
if __name__=='__main__':
    app.run(host='0.0.0.0')