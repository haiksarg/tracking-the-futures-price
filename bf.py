"""Тестовое задание Python-разработчик (Junior)."""

import requests
import time

ENDPOINT = 'https://fapi.binance.com/fapi/v1/ticker/price?symbol=XRPUSDT'


def get_api_answer():
    """Делает запрос к эндпоинту API-сервиса."""
    try:
        response = requests.get(ENDPOINT)
    except Exception as error:
        raise ConnectionError(f'Сбой в работе программы: Эндпоинт {ENDPOINT} '
                              f'недоступен. {error}')
    else:
        return response.json()


def check_response(response):
    """Проверяет ответ API на соответствие документации."""
    if not isinstance(response, dict):
        raise TypeError('Ответ API не является словарём.')
    if 'price' not in response:
        raise KeyError('Цена не передана')
    return float(response.get('price'))


def main():
    """Основная логика работы."""
    timestamp = int(time.time())

    hight_price = {'price': 0}

    while True:
        try:
            response = get_api_answer()
            if response.get('time') - timestamp > 3600:
                timestamp = response.get('time')
                hight_price['price'] = 0
            current_price = {'price': check_response(response)}
            print(current_price['price'])
            if current_price['price'] > hight_price['price']:
                hight_price = current_price.copy()
            elif current_price['price'] < hight_price['price'] * 0.99:
                print('Цена упала на 1% от максимальной за последний час. '
                      f'Сейчас: {current_price["price"]}, '
                      f'максимальная за час: {hight_price["price"]}')
        except Exception as error:
            print(f'Сбой в работе программы: {error}')


if __name__ == '__main__':
    main()
