import bluetooth
import asyncio
import aioble

_SERVICE_UUID = bluetooth.UUID(0xbce3)
_CHARACTERISTIC_UUID = bluetooth.UUID(0x29d6)

_ADV_INTERVAL = const(1000)

service = aioble.Service(_SERVICE_UUID)
characteristic = aioble.Characteristic(service, _CHARACTERISTIC_UUID, read=True, write=True, capture=True)
aioble.register_services(service)

class Peer:
    def __init__(self, device: aioble.Device):
        self.peer_characteristic: aioble.Characteristic = None
        self.addr: str = device.addr_hex()
        self.device = device

    async def start(self):
        peers[self.addr] = self
        await self._handle()
        print(f"Cleaning up {self.addr}")
        peers.pop(self.addr)

    async def _handle(self):
        print(f"Connecting to {self.addr}")
        try:
            connection = await self.device.connect()
            if connection is None: return

            peer_service = await connection.service(_SERVICE_UUID)
            if peer_service is None: return

            self.peer_characteristic = await peer_service.characteristic(_CHARACTERISTIC_UUID)
            if self.peer_characteristic is None: return
        except asyncio.TimeoutError:
            return
        
        self.send(b"Teehee test")
        
        await connection.device_task()

    def send(self, payload: bytes):
        print("Writing")
        self.peer_characteristic.write(payload)

async def accept():
    while True:
        connection = await aioble.advertise(_ADV_INTERVAL, name="communiko", services=[_SERVICE_UUID])
        print(f"Accepting connection from {connection.device.addr_hex()}")
    
async def search():
    while True:
        async with aioble.scan(0, 30000, 30000, active=True) as scanner:
            async for result in scanner:
                if  (
                    result.name() == "communiko" and
                    _SERVICE_UUID in result.services() and
                    result.device.addr_hex() not in peers
                ):
                    await Peer(result.device).start()

async def receive():
    while True:
        payload = await characteristic.written()
        print(f"Recieved {payload}")

async def main():
    await asyncio.gather(search(), accept(), receive())

peers: dict[str, Peer] = {}
asyncio.run(main())