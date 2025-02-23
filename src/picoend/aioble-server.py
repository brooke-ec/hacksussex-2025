import asyncio
import bluetooth
import aioble

_SERVICE_UUID = bluetooth.UUID(0x181A)

_ADV_INTERVAL = const(1000)

async def main():
    connection = await aioble.advertise(
            _ADV_INTERVAL,
            name="communiko",
            services=[_SERVICE_UUID],
        )
    
    print(f"Connection From {connection.device}")

asyncio.run(main())