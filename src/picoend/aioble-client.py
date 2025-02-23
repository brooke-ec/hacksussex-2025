import asyncio

from numpy import char
import bluetooth
import aioble

_SERVICE_UUID = bluetooth.UUID(0x181A)
_CHARACTERISTIC_UUID = bluetooth.UUID(0x181A)
service = aioble.Service(_SERVICE_UUID)
characteristic = aioble.Characteristic(service, _CHARACTERISTIC_UUID, write=True, notify=True)
aioble.register_services(service)

async def main():
    async with aioble.scan(5000, 30000, 30000, active=True) as scanner:
        async for result in scanner:
            if _SERVICE_UUID in result.services():
                device = result.device
                break
        else:
            print("File server not found")
            return
        
        print(f"Found {device}")
        connection = await device.connect()
        
        characteristic.notify(connection, "Hello World")

asyncio.run(main())