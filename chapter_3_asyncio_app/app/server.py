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


if __name__ == "__main__":
    server = Server("127.0.0.1", 8000)
    server.long_pool()
