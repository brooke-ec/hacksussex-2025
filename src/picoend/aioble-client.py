import asyncio

import bluetooth
import aioble

_SERVICE_UUID = bluetooth.UUID(0x181A)
_CHARACTERISTIC_UUID = bluetooth.UUID(0x181A)

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
        
        service = await connection.service(_SERVICE_UUID)
        characteristic = await service.characteristic(_CHARACTERISTIC_UUID)

        msg = await characteristic.read()

        print(f"Recieved: {msg}")

asyncio.run(main())