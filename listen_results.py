import asyncio

import websockets
from websockets.exceptions import ConnectionClosed


class Receiver:
    """
    Класс-получатель
    """

    def __init__(self, dsn):
        self.dsn = dsn

    async def receive(self):
        """
        метод, который подключается к web-сокету и получает приходящие сообщения
        :return:
        """
        async with websockets.connect(self.dsn) as websocket:
            while True:
                try:
                    data = await websocket.recv()
                    print(f'Received data: {data[2:-1]}')
                except ConnectionClosed:
                    print('Connection closed')
                    break
                except TimeoutError:
                    print('Too long connection')
                    break


async def main():
    listener = Receiver('ws://localhost:8000/listen_results')
    await listener.receive()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Stopped')
