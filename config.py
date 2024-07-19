import json
import time
import os
from machine import Pin

power_led = Pin(2, Pin.OUT)

def get_config():
    # CHECK IF CONFIG EXISTS
    if not 'config.json' in os.listdir('/sd'):
        print('[SD] Config file not found')
        while True:
            for _ in range(2):
                power_led.on()
                time.sleep(0.2)
                power_led.off()
                time.sleep(0.2)

    f = open('/sd/config.json', 'r');
    CONFIG = json.load(f)
    f.close()

    return CONFIG