from machine import Pin
import time
import sys

onboardLED = Pin(25, Pin.OUT)

def write(payload: bytes):
        length = len(payload).to_bytes(1, "little")
        sys.stdout.buffer.write(length + payload)

sys.stdin.read(1)
write("Hello World!".encode())

while True:
    onboardLED.toggle()
    time.sleep(1)
