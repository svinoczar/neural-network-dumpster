import csv
import requests
from datetime import datetime, timedelta
import time
import json
import pytz


# Чтение, получение, проверка и корректировка параметров из JSON файла
with open('misc/bb-config.json') as f:
    params = json.load(f)
f.close()

params['request']['start-time'] = max(params['request']['start-time'], params['mother-date']['mother-end-time'])
params['request']['end-time'] = min(datetime.strptime(params['request']['end-time'], '%Y-%m-%d').date(), datetime.now(pytz.timezone('Europe/Moscow')).date())
params['mother-date']['mother-end-time'] = params['request']['end-time']

with open('misc/bb-config.json', 'w') as f:
    json.dump(params, f, default=str)
f.close()

request_params = params['request']
misc_params = params['misc']
mother_date_params = params['mother-date']

symbol = request_params['symbol']
interval = request_params['interval']
start_time = int(datetime.strptime(request_params['start-time'], '%Y-%m-%d').timestamp())
end_time = int(datetime.strptime(request_params['end-time'].strftime('%Y-%m-%d'), '%Y-%m-%d').timestamp())
delta_time = timedelta(days=request_params['delta_time'])

time_sleep = misc_params['time-sleep']
csv_path = misc_params['csv-path']

mother_start_time = mother_date_params['mother-start-time']
mother_end_time = mother_date_params['mother-end-time']

count_of_requests = 1


# Функция для получения свечей с Binance API
def get_candles():
    url = f'https://api.bybit.com/v2/public/kline/list?symbol={symbol}&interval={interval}&from={int(start_time.timestamp())}&to={int((start_time + delta_time).timestamp())}'
    response = requests.get(url)
    if response.status_code == 200:
        candles = response.json()
    return candles


# Получение свечей с Binance API
all_candles = []
current_time = start_time

while current_time < end_time:
    print(f"Запрос номер {count_of_requests}")
    candles = get_candles()
    all_candles.extend(candles)
    start_time += delta_time
    count_of_requests += 1
    time.sleep(time_sleep)


# Проверка CSV файла на наличие хеддера
header_flag = False
with open(csv_path, mode='r', newline='') as f:
    csv_temp = f.read()
f.close()
if "Timestamp,Open price,Close price,High price,Low price,Volume" in csv_temp:
    header_flag = True 


skip_line = True
with open(csv_path, mode='a', newline='') as file:
    writer = csv.writer(file)
    if not header_flag:
        writer.writerow(['Timestamp', 'Open price', 'Close price',
                        'High price', 'Low price', 'Volume'])
    for candle in all_candles:
        timestamp = datetime.fromtimestamp(candle['open_time']).strftime('%Y-%m-%d %H:%M:%S')
        open_price = candle['open']
        close_price = candle['close']
        high_price = candle['high']
        low_price = candle['low']
        volume = candle['volume']
        
        if skip_line: 
            skip_line = False 
            continue
        
        
        # Запись параметров свечи в CSV файл
        writer.writerow([timestamp, open_price, close_price, high_price, low_price, volume])