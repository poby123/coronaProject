import RPi.GPIO as gpio
import time


class Ultra:
    def __init__(self):
        gpio.setmode(gpio.BCM)
        trig = 5
        echo = 6
        gpio.setup(trig, gpio.OUT)
        gpio.setup(echo, gpio.IN)

    def getDistance(self):
        time.sleep(0.2)
        gpio.output(self.trig, 1)
        time.sleep(0.00001)
        gpio.output(self.trig, 0)

        while gpio.input(self.echo) == 0:
            pulse_start = time.time()

        while gpio.input(self.echo) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17000
        distance = round(distance, 2)

        return distance
