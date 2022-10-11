import argparse
import asyncio
import getpass

from client import send_order
from orderbook import Order

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Send orders to the exchange from the command line"
    )

    parser.add_argument("--direction", type=str, help="Direction or order (BUY/SELL)")
    parser.add_argument(
        "--amount",
        type=float,
        help="Price for which you are willing to BUY or SELL",
    )

    args = parser.parse_args()

    asyncio.run(
        send_order(
            Order(
                user=getpass.getuser(),
                direction=args.direction,
                amount=args.amount,
            )
        )
    )
