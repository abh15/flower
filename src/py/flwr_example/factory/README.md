### Run client

`python3 -m flwr_example.factory.flask_factory_client`

`docker run --publish 5000:5000 -it flower:latest bash`

### Run server

`python3 -m flwr_example.factory.server --server_address=localhost:8080`

`docker run -it flower python3 -m flwr_example.factory.server --server_address=localhost:8080 `


