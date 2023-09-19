import requests
import json
from datetime import datetime, timedelta

"""
        --------------------------------ВНИМАНИЕ!!!---------------------------------------
    
    СЕЙЧАС В КОДЕ СТОИТ ЛИМИТ 450 СВЕЧЕЙ ЗА ЗАПРОС, ЧТО РАВНЯЕТСЯ 900 ТОКЕНАМ
    1000 - МИНУТНЫЙ ЛИМИТ, ТАК ЧТО РАБОТАТЬ ОСТОРОЖНО! Я БЫ ДОПИСАЛ TIME.SLEEP СЕКУНД НА 5-10 ПОСЛЕ КАЖДОГО ЗАПРОСА.
    МОЖЕТ НУЖНО БОЛЬШЕ, А МОЖЕТ И НЕ НУЖНО. Я НЕ ЕБУ.
    
    ТАКЖЕ, ДИАПОЗОН ПАРСИНГА ВЫСТАВЛЕН С 17.08.2017 ПО 20.09.2017!!
    ЕСЛИ КОД ЗАПУСТИТЬ, НАПАРСИТ ДОХУЯ. ДУМАЙ.
    
    КСТАТИ, СНАЧАЛА НАДО ДОПИСАТЬ ДОПОЛНИТЕЛЬНЫЕ ПАРАМЕТРЫ СВЕЧЕЙ (ТИПА HIGH И LOW), А ЕЩЕ НАСТРОИТЬ ЗАПИСЬ В CSV
    + Я БЫ НА ЭТАПЕ ПАРСИНГА НЕМНОГО ПОДРЕДАЧИЛ ДАННЫЕ (НОРМИРОВАНИЕ, НО НЕ КАК ДЛЯ НЕЙРОНКИ)
"""




# Функция для получения свечей с Binance API
def get_candles(symbol, interval, start_time, end_time):
    url = 'https://api.binance.com/api/v3/klines'
    params = {
        'symbol': symbol,
        'interval': interval,
        'startTime': start_time,
        'endTime': end_time,
        'limit': 450  # Количество свечей, которые хотите получить за один запрос
    }
    response = requests.get(url, params=params)
    candles = json.loads(response.text)
    return candles

# Параметры для запроса свечей
symbol = 'BTCUSDT'
interval = '15m'
start_time = int(datetime(2017, 8, 17).timestamp() * 1000)
end_time = int(datetime(2023, 9, 20).timestamp() * 1000)

# Получение свечей с Binance API
all_candles = []
current_time = start_time

while current_time < end_time:
    candles = get_candles(symbol, interval, current_time, end_time)
    all_candles.extend(candles)
    last_candle_time = candles[-1][0]
    current_time = int(last_candle_time) + 1

# Обработка полученных свечей
for candle in all_candles:
    open_time = datetime.fromtimestamp(int(candle[0]) / 1000)
    open_price = float(candle[1])
    close_price = float(candle[4])
    volume = float(candle[5])
    
    # Выполните здесь свои операции с данными свечи (например, сохранение в файл или анализ)

    # Пример вывода значений
    print(f"Open Time: {open_time}, Open Price: {open_price}, Close Price: {close_price}, Volume: {volume}")