from machine import Pin,UART
uart = UART(0,9600)

LedGPIO = 16
led = Pin(LedGPIO, Pin.OUT)

while True:
    if uart.any():
        command = uart.readline()
        print(command)   # uncomment this line to see the recieved data
        if command==b'1':
            led.high()
            print("ON")
        elif command==b'3':
            led.low()
            print("OFF")