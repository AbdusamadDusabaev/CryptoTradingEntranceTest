import datetime
import sqlite3


relation_table: str = "relation_ethusdt_to_btcusdt_change_prices"
clean_change_price_table: str = "clean_change_price_of_ethusdt"


def run_sql_query(query: str) -> (None, list[dict[str, int]], dict[str, int]):
    connect: sqlite3.Connection = sqlite3.connect(database="sqlite.db")
    with connect:
        cursor = connect.cursor()
        cursor.execute(query)
        connect.commit()
        result_sql_query = cursor.fetchall()
        return result_sql_query


def create_tables() -> None:
    create_relation_table()
    create_clean_change_price_table()


def create_relation_table() -> None:
    run_sql_query(query=f"CREATE TABLE {relation_table} (value DOUBLE, time DATETIME);")
    print(f"[INFO] Таблица {relation_table} успешно создана")


def create_clean_change_price_table() -> None:
    run_sql_query(query=f"CREATE TABLE {clean_change_price_table} (value DOUBLE, time DATETIME);")
    print(f"[INFO] Таблица {clean_change_price_table} успешно создана")


def record_relation_change_prices(value: float) -> None:
    now: datetime.datetime = datetime.datetime.now()
    query_to_record: str = f"INSERT INTO {relation_table} VALUES({value}, '{now}');"
    run_sql_query(query=query_to_record)
    print(f"[INFO] Значение отношения изменения цен {value} успешно записано в базу данных")


def record_clean_change_price_value(value: float) -> None:
    now: datetime.datetime = datetime.datetime.now()
    query_to_record: str = f"INSERT INTO {clean_change_price_table} VALUES({value}, '{now}');"
    run_sql_query(query=query_to_record)


def get_mean_relation() -> float:
    query_to_get_mean_relation: str = f"SELECT AVG(value) FROM {relation_table};"
    result_query_to_get_mean_relation: list[tuple[float]] = run_sql_query(query=query_to_get_mean_relation)
    mean_relation: float = result_query_to_get_mean_relation[0][0]
    return mean_relation


if __name__ == '__main__':
    create_tables()
