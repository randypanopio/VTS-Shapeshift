from m_utils import log as logging
import asyncio
import websockets

# TODO add keep alive and reconnect logic

class WebSocketConnection:
    def __init__(self, url):
        self.url = url
        self.websocket = None
        self.lock = asyncio.Lock()
        self.timeout = 10

    async def connect(self):
        self.websocket = await asyncio.wait_for(websockets.connect(self.url), 3)

    async def close(self):
        await self.websocket.close()
        self.websocket = None

    async def send(self, message):
        try:
            if self.websocket is None:
                await self.connect()
            async with self.lock:
                await self.websocket.send(message)
        except Exception as e:
            print(e)

    async def receive(self):
        try:
            if self.websocket is None:
                await self.connect()
            async with self.lock:
                return await self.websocket.recv()
        except Exception as e:
            print(e)