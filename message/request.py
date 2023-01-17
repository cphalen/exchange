import pickle


class ExchangeRequest:
    def __init__(self, user: str, balance: bool, buy: float, sell: float) -> None:
        self.user = user
        self.balance = balance
        self.buy = buy
        self.sell = sell

    @staticmethod
    def balance(user):
        return ExchangeMessage(user, True, None, None)

    @staticmethod
    def buy(user, amount):
        return ExchangeMessage(user, None, amount, None)

    @staticmethod
    def sell(user, amount):
        return ExchangeMessage(user, None, None, amount)

    @staticmethod
    def serialize(order_response):
        return pickle.dumps(order_response)

    @staticmethod
    def deserialize(message):
        return pickle.loads(message)
