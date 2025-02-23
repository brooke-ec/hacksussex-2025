import asyncio
import bluetooth
import aioble

_SERVICE_UUID = bluetooth.UUID(0x181A)
_CHARACTERISTIC_UUID = bluetooth.UUID(0x181A)
service = aioble.Service(_SERVICE_UUID)
characteristic = aioble.Characteristic(service, _CHARACTERISTIC_UUID, write=True, notify=True)
aioble.register_services(service)

_ADV_INTERVAL = const(1000)

async def main():
    connection = await aioble.advertise(
            _ADV_INTERVAL,
            name="communiko",
            services=[_SERVICE_UUID],
        )
    
    print(f"Connection From {connection.device}")

    await characteristic.written()
    msg = characteristic.read()

    print(f"Recieved: {msg}")

asyncio.run(main())