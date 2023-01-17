import asyncio
import os
from symbol.symbol import Bond

import websockets

from message.request import ExchangeRequest
from server.orderbook import Direction, Order, OrderBook

hostname = os.environ.get("EXCHANGE_SERVER_HOSTNAME", "127.0.0.1")
port = os.environ.get("EXCHANGE_SERVER_PORT", 8765)
symbol = Symbol.of_string(of_os.environ.get("EXCHANGE_SERVER_SYMBOL", "BOND"))
debug = os.environ.get("EXCHANGE_SERVER_DEBUG", True)


async def handle_request(websocket):
    async for request in websocket:
        # handle the particular kind of request
        request = ExchangeRequest.deserialize(request)
        if request.balance is not None:
            balance = ob.get_balance(request.user)
            await websocket.send(balance)
        elif request.buy is not None:
            order = Order(request.user, Direction.BUY, request.buy)
            ob.add_order(order)
            await websocket.send(None)
        elif request.sell is not None:
            order = Order(request.user, Direction.SELL, request.sell)
            ob.add_order(order)
            await websocket.send(None)

        # try resolving the book
        fills = ob.resolve_orders()
        for fill in fills:
            ExchangeResponse.fill(fill.order_id)

        # if debug print order book
        if debug:
            print(ob)


async def listen():
    print(f"Running exchange server on {hostname}:{port}")
    async with websockets.serve(handle_request, hostname, port):
        await asyncio.Future()


ob = OrderBook(symbol=symbol)
asyncio.run(listen())
