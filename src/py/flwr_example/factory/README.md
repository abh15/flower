### Run client

`python3 -m flwr_example.factory.client --server=localhost:8080 --source=MNIST --model=keras --sink=robot.controller`

`docker run -it flower python3 -m flwr_example.factory.client --server=localhost:8080 --source=MNIST --model=keras --sink=robot.controller`

### Run server

`python3 -m flwr_example.factory.server --server_address=localhost:8080`

`docker run -it flower python3 -m flwr_example.factory.server --server_address=localhost:8080 `


