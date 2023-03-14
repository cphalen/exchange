# Exchange

The exchange follows a client-server model using websockets for communication. There is some shared code in `orderbook.py` between the client and server (to keep serialization and deserialization consistent).

## Development

The code uses [poetry](https://python-poetry.org/) for package management, once installed the packages can be downloaded with
```
$ poetry install
```
and the server can be run with
```
$ poetry run python server.py
```
by default the exchange server will serve on `localhost:8765` but these can be modified with the `EXCHANGE_SERVER_HOSTNAME` and `EXCHANGE_SERVER_PORT` environment variables. The server starts in debug mode by default and will print the exchange state every time there is a new order recieved.

There is a utility script in `util/send_order.py` that sends orders to the exchange server (also using the `EXCHANGE_SERVER_HOSTNAME` and `EXCHANGE_SERVER_PORT` environment variables) which can be run with
```
$ poetry run python -m util.send_order
```
This is just meant for testing though as clients should really use the Python API defined in `client.py`.

## Test

To run test cases use command
```
poetry run pytest test
```

## Lint

The GitHub Actions on this repository run three linting commands you should run before you push to avoid failing the push:
```
$ poetry run black --line-length 79 .
$ poetry run flake8 .
$ poetry run isort .
```

## TODO

A couple ideas for next steps:
- [ ] Add unit tests which connect to a server that runs locally
- [ ] Smarter market cross logic (right now the exchange just steals the overlap of a bid and ask)
- [ ] Support multiple exchanges of different instruments (right now there is only one called `BOND`)
- [ ] Efficiency boosts across the board (I think `pickle` serialization and deserialization could be a good place to start)
- [ ] Stress testing to see how many orders per minute we can handle
- [ ] Debug issue with `deepcopy` so we can get rid of the `copy_bids_and_asks` function written for `OrderBook`
- [ ] Migrate from k8s manifests to helm charts
