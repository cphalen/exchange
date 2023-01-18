import os
import websockets
import asyncio
import pickle
from client.trading_actions import TradingActions
from client.trading_bot import TradingBot

hostname = os.environ.get("EXCHANGE_SERVER_HOSTNAME", "localhost")
port = os.environ.get("EXCHANGE_SERVER_PORT", 8765)
username = os.environ.get("EXCHANGE_USERNAME", "user")


def get_websocket_url():
    return f"ws://{hostname}:{port}"


async def send_trading_bot():
    async with websockets.connect(get_websocket_url()) as websocket:
        # send order
        payload = { "bot": TradingBot, "actions": TradingActions }
        msg = pickle.dumps(payload)
        await websocket.send(msg)
        # await response
        return await websocket.recv()

if __name__ == "__main__":
    asyncio.run(send_trading_bot())
