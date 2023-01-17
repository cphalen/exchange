import pickle


class ExchangeResponse:
    def __init__(self, bid, ask, fill):
        self.bid = bid
        self.ask = ask
        self.fill = fill

    @staticmethod
    def bid(amount):
        return ExchangeMessage(bid, None, None)

    @staticmethod
    def ask(fill):
        return ExchangeMessage(None, ask, None)

    @staticmethod
    def fill(error):
        return ExchangeMessage(None, None, fill)

    @staticmethod
    def serialize(order_response):
        return pickle.dumps(order_response)

    @staticmethod
    def deserialize(message):
        return pickle.loads(message)
