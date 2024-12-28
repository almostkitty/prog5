## Цель работы
Необходимо создать программу на языке Python, которая использует паттерн проектирования "Наблюдатель" для отслеживания изменений курсов валют через API Центробанка РФ. Программа должна запрашивать курсы валют и уведомлять зарегистрированных наблюдателей о изменении курсов в реальном времени или через заданные интервалы времени.


Структура реализованного задания должна представлять

- Объект — веб-сервер Flask или FastAPI, Tornado.

- Наблюдатели - клиенты, представляющие HTML-страницы, связывающиеся с объектом с помощью веб-сокетов. На странице должен отображаться идентификатор клиента.


## Комментарии по выполнению
Изучите пример реализации схемы шаблона «Наблюдатель»: https://refactoringguru.cn/ru/design-patterns/observer/python/example. 

Проанализируйте код: 
- https://github.com/tornadoweb/tornado/tree/stable/demos/chat

- https://github.com/tornadoweb/tornado/tree/stable/demos/websocket


Назначение: 

- Объект (Subject) будет запрашивать данные с API и отслеживать изменения курсов.

- Наблюдатели (Observers) будут получать уведомления об изменении курса и отображать информацию. Например, наблюдателями могут быть различные компоненты системы, которые отслеживают конкретные валюты (например, USD, EUR, GBP).