import requests
import json
import pandas as pd

'''




WORK IN PROGRESS . . .




'''

def get_candle_data(symbol, interval, start_time, end_time):
    url = f"https://public.bybit.com/spot/kline/list?symbol={symbol}&interval={interval}&from={start_time}&to={end_time}"
    response = requests.get(url)
    data = json.loads(response.text)
    return data["result"]

symbol = "BTCUSDT"
interval = "15min"
start_time = 1625097600  # Время начала (1 июля 2021 года, 00:00:00)
end_time = 1692662400  # Время окончания (20 сентября 2023 года, 00:00:00)

candle_data = get_candle_data(symbol, interval, start_time, end_time)

df = pd.DataFrame(candle_data, columns=["timestamp", "open", "high", "low", "close", "volume"])

print("Информация о процессе парсинга:")
print(f"Загружено {len(df)} свечей для пары {symbol} с интервалом {interval}")
print(df)