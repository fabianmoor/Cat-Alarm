import network
from utime import sleep
import sys
import rp2
from config import SSID, PASSWORD, MAX_WIFI_ATTEMPTS

# function to connect to wifi
def connect_to_wifi():
    # make a wifi object
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    # try to connect with our wifi name and password
    wlan.connect(SSID, PASSWORD)
    attempts = 0
    # keep trying until connected or too many attempts
    while not wlan.isconnected() and attempts < MAX_WIFI_ATTEMPTS:
        # check if bootsel button pressed to exit
        if rp2.bootsel_button() == 1:
            sys.exit()
        print(f'Waiting for connection... ({attempts+1}/{MAX_WIFI_ATTEMPTS})')
        sleep(1)
        attempts += 1

    # if still not connected, give up
    if not wlan.isconnected():
        print("Failed to connect to Wi-Fi.")
        return None
    # get our ip address
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip

# simple function to call the wifi connection
def connect():
    return connect_to_wifi()
