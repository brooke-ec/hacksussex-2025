import bluetooth
import asyncio
import aioble

_SERVICE_UUID = bluetooth.UUID(0xbce3)
_CHARACTERISTIC_UUID = bluetooth.UUID(0x29d6)

_ADV_INTERVAL = const(1000)

service = aioble.Service(_SERVICE_UUID)
characteristic = aioble.Characteristic(service, _CHARACTERISTIC_UUID, read=True, write=True, capture=True)
aioble.register_services(service)

async def accept():
    while True:
        await aioble.advertise(_ADV_INTERVAL, name="communiko", services=[_SERVICE_UUID])
        payload = await characteristic.written()
        print(f"Recieved: {payload}")

async def send(payload: bytes):
    async with aioble.scan(0, 30000, 30000, active=True) as scanner:
        async for result in scanner:
            if  (result.name() == "communiko" and _SERVICE_UUID in result.services()):
                try:
                    connection = await result.device.connect()
                    if connection is None: return
                except asyncio.TimeoutError:
                    continue

                with connection:                
                    try:
                        peer_service = await connection.service(_SERVICE_UUID)
                        if peer_service is None: return

                        peer_characteristic = await peer_service.characteristic(_CHARACTERISTIC_UUID)
                        if peer_characteristic is None: return
                    except asyncio.TimeoutError:
                        continue

                    peer_characteristic.write(payload)
                    await asyncio.sleep(1)

async def main():
    await asyncio.gather(accept())

asyncio.run(main())