import argparse
import asyncio
import getpass

from orderbook import Order

from client import send_order

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Send orders to the exchange from the command line"
    )

    # required_named = parser.add_argument_group('required named arguments')

    parser.add_argument(
        "-d",
        "--direction",
        type=str,
        help="Direction or order (BUY/SELL)",
        required=True,
    )
    parser.add_argument(
        "-a",
        "--amount",
        type=float,
        help="Price for which you are willing to BUY or SELL",
        required=True,
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
