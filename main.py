from enum import Enum
import pickle
from copy import copy
from queue import PriorityQueue
from datetime import datetime
from functools import total_ordering

class Symbol(str, Enum):
    BOND = "BOND"
    ETF = "ETF"


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

    def __init__(self, user: str, direction: Direction, amount: float) -> None:
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

    @staticmethod
    def serialize(order):
        return pickle.dumps(order)

    @staticmethod
    def deserialize(message):
        return pickle.loads(message)

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
        return f"<Order direction={self.direction}, amount={self.amount}, timestamp={self.timestamp}>"


class OrderBookMessage:
    def __init__(self, ack, fill, error):
        self.ack = ack
        self.error = error
        self.fill = fill

    @staticmethod
    def ack():
        return OrderBookMessage(True, None, None)

    @staticmethod
    def fill(fill):
        return OrderBookMessage(None, fill, None)

    @staticmethod
    def error(error):
        return OrderBookMessage(None, None, error)

    @staticmethod
    def serialize(order_response):
        return pickle.dumps(order_response)

    @staticmethod
    def deserialize(message):
        return pickle.loads(message)

    def __str__(self, other):
        return f"<OrderBookResponse ack={self.ack}, fill={self.fill}, error={self.error}>"

class OrderBook:
    def __init__(self, symbol: Symbol):
        self.symbol = symbol
        self.bids = PriorityQueue()
        self.asks = PriorityQueue()

    def add_order(self, order):
        match order.direction:
            case Direction.BUY:
                self.bids.put(order)
            case Direction.SELL:
                self.asks.put(order)

    def resolve_orders(self):
        orders_filled = []
        while not self.bids.empty() and not self.asks.empty():
            highest_bid = self.bids.get()
            lowest_ask = self.asks.get()

            if highest_bid.amount >= lowest_ask.amount:
                orders_filled.append(highest_bid)
                orders_filled.append(lowest_ask)
            else:
                self.bids.put(highest_bid)
                self.asks.put(lowest_ask)
                break
        return orders_filled

    def num_bids(self):
        return self.bids.size()

    def num_asks(self):
        return self.asks.size()


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
        res = f"{self.symbol} Order Book\n" + fill_line("", filler="-") + "|" + fill_line("", filler="-") + "\n"

        res += (
            fill_line(str(Direction.BUY)) + "|" + fill_line(str(Direction.SELL)) + "\n"
        )
        res += fill_line("", filler="-") + "|" + fill_line("", filler="-") + "\n"

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
