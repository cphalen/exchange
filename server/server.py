import asyncio
import os
import pickle
from symbol.symbol import symbol_of_string

import websockets

from server.orderbook import Direction, Order, OrderBook
from server.simulator import Simulator

hostname = os.environ.get("EXCHANGE_SERVER_HOSTNAME", "127.0.0.1")
port = os.environ.get("EXCHANGE_SERVER_PORT", 8765)
symbol = symbol_of_string(os.environ.get("EXCHANGE_SERVER_SYMBOL", "BOND"))
debug = os.environ.get("EXCHANGE_SERVER_DEBUG", True)

username = "user"

async def handle_request(websocket):
    async for msg in websocket:
        # create orderbook and override functions
        ob = OrderBook(symbol=symbol)

        def add_buy(amount: int) -> int:
            order = Order(username, Direction.BUY, amount)
            ob.add_order(order)
            return order.order_id

        def add_sell(amount: int) -> int:
            order = Order(username, Direction.SELL, amount)
            ob.add_order(order)

       # unpackage payload and overwrite dummy methods
        payload = pickle.loads(msg)
        bot = payload["bot"]
        actions = payload["actions"]
        actions.add_buy = add_buy
        actions.add_sell = add_sell

        # create and run simulator
        sim = Simulator(username, bot, ob)
        payout = sim.run()

        # serialize and send response
        response = pickle.dumps(payout)
        await websocket.send(response)


async def listen():
    print(f"Running exchange server on {hostname}:{port}")
    async with websockets.serve(handle_request, hostname, port):
        await asyncio.Future()


asyncio.run(listen())
