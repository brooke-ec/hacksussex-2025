from mpremote.transport_serial import SerialTransport
from mpremote.transport import TransportError
from typing import Any, Callable
import serial.tools.list_ports
from serial import Serial
import threading
import time


class CommunikoBookworm:
    def __init__(self) -> None:
        self.serial = self._connect()

    def join(self, consumer: Callable[[bytes], Any]):
        while True:
            if self.serial.inWaiting():
                length = int.from_bytes(self.serial.read(1), "little")
                print(length)
                consumer(self.serial.read(length))
            else:
                time.sleep(0.01)

    def write(self, payload: bytes):
        length = len(payload).to_bytes(1, "little")
        self.serial.write(length + payload)

    def _connect(self) -> Serial:
        # Auto-detect and auto-connect to the first available USB serial port.
        for p in sorted(serial.tools.list_ports.comports()):
            if p.vid is not None and p.pid is not None:
                try:
                    return SerialTransport(p.device, baudrate=115200).serial
                except TransportError as er:
                    if not er.args[0].startswith("failed to access"):
                        raise er
        raise TransportError("no device found")

bookworm = CommunikoBookworm()
threading.Thread(target=lambda: bookworm.write("".encode())).start()
bookworm.join(print)