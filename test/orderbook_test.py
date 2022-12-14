import unittest

from orderbook import Direction, Order, OrderBook, Symbol


class OrderBookTest(unittest.TestCase):
    def setUp(self):
        self.ob = OrderBook(symbol=Symbol.BOND)
        self.user = "test_user"

    def test_no_cross(self):
        self.ob.add_order(
            Order(user=self.user, direction=Direction.BUY, amount=6)
        )
        self.ob.add_order(
            Order(user=self.user, direction=Direction.BUY, amount=8)
        )
        self.ob.add_order(
            Order(user=self.user, direction=Direction.BUY, amount=11)
        )
        self.ob.add_order(
            Order(user=self.user, direction=Direction.SELL, amount=13)
        )
        self.ob.add_order(
            Order(user=self.user, direction=Direction.SELL, amount=16)
        )
        self.ob.add_order(
            Order(user=self.user, direction=Direction.SELL, amount=17)
        )

        assert self.ob.resolve_orders() == []

    def test_cross_equal_amounts(self):
        self.ob.add_order(
            Order(user=self.user, direction=Direction.BUY, amount=6)
        )
        self.ob.add_order(
            Order(user=self.user, direction=Direction.BUY, amount=8)
        )
        self.ob.add_order(
            Order(user=self.user, direction=Direction.BUY, amount=11)
        )
        self.ob.add_order(
            Order(user=self.user, direction=Direction.SELL, amount=13)
        )
        self.ob.add_order(
            Order(user=self.user, direction=Direction.SELL, amount=16)
        )
        self.ob.add_order(
            Order(user=self.user, direction=Direction.SELL, amount=17)
        )

        assert self.ob.resolve_orders() == []

        highest_bid = Order(user=self.user, direction=Direction.BUY, amount=12)
        lowest_ask = Order(user=self.user, direction=Direction.SELL, amount=12)
        self.ob.add_order(highest_bid)
        self.ob.add_order(lowest_ask)

        assert self.ob.resolve_orders() == [highest_bid, lowest_ask]

    def test_cross_different_amounts(self):
        self.ob.add_order(
            Order(user=self.user, direction=Direction.BUY, amount=6)
        )
        self.ob.add_order(
            Order(user=self.user, direction=Direction.BUY, amount=8)
        )
        self.ob.add_order(
            Order(user=self.user, direction=Direction.SELL, amount=16)
        )
        self.ob.add_order(
            Order(user=self.user, direction=Direction.SELL, amount=17)
        )

        assert self.ob.resolve_orders() == []

        highest_bid = Order(user=self.user, direction=Direction.BUY, amount=11)
        lowest_ask = Order(user=self.user, direction=Direction.SELL, amount=10)
        self.ob.add_order(highest_bid)
        self.ob.add_order(lowest_ask)

        assert self.ob.resolve_orders() == [highest_bid, lowest_ask]

    def test_multiple_crosses(self):
        self.ob.add_order(
            Order(user=self.user, direction=Direction.BUY, amount=6)
        )
        self.ob.add_order(
            Order(user=self.user, direction=Direction.BUY, amount=8)
        )
        self.ob.add_order(
            Order(user=self.user, direction=Direction.SELL, amount=16)
        )
        self.ob.add_order(
            Order(user=self.user, direction=Direction.SELL, amount=17)
        )

        assert self.ob.resolve_orders() == []

        second_highest_bid = Order(
            user=self.user, direction=Direction.BUY, amount=11
        )
        highest_bid = Order(user=self.user, direction=Direction.BUY, amount=12)
        lowest_ask = Order(user=self.user, direction=Direction.SELL, amount=10)
        second_lowest_ask = Order(
            user=self.user, direction=Direction.SELL, amount=11
        )

        self.ob.add_order(second_highest_bid)
        self.ob.add_order(highest_bid)
        self.ob.add_order(lowest_ask)
        self.ob.add_order(second_lowest_ask)

        assert self.ob.resolve_orders() == [
            highest_bid,
            lowest_ask,
            second_highest_bid,
            second_lowest_ask,
        ]

    def test_bid_time_priority(self):
        first_bid = Order(user=self.user, direction=Direction.BUY, amount=10)
        second_bid = Order(user=self.user, direction=Direction.BUY, amount=10)
        ask = Order(user=self.user, direction=Direction.SELL, amount=10)

        self.ob.add_order(first_bid)
        self.ob.add_order(second_bid)
        self.ob.add_order(ask)

        assert self.ob.resolve_orders() == [first_bid, ask]

    def test_ask_time_priority(self):
        bid = Order(user=self.user, direction=Direction.BUY, amount=10)
        first_ask = Order(user=self.user, direction=Direction.SELL, amount=10)
        second_ask = Order(user=self.user, direction=Direction.SELL, amount=10)

        self.ob.add_order(bid)
        self.ob.add_order(first_ask)
        self.ob.add_order(second_ask)

        assert self.ob.resolve_orders() == [bid, first_ask]


if __name__ == "__main__":
    unittest.main()
