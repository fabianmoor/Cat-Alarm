from machine import Pin, PWM, Timer
from config import TONES, TOGGLE_INTERVAL_MS

# class for the active buzzer (simple on/off)
class ActiveBuzzer:
    def __init__(self, pin):
        # setup the pin
        self.buzzer_pin = Pin(pin, Pin.OUT)

    # turn buzzer on
    def turn_on(self):
        self.buzzer_pin.value(1)

    # turn buzzer off
    def turn_off(self):
        self.buzzer_pin.value(0)

    # simple on function
    def on(self):
        self.turn_on()

    # simple off function
    def off(self):
        self.turn_off()

# class for passive buzzer (can make different tones)
class PassiveBuzzer:

    def __init__(self, pin):
        # setup pwm for making tones
        self.buzzer_pwm = PWM(Pin(pin))
        self.is_buzzing = False
        self.playing_high_tone = True
        # timer for switching tones
        self.my_timer = Timer()

    # make a tone at specific frequency
    def make_tone(self, frequency):
        self.buzzer_pwm.duty_u16(12768)
        self.buzzer_pwm.freq(frequency)

    # stop making sound
    def stop_sound(self):
        self.buzzer_pwm.duty_u16(0)

    # check if making sound
    def is_making_sound(self):
        return self.is_buzzing

    # start the alarm sound with alternating tones
    def start_alarm_sound(self):
        if not self.is_buzzing:
            self.is_buzzing = True
            self.playing_high_tone = True
            # start with E5 tone
            self.make_tone(TONES["E5"])
            # setup timer to switch tones
            self.my_timer.init(period=TOGGLE_INTERVAL_MS, mode=Timer.PERIODIC,
                             callback=self.switch_tones)

    # stop the alarm sound
    def stop_alarm_sound(self):
        if self.is_buzzing:
            self.is_buzzing = False
            self.my_timer.deinit()
            self.stop_sound()

    # function called by timer to switch between tones
    def switch_tones(self, timer_obj):
        if self.is_buzzing:
            if self.playing_high_tone:
                # switch to E6 tone
                self.make_tone(TONES["E6"])
            else:
                # switch to E5 tone
                self.make_tone(TONES["E5"])
            self.playing_high_tone = not self.playing_high_tone

    # clean up everything when done
    def cleanup_everything(self):
        self.stop_alarm_sound()
        self.buzzer_pwm.deinit()

    # play tones manually for a certain time
    def play_manual_arpeggio(self, how_long_ms=1000, switch_every_ms=50):
        from utime import ticks_ms, sleep
        end_time = ticks_ms() + how_long_ms
        use_high_tone = True

        # keep switching tones until time is up
        while ticks_ms() < end_time:
            if use_high_tone:
                self.make_tone(TONES["E5"])
            else:
                self.make_tone(TONES["E6"])
            use_high_tone = not use_high_tone
            sleep(switch_every_ms / 1000)

        self.stop_sound()

    # simple activate function
    def activate(self):
        self.start_alarm_sound()

    # simple deactivate function
    def deactivate(self):
        self.stop_alarm_sound()

    # make it quiet
    def be_quiet(self):
        self.stop_sound()

    # check if active
    def is_active(self):
        return self.is_making_sound()

    # cleanup function
    def cleanup(self):
        self.cleanup_everything()

    # play a single tone
    def play_tone(self, frequency):
        self.make_tone(frequency)

    # play the arpeggio manually
    def play_arpeggio(self, duration_ms=1000, interval_ms=50):
        self.play_manual_arpeggio(duration_ms, interval_ms)

    # update tone function (doesn't do anything right now)
    def update_tone(self):
        pass

# class for LED control
class LED:
    def __init__(self, pin):
        # setup the led pin
        self.led_pin = Pin(pin, Pin.OUT)

    # turn led on
    def turn_on(self):
        self.led_pin.on()

    # turn led off
    def turn_off(self):
        self.led_pin.off()

    # simple on function
    def on(self):
        self.turn_on()

    # simple off function
    def off(self):
        self.turn_off()
