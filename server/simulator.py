import os
import time
from symbol.symbol import symbol_of_string
from agent.agent import agent_of_symbol
from server.orderbook import Direction

debug = os.environ.get("EXCHANGE_SERVER_DEBUG", True)
symbol = symbol_of_string(os.environ.get("EXCHANGE_SERVER_SYMBOL", "BOND"))

class Simulator:
    def __init__(self, username, bot, ob):
        self.username = username
        self.bot = bot
        self.ob = ob
        self.agent = agent_of_symbol(symbol)

    def tick(self):
        # stop playing if we reach the order limit
        if self.ob.num_bids() + self.ob.num_asks() >= self.agent.order_limit:
            return True

        # generate order from agent if limit not reached
        order = self.agent.generate_order()
        self.ob.add_order(order)

        # call player provided callback function for buy or sell
        match order.direction:
            case Direction.BUY:
                self.bot.buy(order.order_id, order.amount)
            case Direction.SELL:
                self.bot.sell(order.order_id, order.amount)

        # try and resolve orders
        fills = self.ob.resolve_orders()

        # call player provided callback function for fill
        for fill in fills:
            self.bot.fill(fill["buy"].order_id, fill["sell"].order_id)

        return False


    def run(self):
        # call the player provided init callback function
        self.bot.init()

        # run simulation until we reach stalemate
        while not self.tick():
            pass

        return self.ob.get_payout(self.username)
