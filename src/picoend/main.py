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
    def __init__(self, addr: str):
        self.addr = addr
    
    def start(self):
        print(self.addr)
        peers[self.addr] = self
        async def wrapper():
            await self._handle()
            peers.pop(self.addr)
            print(f"Cleaning up: {self.addr}")
        asyncio.create_task(wrapper())
    
    async def _handle(self):
        ...


class IncomingPeer(Peer):
    ...


class OutgoingPeer(Peer):
    def __init__(self, device: aioble.Device):
        super().__init__(device.addr_hex())
        self.device = device

    async def _handle(self):
        try:
            connection = await self.device.connect()
            if connection is None: return

            peer_service = await connection.service(_SERVICE_UUID)
            if peer_service is None: return

            peer_characteristic = await peer_service.characteristic(_CHARACTERISTIC_UUID)
            if peer_characteristic is None: return

            await peer_characteristic.subscribe(notify=True)
        except asyncio.TimeoutError:
            return

        while True:
            msg = await peer_characteristic.notified()
            print(f"Notified: {msg}")
            msg = await peer_characteristic.read()

async def listen():
    connection = await aioble.advertise(_ADV_INTERVAL, name="communiko", services=[_SERVICE_UUID])
    print(f"New Connection from {connection.device}")
    await Peer(characteristic).join()

async def search():
    while True:
        async with aioble.scan(0, 30000, 30000, active=True) as scanner:
            async for result in scanner:
                if  (
                    result.name() == "communiko" and
                    _SERVICE_UUID in result.services() and
                    result.device.addr_hex() not in peers
                ):
                    OutgoingPeer(result.device).start()

                    

async def main():
    await asyncio.gather(search())

peers: dict[str, Peer] = {}
asyncio.run(main())