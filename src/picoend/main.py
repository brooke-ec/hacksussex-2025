import sys
import bluetooth
import asyncio
import aioble

_SERVICE_UUID = bluetooth.UUID(0xbce4)
_CHARACTERISTIC_UUID = bluetooth.UUID(0x29d2)

_ADV_INTERVAL = const(1000)

service = aioble.Service(_SERVICE_UUID)
characteristic = aioble.Characteristic(service, _CHARACTERISTIC_UUID, read=True, write=True, capture=True, notify=True)
aioble.register_services(service)

class Peer:
    def __init__(self, connection):
        self.addr = connection.device.addr_hex()
        self.connection = connection
    
    async def start(self):
        peers[self.addr] = self
        await self._handle()
        peers.pop(self.addr)
    
    async def _handle(self):
        try:
            peer_service = await self.connection.service(_SERVICE_UUID)
            if peer_service is None: return

            self.peer_characteristic = await peer_service.characteristic(_CHARACTERISTIC_UUID)
            if self.peer_characteristic is None: return

            del peer_service

            await self.peer_characteristic.subscribe(notify=True)
        except asyncio.TimeoutError:
            return

        try:
            while True:
                msg = await self.peer_characteristic.notified()
                sys.stdout.buffer.write(msg)
        except (aioble.DeviceDisconnectedError): ...

    async def send(self, content: bytes):
        for i in range(0, len(content), 20):
            characteristic.notify(self.connection, content[i:i+20])
            await asyncio.sleep(0.2)

async def listen():
    while True:
        connection = await aioble.advertise(_ADV_INTERVAL, name="communiko", services=[_SERVICE_UUID])
        await Peer(connection).start()

async def search():
    async with aioble.scan(0, active=True) as scanner:
        async for result in scanner:
            if  (
                result.name() == "communiko" and
                _SERVICE_UUID in result.services() and
                result.device.addr_hex() not in peers
            ):
                device = result.device
                connection = await result.device.connect()
                if connection is None: continue
                scanner.cancel()
                await Peer(connection).start()

async def input():
    while True:
        length = int.from_bytes(sys.stdin.buffer.read(1), "little")
        payload = sys.stdin.buffer.read(length)
        for peer in peers.values():
            peer.send(payload)

async def main():
    await asyncio.gather(listen(), search(), input())

peers: dict[str, Peer] = {}
asyncio.run(main())