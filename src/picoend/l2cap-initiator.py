import bluetooth
import asyncio
import aioble

_COMMUNIKO_UUID = bluetooth.UUID("0492fcec-7194-11eb-9439-0242ac130002")

_L2CAP_MTU = const(128)
_L2CAP_PSN = const(22)

async def main():
    async with aioble.scan(5000, 30000, 30000, active=True) as scanner:
        async for result in scanner:
            if _COMMUNIKO_UUID in result.services():
                device = result.device
                break
        else:
            print("File server not found")
            return
        
        connection = await device.connect()
        channel = await connection.l2cap_connect(_L2CAP_PSN, _L2CAP_MTU)
        while True:
            buf = bytearray(channel.our_mtu)
            await channel.recvinto(buf)
            print(buf)


asyncio.run(main())