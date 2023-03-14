import asyncio
import importlib
import os
import sys
from symbol.symbol import symbol_of_string

import dill
import websockets

from server.orderbook import Direction, Order, OrderBook
from server.simulator import Simulator

hostname = os.environ.get("EXCHANGE_SERVER_HOSTNAME", "127.0.0.1")
port = os.environ.get("EXCHANGE_SERVER_PORT", 8765)
symbol = symbol_of_string(os.environ.get("EXCHANGE_SERVER_SYMBOL", "BOND"))
debug = os.environ.get("EXCHANGE_SERVER_DEBUG", True)

username = "user"


def dynamic_module_load(module):
    importlib.import_module(module.__name__)


def dynamic_module_unload(module):
    del sys.modules[module.__name__]
    del module


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
            return order.order_id

        # unpackage user defined trading modules
        trading_modules = dill.loads(msg)
        [bot_module, actions_module] = trading_modules

        # dynamic load of user defined trading modules
        dynamic_module_load(bot_module)
        dynamic_module_load(actions_module)

        # override dummy add_buy and add_sell functions
        actions_module.TradingActions.add_buy = add_buy
        actions_module.TradingActions.add_sell = add_sell

        # create and run simulator
        sim = Simulator(username, bot_module.TradingBot(), ob)
        payout = sim.run()

        # serialize and send response
        response = dill.dumps(payout)
        await websocket.send(response)

        # dynamic unload of user defined trading modules
        dynamic_module_unload(bot_module)
        dynamic_module_unload(actions_module)


async def listen():
    print(f"Running exchange server on {hostname}:{port}")
    async with websockets.serve(handle_request, hostname, port):
        await asyncio.Future()


asyncio.run(listen())
