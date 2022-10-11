import asyncio
import os

import websockets

from orderbook import Order, OrderBook, OrderBookMessage, Symbol

hostname = os.environ.get("EXCHANGE_SERVER_HOSTNAME", "localhost")
port = os.environ.get("EXCHANGE_SERVER_PORT", 8765)
symbol = os.environ.get("EXCHANGE_SERVER_SYMBOL", Symbol.BOND)
debug = os.environ.get("EXCHANGE_SERVER_DEBUG", True)


async def marshal_order(websocket):
    async for message in websocket:
        # add order to order book and send response
        ob.add_order(Order.deserialize(message))
        await websocket.send(OrderBookMessage.serialize(OrderBookMessage.ack()))

        # try resolving the book
        fills = ob.resolve_orders()
        for fill in fills:
            await websocket.send(
                OrderBookMessage.serialize(OrderBookMessage.fill(fill))
            )

        # if debug print order book
        if debug:
            print(ob)


async def listen():
    print(f"Running exchange server on {hostname}:{port}")
    async with websockets.serve(marshal_order, hostname, port):
        await asyncio.Future()


ob = OrderBook(symbol=symbol)
asyncio.run(listen())
