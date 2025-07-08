from machine import Pin
from utime import sleep, ticks_ms, ticks_diff
import sys

# get our other files
from config import LED_PIN, PUSH_BUTTON_PIN
from network_manager import connect
from ubidots_client import UbidotsClient
from sensors import UltrasonicSensor
from actuators import ActiveBuzzer, PassiveBuzzer, LED

# connect to wifi first
print("Connecting to WiFi...")
if connect() is None:
    print("ERROR: WiFi connection failed, exiting")
    sys.exit()

# make the ubidots client
print("Initializing Ubidots client...")
ubidots_client = UbidotsClient()

# setup all the hardware stuff
print("Initializing hardware components...")
ultrasonic_sensor = UltrasonicSensor(trigger_pin=20, echo_pin=21)
active_buzzer = ActiveBuzzer(pin=27)
passive_buzzer = PassiveBuzzer(pin=26)
onboard_led = LED(pin=LED_PIN)
push_button = Pin(PUSH_BUTTON_PIN, Pin.IN, Pin.PULL_UP)

# tell user we're ready
print("=== SYSTEM READY ===")
print("Press button to toggle sensor on/off")
print("Current status: System active, sensor OFF")

# variables to keep track of stuff
led_state = False
last_button_state = push_button.value()
last_ubidots_send_time = 0
UBIDOTS_COOLDOWN_MS = 5000

# function to turn passive buzzer on or off
def update_passive_buzzer_state(activate):
    if activate and not passive_buzzer.is_active():
        passive_buzzer.activate()
    elif not activate and passive_buzzer.is_active():
        passive_buzzer.deactivate()

# check if button was pressed
def check_button_press():
    global led_state, last_button_state

    current_button_state = push_button.value()
    # if button just got pressed
    if current_button_state == False and last_button_state == True:
        print("Button press detected")
        
        # toggle the sensor on/off
        led_state = not led_state
        if led_state:
            onboard_led.on()
            print(">>> SENSOR ACTIVATED - Distance monitoring ON")
        else:
            onboard_led.off()
            print(">>> SENSOR DEACTIVATED - Distance monitoring OFF")
        sleep(0.05)

    last_button_state = current_button_state

# check the sensor and do stuff if something is detected
def handle_sensor_reading():
    global last_ubidots_send_time
    distance = ultrasonic_sensor.get_distance_cm()
    # if something is close enough
    if distance > 0 and distance <= 20:
        if not active_buzzer.buzzer_pin.value():
            print(f"ALERT! Object detected at {distance:.1f}cm - Activating alarms!")
        # turn on the buzzers
        active_buzzer.on()
        update_passive_buzzer_state(True)

        # send data to ubidots
        current_time = ticks_ms()
        if ticks_diff(current_time, last_ubidots_send_time) > UBIDOTS_COOLDOWN_MS:
            print("Sending data to Ubidots...")
            ubidots_client.send_data(value=1)
            ubidots_client.send_distance(distance)
            last_ubidots_send_time = current_time
        else:
            print("Ubidots cooldown active, skipping API call")

        sleep(0.5)
    else:
        # nothing detected, turn off alarms
        if active_buzzer.buzzer_pin.value():
            print("Object moved away - Deactivating alarms")
        active_buzzer.off()
        update_passive_buzzer_state(False)

# turn everything off
def turn_everything_off():
    active_buzzer.off()
    update_passive_buzzer_state(False)
    passive_buzzer.be_quiet()

# main loop that runs forever
while True:
    check_button_press()

    # if sensor is on, check sensor
    if led_state:
        handle_sensor_reading()
        passive_buzzer.update_tone()
        sleep(0.05)
    else:
        # sensor is off, turn everything off
        turn_everything_off()
        sleep(0.1)
