class Symbol:
    def symbol_name() -> str:
        pass

    def true_value() -> int:
        pass


class Bond(Symbol):
    def symbol_name():
        return "BOND"

    def true_value():
        return 100


def symbol_of_string(s: str):
    for symbol in [Bond]:
        if symbol.symbol_name() == s:
            return symbol
    raise ValueError("No such symbol")
