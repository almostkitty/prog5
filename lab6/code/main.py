import requests
from xml.etree import ElementTree as ET
import io
import json
import csv
from abc import ABC, abstractmethod


# Абстрактный интерфейс компонента. Является шаблоном для fetch. Все классы после него -- реализуют этот метод.
class Component(ABC):
    @abstractmethod
    def fetch(self):
        pass


# Конкретный компонент. Возвращает инфу с сайта ЦБ. Просто парсинг + возврат в виде словаря.
class CurrenciesList(Component):
    def fetch(self):
        response = requests.get('http://www.cbr.ru/scripts/XML_daily.asp')
        root = ET.fromstring(response.content)
        currencies = {}
        for valute in root.findall('Valute'):
            charcode = valute.find('CharCode').text
            name = valute.find('Name').text
            value = float(valute.find('Value').text.replace(',', '.'))
            currencies[charcode] = {'name': name, 'value': value, 'nominal': 1}
        return currencies


# Базовый декоратор. Принимает объект Component и делегирует вызов get_data вложенному объекту
class Decorator(Component):
    def __init__(self, component: Component):
        self._component = component

    @abstractmethod
    def fetch(self):
        return self._component.fetch()


# Конкретный декоратор для JSON.
class DecoratorJSON(Decorator):
    def fetch(self):
        data = self._component.fetch()
        return json.dumps(data, indent=2, ensure_ascii=False)  # Для отступ + отключение аскии


# Конкретный декоратор для csv.
class DecoratorCSV(Decorator):
    def fetch(self):
        data = self._component.fetch()

        if isinstance(data, str):
            raise TypeError("Не форматируется из json в csv!")
        
        output = io.StringIO()
        writer = csv.writer(output)

        writer.writerow(['CharCode', 'Name', 'Value', 'Nominal'])

        for charcode, info in data.items():
            writer.writerow([charcode, info['name'], info['value'], info['nominal']])

        return output.getvalue()


if __name__ == "__main__":
    currencies = CurrenciesList()

    json_decorator = DecoratorJSON(currencies)
    print("Data in JSON format:")
    print(json_decorator.fetch())

    csv_decorator = DecoratorCSV(currencies)
    print("\nData in CSV format:")
    print(csv_decorator.fetch())
