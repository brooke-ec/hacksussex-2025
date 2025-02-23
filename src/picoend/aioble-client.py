import asyncio
import bluetooth
import aioble

_SERVICE_UUID = bluetooth.UUID(0x181A)

_ADV_INTERVAL = const(1000)

async def main():
    async with aioble.scan(duration_ms=6000) as scanner:
        async for result in scanner:
            print(result, result.name(), result.rssi, result.services())

asyncio.run(main())