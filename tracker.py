import requests
import time
import datetime
from connector import get_mean_relation, record_clean_change_price_value


symbol_1 = "BTCUSDT"
symbol_2 = "ETHUSDT"


def main():
    print(f'[INFO] Запущен трекинг цены на {symbol_2}')
    start_time: float = time.time()
    old_clean_change_price, old_price = get_clean_change_price(symbol1=symbol_1, symbol2=symbol_2)

    while True:
        current_time: float = time.time()
        current_clean_change_price, current_price = get_clean_change_price(symbol1=symbol_1, symbol2=symbol_2)
        percent_change_price = (current_price - old_price) / old_price * 100
        percent_clean_change_price: float = current_clean_change_price / old_price * 100
        record_clean_change_price_value(value=current_clean_change_price)
        now: datetime.datetime = datetime.datetime.now()

        if current_time - start_time >= 3600:
            start_time: float = time.time()
            old_clean_change_price, old_price = get_clean_change_price(symbol1=symbol_1, symbol2=symbol_2)

        if percent_clean_change_price >= 1:
            start_time: float = time.time()
            old_clean_change_price, old_price = get_clean_change_price(symbol1=symbol_1, symbol2=symbol_2)

            print(f"[INFO] [{now}] Собственное движение цены более чем на 1 процент за последний час")

        if percent_change_price >= 1:
            start_time: float = time.time()
            old_clean_change_price, old_price = get_clean_change_price(symbol1=symbol_1, symbol2=symbol_2)

            old_to_start_price: str = f"({old_price} -> {current_price})"
            print(f"[INFO] [{now}] Цена изменилась более чем на 1 процент за последний час {old_to_start_price}")


def get_clean_change_price(symbol1: str, symbol2: str) -> tuple[float, float]:
    change_price_1, current_price_1 = get_change_price_and_current_price(symbol=symbol1)
    change_price_2, current_price_2 = get_change_price_and_current_price(symbol=symbol2)
    mean_relation = get_mean_relation()
    if change_price_2 != 0:
        clean_relation_change_price: float = abs(change_price_1 / change_price_2 - mean_relation)
        clean_change_price: float = change_price_1 / clean_relation_change_price
    else:
        clean_change_price = 0
    return clean_change_price, current_price_2


def get_change_price_and_current_price(symbol: str) -> tuple[float, float]:
    response: requests.Response = requests.get(url=f"https://api.binance.com/api/v3/trades?symbol={symbol}&limit=1000")
    data: list[dict[str, str]] = response.json()
    last_price: float = float(data[0]["price"])
    first_price: float = float(data[-1]["price"])
    change_price: float = abs(last_price - first_price)
    return change_price, last_price


if __name__ == '__main__':
    main()
