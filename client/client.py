import asyncio
import os

import dill
import websockets

import client.trading_actions
import client.trading_bot

hostname = os.environ.get(
    "EXCHANGE_SERVER_HOSTNAME", "challenge1.edutrading.dev"
)
username = os.environ.get("EXCHANGE_USERNAME", "user")


def get_websocket_url():
    return f"wss://{hostname}"


async def send_trading_bot():
    async with websockets.connect(get_websocket_url()) as websocket:
        # serialize the trading bot
        trading_modules = [client.trading_bot, client.trading_actions]
        msg = dill.dumps(trading_modules)

        # send bot over the wire
        await websocket.send(msg)

        # await and deserialize response
        response = await websocket.recv()
        payout = round(dill.loads(response), 2)

        print("Payout for simulation: ${:0.2f}".format(payout))


if __name__ == "__main__":
    asyncio.run(send_trading_bot())
