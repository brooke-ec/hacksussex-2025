from machine import Pin, PWM, I2C
from ssd1306 import SSD1306_I2C # type: ignore
import time


i2c=I2C(0,sda=Pin(0), scl=Pin(1), freq=400000)


time.sleep(1) 


display = SSD1306_I2C(128, 32, i2c)


display.fill(0) 


def LED_Control():
    gween.value(1)
    time.sleep(0.1)
    gween.value(0)


def Buzzer_Control(vol, note, delay1, delay2):
    buzzer.duty_u16(vol)
    buzzer.freq(note)
    time.sleep(delay1)
    buzzer.duty_u16(0)
    time.sleep(delay2)


button = Pin(8, Pin.IN, Pin.PULL_DOWN)
gween = Pin(18, Pin.OUT)
buzzer = PWM(Pin(13))


display.text("Message recived!", 0,0)
display.show()
time.sleep(1)
message_recived = True
volume = 1000
c = 523
d = 587
e = 659
g = 784

while(message_recived):
    LED_Control()
    Buzzer_Control(volume,c,0.1, 0)    
    if(button.value() == 1):
        message_recived = False

    LED_Control()
    Buzzer_Control(volume,d,0.1, 0)    
    if(button.value() == 1):
        message_recived = False

    LED_Control()
    Buzzer_Control(volume,e,0.1, 0)
    if(button.value() == 1):
        message_recived = False
    LED_Control()
    Buzzer_Control(volume,g,0.1, 0)

    if(button.value() == 1):
        message_recived = False
    
    time.sleep(0.3)

display.fill(0)
display.text("Acknowledged!", 0, 0)
display.show()








