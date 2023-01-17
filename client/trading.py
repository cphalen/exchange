import pickle


class ExchangeResponse:
    def __init__(self, ack, fill, error):
        self.ack = ack
        self.error = error
        self.fill = fill

    @staticmethod
    def ack():
        return ExchangeMessage(True, None, None)

    @staticmethod
    def fill(fill):
        return ExchangeMessage(None, fill, None)

    @staticmethod
    def error(error):
        return ExchangeMessage(None, None, error)

    @staticmethod
    def serialize(order_response):
        return pickle.dumps(order_response)

    @staticmethod
    def deserialize(message):
        return pickle.loads(message)

    def __str__(self, other):
        return (
            f"<OrderBookResponse ack={self.ack}, fill={self.fill},"
            f" error={self.error}>"
        )
