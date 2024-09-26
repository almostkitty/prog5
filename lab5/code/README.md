# Лабораторная работа 5. Работа с валютами. Шаблон «одиночка»

Написать код, который позволяет получать значения курсов валют с сайта [ЦБ РФ](http://www.cbr.ru/scripts/XML_daily.asp)
в объектно-ориентированном стиле. Реализовать шаблон проектирования "одиночка", чтобы нельзя было создать больше чем
один объект данного класса. Одиночка должен быть реализован с помощью метаклассов (см. [Method 3](https://stackoverflow.com/questions/6760685/what-is-the-best-way-of-implementing-singleton-in-python) )
Основа - функция ```get_currencies```, описанная ниже.

Требования к заданию:
1. Создать класс, реализовать методы для получения валюты, геттеры и сеттеры для задания входных параметров и результата,
конструкторы, деструкторы для атрибутов.
3. Хранить значения с плавающей точкой в формате: отдельно целая часть, отдельно - дробная часть (см. [ссылку](https://digitology.tech/docs/python_3/tutorial/floatingpoint.html))
4. Формат результата представлен ниже.
5. Если номинал валюты не 1, то сохраняем его, чтобы не было путаницы с переводом в рубли.
6. Реализовать контроль слишком частого выполнения запросов: запрос не должен отправляться чаще, чем 1 раз в какое-то время
(по умолчанию - это 1 с., но можно параметризовать параметр и указывать как часто может вызываться функция.
7. Написать тесты для проверки по неправильному коду возвращается словарь с неправильным id и значением None: ```{'R9999': None}```; 1-2 теста на корректные id: проверяете название валюты (русскоязычное) и диапазон значений от 0 до 999
8. Реализовать отдельный метод внутри класса, получающий данные о курсах валют и визуализирующий их в виде графика, который сохраняется в файле currencies.jpg и отображается в отчете README.md, представленный в репл-борде.



Формат возвращаемого результата:
```python
[{'GBP': ('Фунт стерлингов Соединенного королевства', '113,2069')},
 {'KZT': ('Казахстанских тенге', '19,8264')},
 {'TRY': ('Турецких лир', '33,1224')}]
```
или
```python
[{'GBP': ('Фунт стерлингов Соединенного королевства', '(113, 2069')},
 {'KZT': ('Казахстанских тенге', '(19,8264)')},
 {'TRY': ('Турецких лир', '(33, 1224)')}]
```
или decimal, т.е. для
```{'GBP': ('Фунт стерлингов Соединенного королевства', '113,2069')}``` объект можно представить в виде
``` {'GBP': ('Фунт стерлингов Соединенного королевства', ('113','2069') )}```


Необходимо изучить и использовать для выполнения ЛР материалы:
https://digitology.tech/docs/python_3/tutorial/floatingpoint.html