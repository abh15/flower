#!/usr/bin/python3

import argparse

import flwr as fl

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flower")
    parser.add_argument(
        "--server_address",
        type=str,
        default="localhost:6000",
        help=f"gRPC server address (default: localhost:6000)",
    )
    args = parser.parse_args()
    fl.server.start_server(config={"num_rounds": 3}, server_address=args.server_address)
