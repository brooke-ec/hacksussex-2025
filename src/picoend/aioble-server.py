import asyncio
import bluetooth
import aioble

_SERVICE_UUID = bluetooth.UUID(0xbce3)
_CHARACTERISTIC_UUID = bluetooth.UUID(0x29d6)
service = aioble.Service(_SERVICE_UUID)
characteristic = aioble.Characteristic(service, _CHARACTERISTIC_UUID, read=True, write=True, capture=True, notify=True)
aioble.register_services(service)

_ADV_INTERVAL = const(1000)

async def listen():
    connection = await aioble.advertise(
            _ADV_INTERVAL,
            name="communiko",
            services=[_SERVICE_UUID],
        )
    
    print(f"Connection From {connection.device}")

    await asyncio.sleep(2)

    characteristic.notify(connection, b"Hello Notify")
    characteristic.write(b"Hello Write", send_update=True)

asyncio.run(listen())