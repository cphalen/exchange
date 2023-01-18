import numpy as np

from server.orderbook import Direction, Order


class Agent:
    def __init__(self):
        self.username = "agent"
        self.order_limit = 1000

    def generate_buy(self):
        pass

    def generate_sell(self):
        pass

    def generate_order(self):
        if np.random.uniform(0, 1) < 0.5:
            return self.generate_buy()
        else:
            return self.generate_sell()


class BondAgent(Agent):
    def generate_buy(self):
        direction = Direction.BUY
        amount = round(np.random.normal(loc=101, scale=2, size=None), 2)
        return Order(self.username, direction, amount)

    def generate_sell(self):
        direction = Direction.SELL
        amount = round(np.random.normal(loc=99, scale=2, size=None), 2)
        return Order(self.username, direction, amount)


def agent_of_symbol(symbol):
    match symbol.symbol_name():
        case "BOND":
            return BondAgent()
        case _:
            raise ValueError("No agent for provided symbol")
