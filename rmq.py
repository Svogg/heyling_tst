from typing import List

from fastapi import WebSocket

import asyncio
from aio_pika import connect, Message, IncomingMessage, DeliveryMode


class AioRMQ:
    def __init__(self):
        self.connections: List[WebSocket] = []
        self.is_ready = False

    async def setup(self, queue_name: str):
        """
        Метод, устанавливающий соединение с брокером, объявляющий очередь, исполняющий сообщение в consumer
        :param queue_name:
        :return:
        """
        self.rabbit_conn = await connect(
            url="amqp://guest:guest@rabbitmq/",
            loop=asyncio.get_running_loop()
        )
        self.channel = await self.rabbit_conn.channel()
        self.queue_name = queue_name
        queue = await self.channel.declare_queue(self.queue_name)
        await queue.consume(self._reverse, no_ack=True)
        self.is_ready = True

    async def push(self, msg: str):
        """
        Метод, отправляющий сообщение в персистентную очередь
        :param msg:
        :return:
        """
        await self.channel.default_exchange.publish(
            Message(msg.encode('ascii'), delivery_mode=DeliveryMode.PERSISTENT),
            routing_key=self.queue_name,
        )

    async def connect(self, websocket: WebSocket):
        """
        Метод, подключающий к web-сокету
        :param websocket:
        :return:
        """
        await websocket.accept()
        self.connections.append(websocket)

    def remove(self, websocket: WebSocket):
        """
        Метод, удаляющий коннкет к web-сокету
        :param websocket:
        :return:
        """
        self.connections.remove(websocket)

    async def _reverse(self, message: IncomingMessage):
        """
        Метод, переворачивающий сообщение, освобождающий список конектов
        :param message:
        :return:
        """
        living_connections = []
        while len(self.connections) > 0:
            websocket = self.connections.pop()
            new_message = message.body[::-1]
            await websocket.send_text(f"{new_message}")
            living_connections.append(websocket)
        self.connections = living_connections
