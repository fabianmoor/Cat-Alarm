from machine import Pin
from utime import sleep_us, ticks_us, ticks_diff
from config import ULTRASONIC_TIMEOUT_US

# class for the ultrasonic sensor
class UltrasonicSensor:
    def __init__(self, trigger_pin, echo_pin):
        # setup the pins
        self.trigger = Pin(trigger_pin, Pin.OUT)
        self.echo = Pin(echo_pin, Pin.IN)

    # function to get distance in cm
    def get_distance_cm(self):
        # send a pulse
        self.trigger.low()
        sleep_us(2)
        self.trigger.high()
        sleep_us(5)
        self.trigger.low()

        # wait for echo to start
        start_time_high = ticks_us()
        pulse_start = None
        while self.echo.value() == 0:
            pulse_start = ticks_us()
            # timeout if taking too long
            if ticks_diff(ticks_us(), start_time_high) > ULTRASONIC_TIMEOUT_US:
                return -1

        # wait for echo to end
        start_time_low = ticks_us()
        pulse_end = None
        while self.echo.value() == 1:
            pulse_end = ticks_us()
            # timeout if taking too long
            if ticks_diff(ticks_us(), start_time_low) > ULTRASONIC_TIMEOUT_US:
                return -1

        # check if we got valid readings
        if pulse_start is None or pulse_end is None:
            return -1

        # calculate distance using time
        time_passed = ticks_diff(pulse_end, pulse_start)
        distance = (time_passed * 0.0343) / 2
        print("The distance from object is ", round(distance, 2), "cm")
        return distance
