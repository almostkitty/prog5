## Лабораторная работа #5
#### Пальчук Г.А. ИВТ 2.1

### Отчёт о проделанной работе

1. ***Выполнена первоначальная настройка:*** Создано и активировано окружение; установлены необходимые библиотеки.


2. ***Реализован паттерн проектирования Singleton для класса ```CurrencyManager```.***


3. ***Реализован ```CurrencyManager```:*** Определены атрибуты класса для хранения списка валют, времени последнего запроса и минимального интервала между запросами.
Реализованы методы для установки и получения минимального интервала.


4. ***Получение данных о валютах:*** Написан метод ```get_currencies``` для отправки запроса, извлечения данных о валютах и их преобразования в нужный формат. Для точного представления и обработки значений валют использована библиотека ```Decimal```. Причина выбора ```Decimal``` – отсутствие необходимости выполнять математические операции с полученными значениями.


5. ***Визуализация курсов валют:*** Создан метод ```visualize_currencies```, который строит график на основе полученных данных о валютах. Добавил timestamp в название файла для удобства.
![](code/graphs/graph_2024-09-26_23-44-18.jpg)


### В процессе:
6. Написание тестов
