import requests
from connector import record_relation_change_prices


def get_and_record_binance_data(symbol_1: str, symbol_2: str) -> float:
    symbol_1_prices: list[float] = get_binance_symbol_prices(symbol=symbol_1)
    symbol_2_prices: list[float] = get_binance_symbol_prices(symbol=symbol_2)
    symbol_1_change_prices = abs(symbol_1_prices[0] - symbol_1_prices[-1]) / symbol_1_prices[-1]
    symbol_2_change_prices = abs(symbol_2_prices[0] - symbol_2_prices[-1]) / symbol_2_prices[-1]
    relation_symbol_1_to_symbol_2_change_prices: float = symbol_1_change_prices / symbol_2_change_prices
    record_relation_change_prices(relation_symbol_1_to_symbol_2_change_prices)
    return relation_symbol_1_to_symbol_2_change_prices


def get_binance_symbol_prices(symbol: str) -> list[float]:
    result: list = list()

    response: requests.Response = requests.get(url=f"https://api.binance.com/api/v3/trades?symbol={symbol}&limit=1000")
    data: list[dict] = response.json()

    for current_data in data:
        price: float = float(current_data["price"])
        result.append(price)

    result: list[float] = list(set(result))
    return result


def main() -> None:
    while True:
        get_and_record_binance_data(symbol_1="BTCUSDT", symbol_2="ETHUSDT")


if __name__ == '__main__':
    main()
