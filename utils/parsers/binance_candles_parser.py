import requests
import json
import csv
from datetime import datetime, timedelta, date
import time
import pytz



# Чтение, получение, проверка и корректировка параметров из JSON файла
with open('utils/parsers/bn-config.json') as f:
    params = json.load(f)
f.close()

params['request']['start-time'] = max(params['request']['start-time'], params['mother-date']['mother-end-time'])
params['request']['end-time'] = min(datetime.strptime(params['request']['end-time'], '%Y-%m-%d').date(), datetime.now(pytz.timezone('Europe/Moscow')).date())
params['mother-date']['mother-end-time'] = params['request']['end-time']

with open('utils/parsers/bn-config.json', 'w') as f:
    json.dump(params, f, default=str)
f.close()

request_params = params['request']
misc_params = params['misc']
mother_date_params = params['mother-date']

symbol = request_params['symbol']
interval = request_params['interval']
start_time = int(datetime.strptime(request_params['start-time'], '%Y-%m-%d').timestamp()*1000)
end_time = int(datetime.strptime(request_params['end-time'].strftime('%Y-%m-%d'), '%Y-%m-%d').timestamp()*1000)
limit = request_params['limit']

time_sleep = misc_params['time-sleep']
csv_path = misc_params['csv-path']

mother_start_time = mother_date_params['mother-start-time']
mother_end_time = mother_date_params['mother-end-time']

count_of_requests = 0



# Функция для получения свечей с Binance API
def get_candles():
    url = 'https://api.binance.com/api/v3/klines'
    params = {
        'symbol': symbol,
        'interval': interval,
        'startTime': current_time,
        'endTime': end_time,
        'limit': limit  # Количество свечей, которые хотите получить за один запрос
    }
    response = requests.get(url, params=params)
    candles = json.loads(response.text)
    return candles


# Получение свечей с Binance API
all_candles = []
current_time = start_time

while current_time < end_time:
    count_of_requests += 1
    print(f"Запрос номер {count_of_requests}")
    candles = get_candles()
    all_candles.extend(candles)
    last_candle_time = candles[-1][0]
    current_time = int(last_candle_time) + 1
    time.sleep(time_sleep)
    print(f"current time: {current_time}\nend_time: {end_time}")


# Проверка CSV файла на наличие хеддера
header_flag = False
with open(csv_path, mode='r', newline='') as f:
    csv_temp = f.read()
f.close()
if "Date,Open,High,Low,Close,Volume,Close Time,Quote Asset Volume,Number of Trades,Taker Buy Base Asset Volume,Taker Buy Quote Asset Volume,Ignore" in csv_temp:
    header_flag = True


# Запись полученных свечей в CSV файл
skip_line = True
with open(csv_path, mode='a', newline='') as file:
    writer = csv.writer(file)
    if not header_flag:
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
        
        if skip_line: 
            skip_line = False 
            continue
        
        # Запись параметров свечи в CSV файл
        writer.writerow([open_time, open_price, high_price, low_price, close_price, volume, close_time, quote_asset_volume, number_of_trades, taker_buy_base_asset_volume, taker_buy_quote_asset_volume, ignore])