import bluetooth
import asyncio
import aioble

_COMMUNIKO_UUID = bluetooth.UUID("0492fcec-7194-11eb-9439-0242ac130002")

_L2CAP_MTU = const(128)
_L2CAP_PSN = const(22)

async def main():
    connection = await aioble.advertise(1000, name="communiko", services=[_COMMUNIKO_UUID])
    print(f"Connection from {connection.device}")

    channel = connection.l2cap_accept(_L2CAP_PSN, _L2CAP_MTU)
    buf = bytearray(channel.peer_mtu)
    buf[0] = 16
    await channel.send(buf)


asyncio.run(main())