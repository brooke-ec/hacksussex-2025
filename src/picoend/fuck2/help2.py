# Import necessary modules
from machine import Pin
import bluetooth
from ble_simple_peripheral import BLESimplePeripheral
import time

# Create a Bluetooth Low Energy (BLE) object
ble = bluetooth.BLE()
# Create an instance of the BLESimplePeripheral class with the BLE object
sp = BLESimplePeripheral(ble)

def scan(callback=None):
        addr_type = None
        addr = None
        scan_callback = callback
        ble.gap_scan(2000, 30000, 30000)

    # Connect to the specified device (otherwise use cached address from a scan).
def connect(addr_type=None, addr=None, callback=None):
        _addr_type = addr_type
        _addr = addr 
        _conn_callback = callback
        if _addr_type is None or _addr is None:
            return False
        ble.gap_connect(_addr_type, _addr)
        return True

# Set the debounce time to 0. Used for switch debouncing
debounce_time=0
not_found = False

def on_scan(addr_type, addr, name):
    if addr_type is not None:
        print("Found sensor: %s" % name)
        connect()
    else:
        not_found = True
        print("No sensor found.")

    scan(callback=on_scan)

# Create a Pin object for Pin 0, configure it as an input with a pull-up resistor
pin = Pin(0, Pin.IN, Pin.PULL_UP)

while True:
    # Check if the pin value is 0 and if debounce time has elapsed (more than 300 milliseconds)
    if ((pin.value() is 0) and (time.ticks_ms()-debounce_time) > 300):
        # Check if the BLE connection is established
        if sp.is_connected():
            # Create a message string
            msg="toggle"
            # Send the message via BLE
            sp.send(msg)
        # Update the debounce time    
        debounce_time=time.ticks_ms()