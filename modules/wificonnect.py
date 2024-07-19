import network
import time

def connect_to_wifi(ssid, password):
    print('[WIFI] Starting to connect to WiFi')

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print('[WIFI] Trying to connect to WiFi using SSID: '+ssid+' Pass: '+password)
        wlan.connect(ssid, password)

        while not wlan.isconnected():
            print('[WIFI] Connection not successful. Trying again in 2 seconds')
            time.sleep(2)
            pass
    
    print('[WIFI] Connected to network:', wlan.ifconfig())
    return True