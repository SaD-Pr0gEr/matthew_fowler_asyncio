import asyncio
from asyncio import AbstractEventLoop
from socket import socket, AF_INET, SOCK_STREAM
from typing import List, Tuple
from selectors import DefaultSelector, SelectorKey, EVENT_READ


class Server(socket):

    def __init__(self, host: str, port: int):
        super().__init__(AF_INET, SOCK_STREAM)
        self.host = host
        self.port = port
        self.bind((self.host, self.port))
        self.selector = DefaultSelector()

    def long_pool(self):
        print("Запускаю сервер...")
        self.listen()
        self.setblocking(False)
        print("Слушаю...")
        self.selector.register(self, EVENT_READ)
        try:
            while True:
                events: List[Tuple[SelectorKey, int]] = self.selector.select(1)  # Создать селектор с тайм-аутом 1 с
                if len(events) == 0:  # Если ничего не произошло, сообщить об этом. Такое возможно в случае тайм-аута
                    print('Событий нет, подожду еще!')
                for event, _ in events:
                    event_socket = event.fileobj  # Получить сокет, для которого произошло событие, он хранится в поле fileobj
                    if event_socket == self:  # Если событие произошло с серверным сокетом, значит, была попытка подключения
                        connection, address = self.accept()
                        connection.setblocking(False)
                        print(f"Получен запрос на подключение от {address}")
                        self.selector.register(connection, EVENT_READ)  # Зарегистрировать клиент, подключившийся к сокету
                    else:
                        data = event_socket.recv(1024)  # Если событие произошло не с серверным сокетом, получить данные от клиента и отправить их обратно
                        print(f"Получены данные: {data}")
                        event_socket.send(data)
        finally:
            self.close()


async def echo(connection: socket, loop: AbstractEventLoop) -> None:
    while data := await loop.sock_recv(connection, 1024):  # В бесконечном цикле ожидаем данных от клиента
        await loop.sock_sendall(connection, data)  # Получив данные, отправляем их обратно клиенту


async def listen_for_connection(server_socket: socket, loop: AbstractEventLoop):
    while True:
        connection, address = await loop.sock_accept(server_socket)
        connection.setblocking(False)
        print(f"Получен запрос на подключение от {address}")
        asyncio.create_task(echo(connection, loop))  # После получения запроса на подключение создаем задачу echo, ожидающую данные от клиента


async def main():
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_address = ('127.0.0.1', 8000)
    server_socket.setblocking(False)
    server_socket.bind(server_address)
    server_socket.listen()
    await listen_for_connection(server_socket, asyncio.get_event_loop())  # Запускаем сопрограмму прослушивания порта на предмет подключений


if __name__ == "__main__":
    # server = Server("127.0.0.1", 8000)
    # server.long_pool()
    asyncio.run(main())
