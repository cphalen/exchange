import unittest
from symbol.symbol import Bond

from server.orderbook import Direction, Order, OrderBook


class OrderBookTest(unittest.TestCase):
    def setUp(self):
        self.ob = OrderBook(symbol=Bond)
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

        assert self.ob.resolve_orders() == [
            {"buy": highest_bid, "sell": lowest_ask}
        ]

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

        assert self.ob.resolve_orders() == [
            {"buy": highest_bid, "sell": lowest_ask}
        ]

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
            {"buy": highest_bid, "sell": lowest_ask},
            {"buy": second_highest_bid, "sell": second_lowest_ask},
        ]

    def test_bid_time_priority(self):
        first_bid = Order(user=self.user, direction=Direction.BUY, amount=10)
        second_bid = Order(user=self.user, direction=Direction.BUY, amount=10)
        ask = Order(user=self.user, direction=Direction.SELL, amount=10)

        self.ob.add_order(first_bid)
        self.ob.add_order(second_bid)
        self.ob.add_order(ask)

        assert self.ob.resolve_orders() == [{"buy": first_bid, "sell": ask}]

    def test_ask_time_priority(self):
        bid = Order(user=self.user, direction=Direction.BUY, amount=10)
        first_ask = Order(user=self.user, direction=Direction.SELL, amount=10)
        second_ask = Order(user=self.user, direction=Direction.SELL, amount=10)

        self.ob.add_order(bid)
        self.ob.add_order(first_ask)
        self.ob.add_order(second_ask)

        assert self.ob.resolve_orders() == [{"buy": bid, "sell": first_ask}]

    def test_order_id_increment(self):
        order_1 = Order(user=self.user, direction=Direction.BUY, amount=100)
        order_2 = Order(user=self.user, direction=Direction.BUY, amount=110)
        order_3 = Order(user=self.user, direction=Direction.SELL, amount=120)

        assert order_2.order_id - order_1.order_id == 1
        assert order_3.order_id - order_2.order_id == 1


if __name__ == "__main__":
    unittest.main()
