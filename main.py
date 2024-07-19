import os
import time
from machine import Pin, SoftSPI
from modules.sdcard import SDCard
from config import get_config
import uasyncio as asyncio

from modules.wificonnect import connect_to_wifi

from webserver import init_webserver, serve_client
from work_loop import main_loop

# 1. READ CONFIG FROM SD CARD

spisd = SoftSPI(-1, miso=Pin(19), mosi=Pin(23), sck=Pin(18))
power_led = Pin(2, Pin.OUT)

def initialize_sd():
    print('[SD] Starting to initialize SD card')
    try:
        sd = SDCard(spisd, Pin(13))

        print('[SD] Card found successfully')
        return sd
    except Exception as e:
        print("[SD] An error occurred:", e)

        for _ in range(5):
            power_led.on()
            time.sleep(0.5)
            power_led.off()
            time.sleep(0.5)
        
        return None

sd = initialize_sd()

while sd is None:
    time.sleep(1)
    sd = initialize_sd()

vfs = os.VfsFat(sd)
os.mount(vfs, '/sd')

# GET CONFIG FROM SD
CONFIG = get_config()

power_led.off()

# CONNECT TO WIFI
WIFI = CONFIG['wifi'];
con = connect_to_wifi(WIFI['ssid'], WIFI['pass'])
if con:
    power_led.off()
    time.sleep(0.5)
    power_led.on()


async def main():
    # START WEB SERVER
    server_socket = init_webserver()
    server_task = asyncio.create_task(serve_client(server_socket))

    # MAIN LOOP
    gpio_task = asyncio.create_task(main_loop())

    await asyncio.gather(server_task, gpio_task)



# MAIN SCRIPT
asyncio.run(main())