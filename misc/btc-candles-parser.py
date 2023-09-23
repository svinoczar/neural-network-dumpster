import requests
import json
import csv
from datetime import datetime, timedelta
import time

"""
    --------------------------------ВНИМАНИЕ!!!---------------------------------------
    
    СЕЙЧАС В КОДЕ СТОИТ ЛИМИТ 550 СВЕЧЕЙ ЗА ЗАПРОС, ЧТО РАВНЯЕТСЯ 900 ТОКЕНАМ
    1200 - МИНУТНЫЙ ЛИМИТ, ТАК ЧТО РАБОТАТЬ ОСТОРОЖНО! 
    
    ТАКЖЕ, ДИАПОЗОН ПАРСИНГА ВЫСТАВЛЕН С 17.08.2017 ПО 20.09.2023!!

"""

# JSON
data = json.loads("config.json")


# Функция для получения свечей с Binance API
def get_candles(symbol, interval, start_time, end_time, limit):
    url = 'https://api.binance.com/api/v3/klines'
    params = {
        'symbol': symbol,
        'interval': interval,
        'startTime': start_time,
        'endTime': end_time,
        'limit': limit  # Количество свечей, которые хотите получить за один запрос
    }
    response = requests.get(url, params=params)
    candles = json.loads(response.text)
    return candles

# Параметры для запроса свечей
symbol = 'BTCUSDT'
interval = '15m'
start_time = int(datetime(2017, 8, 17).timestamp() * 1000)
end_time = int(datetime(2023, 9, 20).timestamp() * 1000)
limit = 550

# Получение свечей с Binance API
all_candles = []
current_time = start_time
request_count = 1

while current_time < end_time:
    print(f"Запрос номер {request_count}")
    candles = get_candles(symbol, interval, current_time, end_time)
    all_candles.extend(candles)
    last_candle_time = candles[-1][0]
    current_time = int(last_candle_time) + 1
    request_count += 1
    time.sleep(1.25)

# Запись полученных свечей в CSV файл
with open('candles.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote Asset Volume', 'Number of Trades', 'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume', 'Ignore'])
    for candle in all_candles:
        open_time = datetime.fromtimestamp(int(candle[0]) / 1000)
        open_price = float(candle[1])
        high_price = float(candle[2])
        low_price = float(candle[3])
        close_price = float(candle[4])
        volume = float(candle[5])
        close_time = datetime.fromtimestamp(int(candle[6]) / 1000)
        quote_asset_volume = float(candle[7])
        number_of_trades = int(candle[8])
        taker_buy_base_asset_volume = float(candle[9])
        taker_buy_quote_asset_volume = float(candle[10])
        ignore = float(candle[11])
        
        # Запись параметров свечи в CSV файл
        writer.writerow([open_time, open_price, high_price, low_price, close_price, volume, close_time, quote_asset_volume, number_of_trades, taker_buy_base_asset_volume, taker_buy_quote_asset_volume, ignore])