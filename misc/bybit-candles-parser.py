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

params['request']['start-time'] = max(params['request']
                                      ['start-time'], params['mother-date']['mother-end-time'])
params['request']['end-time'] = min(datetime.strptime(params['request']['end-time'],
                                    '%Y-%m-%d').date(), datetime.now(pytz.timezone('Europe/Moscow')).date())
params['mother-date']['mother-end-time'] = params['request']['end-time']

with open('misc/bb-config.json', 'w') as f:
    json.dump(params, f, default=str)
f.close()

request_params = params['request']
misc_params = params['misc']
mother_date_params = params['mother-date']

symbol = request_params['symbol']
interval = request_params['interval']
start_time = datetime.strptime(request_params['start-time'], '%Y-%m-%d')
end_time = datetime.strptime(
    request_params['end-time'].strftime('%Y-%m-%d'), '%Y-%m-%d')
delta_time = timedelta(days=request_params['delta_time'])
limit = request_params['limit']

time_sleep = misc_params['time-sleep']
csv_path = misc_params['csv-path']

mother_start_time = mother_date_params['mother-start-time']
mother_end_time = mother_date_params['mother-end-time']

count_of_requests = 1


# Проверка CSV файла на наличие хеддера
header_flag = False
with open(csv_path, mode='r', newline='') as f:
    csv_temp = f.read()
f.close()
if "Timestamp,Open price,Close price,High price,Low price,Volume,Turnover" in csv_temp:
    header_flag = True


# Запись полученных свечей в CSV файл
skip_line = True
with open(csv_path, mode='a', newline='') as file:
    writer = csv.writer(file)
    if not header_flag:
        writer.writerow(['Timestamp', 'Open price', 'Close price',
                        'High price', 'Low price', 'Volume', 'Turnover'])
    while start_time < end_time:
        print(f"Запрос номер {count_of_requests}")
        count_of_requests += 1

        url = f'https://api.bybit.com/v2/public/kline/list?symbol={symbol}&interval={interval}&from={int(start_time.timestamp())}&to={int((start_time + delta_time).timestamp())}&limit={limit}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            klines = data['result']
            for kline in klines:
                timestamp = datetime.fromtimestamp(kline['open_time']).strftime('%Y-%m-%d %H:%M:%S')
                open_price = kline['open']
                close_price = kline['close']
                high_price = kline['high']
                low_price = kline['low']
                volume = kline['volume']
                turnover = kline['turnover']
                
                if skip_line:
                    skip_line = False
                    continue
                
                # Запись параметров свечи в CSV файл
                writer.writerow([timestamp, open_price, close_price,
                        high_price, low_price, volume, turnover])
        else: print('Ooops! Something went wrong...')
        print(f'{timestamp}')
        start_time += delta_time
        time.sleep(time_sleep)