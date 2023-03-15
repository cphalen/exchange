import asyncio
import os
import pickle

import websockets

from client.trading_actions import TradingActions
from client.trading_bot import TradingBot

hostname = os.environ.get(
    "EXCHANGE_SERVER_HOSTNAME", "challenge1.edutrading.dev"
)
username = os.environ.get("EXCHANGE_USERNAME", "user")


def get_websocket_url():
    return f"wss://{hostname}"


async def send_trading_bot():
    async with websockets.connect(get_websocket_url()) as websocket:
        # serialize the trading bot
        msg = pickle.dumps(TradingBot(TradingActions()))

        # send bot over the wire
        await websocket.send(msg)

        # await and deserialize response
        response = await websocket.recv()
        payout = round(pickle.loads(response), 2)

        print("Payout for simulation: ${:0.2f}".format(payout))


if __name__ == "__main__":
    asyncio.run(send_trading_bot())
