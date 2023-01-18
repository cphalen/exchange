from datetime import datetime
from enum import Enum
from functools import total_ordering
from queue import PriorityQueue
from symbol.symbol import Symbol


class Direction(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


@total_ordering
class Order:
    """
    PennETC supports only one kind of order: limit orders. No market orders
    here. Limit orders have two attributes:
        - Direction: either `Direction.BUY` or `Direction.SELL`, this indicates
                     whether you are looking to buy a product or looking to
                     sell a product.
        - Amount: this is an `float` representing the highest amount for which
                  you would be willing to buy, or the lowest amount for which
                  you would be willing to sell.
    """

    order_id_counter = 1

    def mint_order_id() -> int:
        order_id = Order.order_id_counter
        Order.order_id_counter += 1
        return order_id

    def __init__(self, user: str, direction: Direction, amount: float) -> None:
        self.order_id = Order.mint_order_id()
        self.user = user
        self.direction = direction
        self.amount = amount
        self.timestamp = datetime.now()

    def signed_amount(self):
        match self.direction:
            case Direction.BUY:
                return (-1) * self.amount
            case Direction.SELL:
                return self.amount

    def __eq__(self, other) -> bool:
        if self.direction != other.direction:
            raise ValueError("Cannot compare a BUY order with a SELL order")
        else:
            return (
                self.signed_amount() == other.signed_amount()
                and self.timestamp == other.timestamp
            )

    def __lt__(self, other) -> bool:
        if self.direction != other.direction:
            raise ValueError("Cannot compare a BUY order with a SELL order")
        elif self.signed_amount() == other.signed_amount():
            return self.timestamp < other.timestamp
        else:
            return self.signed_amount() < other.signed_amount()

    def __str__(self, other):
        return (
            f"<Order direction={self.direction}, amount={self.amount},"
            f" timestamp={self.timestamp}>"
        )


class OrderBook:
    def __init__(self, symbol: Symbol):
        self.symbol = symbol
        self.bids = PriorityQueue()
        self.asks = PriorityQueue()
        self.balances = {}

    def add_order(self, order):
        match order.direction:
            case Direction.BUY:
                self.bids.put(order)
            case Direction.SELL:
                self.asks.put(order)

    def get_payout(self, user: str):
        return self.balances.get(user, 0)

    def resolve_orders(self):
        orders_filled = []
        while not self.bids.empty() and not self.asks.empty():
            highest_bid = self.bids.get()
            lowest_ask = self.asks.get()

            if highest_bid.amount >= lowest_ask.amount:
                # bidding user gains profit of symbol value minus buy amount
                self.balances[highest_bid.user] = (
                    self.balances.get(highest_bid.user, 0)
                    + self.symbol.true_value()
                    - highest_bid.amount
                )
                # asking user gains profit of sell amount minus symbol value
                self.balances[lowest_ask.user] = (
                    self.balances.get(lowest_ask.user, 0)
                    + lowest_ask.amount
                    - self.symbol.true_value()
                )

                orders_filled.append({"buy": highest_bid, "sell": lowest_ask})
            else:
                self.bids.put(highest_bid)
                self.asks.put(lowest_ask)
                break
        return orders_filled

    def num_bids(self):
        return self.bids.qsize()

    def num_asks(self):
        return self.asks.qsize()

    def copy_bids_and_asks(self):
        bids_list = []
        asks_list = []

        while not self.bids.empty():
            bids_list.append(self.bids.get())

        while not self.asks.empty():
            asks_list.append(self.asks.get())

        # create copies
        bids = PriorityQueue()
        asks = PriorityQueue()

        # repopulate copies and originals
        for bid in bids_list:
            bids.put(bid)
            self.bids.put(bid)

        for ask in asks_list:
            asks.put(ask)
            self.asks.put(ask)

        return bids, asks

    def __str__(self):
        def fill_line(line: str, filler: str = " "):
            leftover = width - len(line)
            return line + (filler * leftover)

        width = 20
        bids, asks = self.copy_bids_and_asks()
        res = (
            f"{self.symbol} Order Book\n"
            + fill_line("", filler="-")
            + "|"
            + fill_line("", filler="-")
            + "\n"
        )

        res += (
            fill_line(str(Direction.BUY))
            + "|"
            + fill_line(str(Direction.SELL))
            + "\n"
        )
        res += (
            fill_line("", filler="-") + "|" + fill_line("", filler="-") + "\n"
        )

        while not bids.empty() or not asks.empty():
            if not bids.empty():
                bid_string = fill_line(str(bids.get().amount))
            else:
                bid_string = fill_line("")

            if not asks.empty():
                ask_string = fill_line(str(asks.get().amount))
            else:
                ask_string = fill_line("")

            res += bid_string + "|" + ask_string + "\n"

        return res
