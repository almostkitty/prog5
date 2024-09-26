import requests
from xml.etree import ElementTree as ET
import time
import os
import matplotlib.pyplot as plt
from decimal import Decimal
from datetime import datetime


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class CurrencyManager(metaclass=Singleton):
    def __init__(self):
        self.currencies = []
        self.last_request_time = 0
        self.min_interval = 1


    def set_min_interval(self, interval: float):
        self.min_interval = interval

    def get_min_interval(self):
        return self.min_interval


    def get_currencies(self, currencies_ids_lst: list) -> list:
        if time.time() - self.last_request_time < self.min_interval:
            raise Exception(f"Запросы разрешено отправлять не чаще, чем каждые {self.min_interval} секунд.")

        cur_res_str = requests.get('http://www.cbr.ru/scripts/XML_daily.asp')
        root = ET.fromstring(cur_res_str.content)
        valutes = root.findall("Valute")

        result = []
        for _v in valutes:
            valute_id = _v.get('ID')
            if valute_id in currencies_ids_lst:
                valute_cur_name = _v.find('Name').text
                valute_cur_val = _v.find('Value').text.replace(',', '.')
                valute_charcode = _v.find('CharCode').text


                decimal_value = Decimal(valute_cur_val)
                whole_part = int(decimal_value // 1)
                fractional_part = int((decimal_value % 1) * 10000)

                result.append({valute_charcode: (valute_cur_name, (whole_part, fractional_part))})

        self.currencies = result
        self.last_request_time = time.time()

        return result


    def visualize_currencies(self, folder='graphs'):
        if not self.currencies:
            raise Exception("Нет данных для визуализации.")

        if not os.path.exists(folder):
            os.makedirs(folder)

        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f'graph_{timestamp}.jpg'
        file_path = os.path.join(folder, filename)


        fig, ax = plt.subplots()
        currencies = []
        values = []

        for el in self.currencies:
            for code, data in el.items():
                currencies.append(code)
                whole, fractional = data[1]
                values.append(float(f"{whole}.{fractional}"))

        ax.bar(currencies, values, color='tab:blue')
        ax.set_ylabel('Курс валюты к рублю')
        ax.set_title('Курсы валют')

        plt.savefig(file_path)
        plt.close(fig)


if __name__ == '__main__':
    currency_manager = CurrencyManager()
    currency_manager.set_min_interval(1)

    try:
        result = currency_manager.get_currencies(['R01805F', 'R01375', 'R01235', 'R01090B', 'R01239'])
        print(result)
    except Exception as e:
        print(e)

    currency_manager.visualize_currencies()
