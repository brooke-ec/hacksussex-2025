import bluetooth
import asyncio
import aioble

_SERVICE_UUID = bluetooth.UUID(0xbce3)
_CHARACTERISTIC_UUID = bluetooth.UUID(0x29d6)

_ADV_INTERVAL = const(1000)

service = aioble.Service(_SERVICE_UUID)
characteristic = aioble.Characteristic(service, _CHARACTERISTIC_UUID, read=True, write=True, capture=True, notify=True)
aioble.register_services(service)

class Peer:
    def __init__(self, connection):
        self.addr = connection.device.addr_hex()
        self.connection = connection
    
    def start(self):
        peers[self.addr] = self
        async def wrapper():
            await self._handle()
            peers.pop(self.addr)
            print(f"Cleaning up: {self.addr}")
        asyncio.create_task(wrapper())
    
    async def _handle(self):
        try:
            peer_service = await self.connection.service(_SERVICE_UUID)
            if peer_service is None: return

            self.peer_characteristic = await peer_service.characteristic(_CHARACTERISTIC_UUID)
            if self.peer_characteristic is None: return

            await self.peer_characteristic.subscribe(notify=True)
        except asyncio.TimeoutError:
            return

        asyncio.create_task(self.test())

        try:
            while True:
                msg = await self.peer_characteristic.notified()
                print(f"Notified: {msg}")
        except (aioble.DeviceDisconnectedError): ...

    async def test(self):
        await asyncio.sleep(2)
        self.send(b"Hehe :3")

    def send(self, content: bytes):
        characteristic.notify(self.connection, content)

async def listen():
    while True:
        connection = await aioble.advertise(_ADV_INTERVAL, name="communiko", services=[_SERVICE_UUID])
        print(f"New Connection from {connection.device}")
        Peer(connection).start()

async def search():
    while True:
        async with aioble.scan(0, 30000, 30000, active=True) as scanner:
            async for result in scanner:
                if  (
                    result.name() == "communiko" and
                    _SERVICE_UUID in result.services() and
                    result.device.addr_hex() not in peers
                ):
                    connection = await result.device.connect()
                    if connection is None: continue
                    Peer(connection).start()

async def main():
    await asyncio.gather(listen(), search())

peers: dict[str, Peer] = {}
asyncio.run(main())