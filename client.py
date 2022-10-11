import os

import websockets

from orderbook import Order, OrderBookMessage

hostname = os.environ.get("EXCHANGE_SERVER_HOSTNAME", "localhost")
port = os.environ.get("EXCHANGE_SERVER_PORT", 8765)


def get_websocket_url():
    return f"ws://{hostname}:{port}"


async def send_order(order):
    async with websockets.connect(get_websocket_url()) as websocket:
        # send order
        await websocket.send(Order.serialize(order))
        # await response
        return OrderBookMessage.deserialize(await websocket.recv())
