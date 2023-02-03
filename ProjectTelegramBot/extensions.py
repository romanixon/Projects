import requests
import json
from config import keys

class APIExeption(Exception):
    pass

class ValueConverter:
    @staticmethod
    def get_price(quote: int, base: int, amount: int):
        if quote == base:
            raise APIExeption(f'Невозможно перевести одинаковые валюты{base}.')

        try:
            quote_tiker = keys[quote]
        except KeyError:
            raise APIExeption(f'Не удалось обработать валюту {quote}')

        try:
            base_tiker = keys[base]
        except KeyError:
            raise APIExeption(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIExeption(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_tiker}&tsyms={base_tiker}')
        total_base = json.loads(r.content)[keys[base]]
        final_base = total_base * amount


        return final_base

