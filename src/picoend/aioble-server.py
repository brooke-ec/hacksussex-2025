import asyncio
import bluetooth
import aioble

_SERVICE_UUID = bluetooth.UUID(0x181A)
_CHARACTERISTIC_UUID = bluetooth.UUID(0x181A)
service = aioble.Service(_SERVICE_UUID)
characteristic = aioble.Characteristic(service, _CHARACTERISTIC_UUID, read=True, notify=True)
aioble.register_services(service)

_ADV_INTERVAL = const(1000)

async def listen():
    connection = await aioble.advertise(
            _ADV_INTERVAL,
            name="communiko",
            services=[_SERVICE_UUID],
        )
    
    print(f"Connection From {connection.device}")

    msg = await characteristic.written()
    print(f"Recieved: {msg}")

asyncio.run(listen())