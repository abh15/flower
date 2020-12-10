#!/usr/bin/python3

import argparse

import flwr as fl

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flower")
    parser.add_argument(
        "--mincli",
        type=str,
        default="2",
        help=f"Specifies min number of clients",
    )
    args = parser.parse_args()


    client_manager = fl.server.SimpleClientManager()
    strategy = fl.server.strategy.FedAvg(min_fit_clients = args.mincli, min_available_clients = args.mincli)
    server = fl.server.Server(client_manager=client_manager, strategy=strategy)
    # Run server
    fl.server.start_server(
        "0.0.0.0:6000",
        server,
        config={"num_rounds": 2},
    )
   