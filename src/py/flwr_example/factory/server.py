#!/usr/bin/python3

import argparse

import flwr as fl

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flower")
    parser.add_argument(
        "--mincli",
        type=int,
        default=2,
        help=f"Specifies min number of clients",
    )
    args = parser.parse_args()


    client_manager = fl.server.SimpleClientManager()
    strategy = fl.server.strategy.FedAvg(
        fraction_fit= 0.1,  # Sample 10% of available clients for the next round
        min_fit_clients= int(args.mincli/2),  # Minimum number of clients to be sampled for the next round
        min_available_clients= args.mincli,  # Minimum number of clients that need to be connected to the server before a training round can start
)
    # Run server
    fl.server.start_server(
        "0.0.0.0:6000",
        strategy=strategy,
        config={"num_rounds": 6},
    )
   