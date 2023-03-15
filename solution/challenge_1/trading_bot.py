class TradingBot:
    """
    In this class you will write callback functions that dictate how your
    trading bot will trade in a 1 minute trading simulation. The system running
    the simulation will call the callback functions you define below when
    specific events happen (for example: someone adds a "buy" or "sell" order
    to the orderbook).

    Although we are only leaving you with 4 callback functions to complete.
    Feel free to add additional helper functions, global state, or even create
    additional Python files that your code references.

    These actions, however, are disallowed:
      - I/O from disk or the web
      - Using external Python packages in your code
    """

    def __init__(self, actions) -> None:
        self.actions = actions
        self.buy_price = 99
        self.sell_price = 101

    def open(self) -> None:
        """
        This function is called by the simulation when the simulation begins.
        You can add any buy or sell orders that you want to exist on the
        orderbook at the beginning of the simulation.
        """
        self.buy_id = self.actions.add_buy(self.buy_price)
        self.sell_id = self.actions.add_sell(self.sell_price)

    def buy(self, order_id: int, amount: float) -> None:
        """
        This function is called by the simulation when some other agent adds a
        buy order (i.e. they are buying at the given amount) to the orderbook.
        Your code should respond accordingly, now knowing that this buy order
        exists on the orderbook.
        """
        pass

    def sell(self, order_id: int, amount: float) -> None:
        """
        This function is called by the simulation when some other agent adds a
        sell order (i.e. they are selling at the given amount) to the
        orderbook. Your code should respond accordingly, now knowing that this
        sell order exists on the orderbook.
        """
        pass

    def fill(self, buy_order_id: int, sell_order_id: int) -> None:
        """
        This function is called by the simulation when the orderbook fills two
        orders. In other words, the orderbook is taking the buy order and
        matching it will the sell order, so the transaction is resolved and
        these two orders are taken off the orderbook. Your code should respond
        accordingly, now knowing that these orders no longer exist on the
        orderbook.
        """
        if buy_order_id == self.buy_id:
            self.buy_id = self.actions.add_buy(self.buy_price)

        if sell_order_id == self.sell_id:
            self.sell_id = self.actions.add_sell(self.sell_price)
