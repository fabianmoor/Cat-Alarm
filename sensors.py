from machine import Pin, time_pulse_us
from utime import sleep_us

SOUND_SPEED_CM_PER_US = 0.0343
TRIG_PULSE_DURATION_US = 10

class UltrasonicSensor:
    def __init__(self, trigger_pin, echo_pin):
        self.trigger = Pin(trigger_pin, Pin.OUT)
        self.echo = Pin(echo_pin, Pin.IN)
        self.trigger.value(0)
        sleep_us(5)

    def get_distance_cm(self):
        self.trigger.value(1)
        sleep_us(TRIG_PULSE_DURATION_US)
        self.trigger.value(0)

        pulse_duration_us = time_pulse_us(self.echo, 1, 30000)

        if pulse_duration_us < 0:
            return -1

        distance = (pulse_duration_us * SOUND_SPEED_CM_PER_US) / 2

        print("The distance from object is {:.2f} cm".format(distance))
        return distance
