class TradingActions:
    """
    These two functions will be overwritten when you submit to the trading
    simulation. You can assume they work as described and you should use them
    in your TradingBot code.
    """

    def add_buy(amount: int) -> int:
        """
        Creates a buy order on the orderbook (i.e. you are buying at a certain
        price). This function returns the order_id of the new buy order that is
        created.
        """
        pass

    def add_sell(amount: int) -> int:
        """
        Creates a sell order on the orderbook (i.e. you are selling at a
        certain price). This function returns the order_id of the new sell
        order that is created.
        """
        pass
