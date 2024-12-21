import json
import asyncio
from abc import ABC, abstractmethod
from xml.etree import ElementTree as ET
import requests
import uvicorn
import time
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request


app = FastAPI()
clients = []
templates = Jinja2Templates(directory="templates")

# Абстрактный класс Observer - наблюдатель, который получает обновления.
class Observer(ABC):
    @abstractmethod
    async def update(self, message: str):
        pass

# Абстрактный класс Subject - субъекта, который управляет подписчиками.
class Subject(ABC):
    @abstractmethod
    def subscribe(self, observer: Observer):
        pass

    @abstractmethod
    def unsubscribe(self, observer: Observer):
        pass

    @abstractmethod
    def notify(self, message: str):
        pass

# Конкретная реализация Subject для работы с валютами.
class CurrenciesList(Subject):
    def __init__(self):
        self._observers = []
        self.last_update = None  # Время последнего обновления
        self.second_last_update = None  # Время предпоследнего обновления
    
    def subscribe(self, observer: Observer):
        self._observers.append(observer)

    def unsubscribe(self, observer: Observer):
        self._observers.remove(observer)

    async def notify(self, message: str):
        for observer in self._observers:
            await observer.update(message)  

    # Получение данных о курсах валют с сайта ЦБ
    def fetch(self):
        response = requests.get('http://www.cbr.ru/scripts/XML_daily.asp')
        root = ET.fromstring(response.content)
        currencies = {}
        for valute in root.findall('Valute'):
            charcode = valute.find('CharCode').text
            name = valute.find('Name').text
            value = float(valute.find('Value').text.replace(',', '.'))
            nominal = int(valute.find('Nominal').text)
            currencies[charcode] = {'name': name, 'value': value, 'nominal': nominal}
        return currencies

    # Метод для обновления данных и уведомления подписчиков
    async def update_data(self):
        currencies = self.fetch()  # Новые данные
        if currencies:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
            self.second_last_update = self.last_update
            self.last_update = current_time

            # Форматирование
            data_with_time = {
                "currencies": currencies,
                "last_update": self.last_update,
                "second_last_update": self.second_last_update
            }

            json_data = json.dumps(data_with_time)
            await self.notify(json_data)


# Конкретная реализация Observer для WebSocket-клиента
class WebSocketClient(Observer):
    def __init__(self, websocket: WebSocket):
        self.websocket = websocket
    
    async def update(self, message: str):
        await self.websocket.send_text(message)

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# WebSocket-обработчик для подключения клиентов
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()  # Принимаем подключение
    client = WebSocketClient(websocket)  # Создаем объект клиента
    clients.append(client)  # Добавляем его в список
    currency_data.subscribe(client)  # Подписываем его на обновления

    try:
        while True:
            await websocket.receive_text()
    except Exception:
        # На случай отключения клиента
        clients.remove(client)
        currency_data.unsubscribe(client)

# Обновление раз в 30 сек.
async def currency_updater():
    while True:
        await currency_data.update_data()
        await asyncio.sleep(30)

# Событие при старте
@app.on_event("startup")
async def startup_event():
    global currency_data
    currency_data = CurrenciesList()  # Инициализируем объект с данными о валютах
    task = asyncio.create_task(currency_updater())  # Запускаем задачу по обновлению данных

# Событие при остановке
@app.on_event("shutdown")
async def shutdown_event():
    for client in clients:
        await client.websocket.close()  # Закрываем соединения с клиентами

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)