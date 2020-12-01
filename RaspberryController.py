import time
from multiprocessing import Value
import MLX90614
import RPi.GPIO as GPIO
import Ultra
from mfrc522 import MyMFRC522


class RaspberryController():
    def __init__(self, interrupt):
        self.nfc_reader = MyMFRC522(interrupt)
        self.interrupt = interrupt
        gpio.setmode(gpio.BCM)
        gpio.setup(trig, gpio.OUT)
        gpio.setup(echo, gpio.IN)

    def __del__(self):
        GPIO.cleanup()

    def getNFCId(self):
        try:
            id = self.nfc_reader.read_id()
        finally:
            pass
        return id

    def getTemp(self):
        temp_sensor = MLX90614.MLX90614()
        total = 0
        n = 4
        while(self.getDistance() >= 8.0):
            time.sleep(0.2)
        for i in range(n):
            total += float(temp_sensor.get_obj_temp())
            if(self.interrupt.value):
                return 'INTERRUPTED'
            time.sleep(0.5)
        return round(total / n, 2)

    def getDistance(self):
        trig = 5
        echo = 6

        time.sleep(0.2)
        gpio.output(trig, 1)
        time.sleep(0.00001)
        gpio.output(trig, 0)

        while gpio.input(echo) == 0:
            pulse_start = time.time()

        while gpio.input(echo) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17000
        distance = round(distance, 2)

        return distance

# import time
# from multiprocessing import Value


# class RaspberryController():
#     def __init__(self, interrupt):
#         self.interrupt = interrupt

#     def __del__(self):
#         pass

#     def getNFCId(self):
#         try:
#             time.sleep(1)
#             id = 138164
#         finally:
#             pass
#         return id

#     def getTemp(self):
#         n = 4
#         total = 0
#         for i in range(n):
#             total += 36.52
#             if(self.interrupt.value):
#                 return 'INTERRUPTED'
#             time.sleep(0.5)
#         return round(total / n, 2)


if __name__ == '__main__':
    v = Value('b', False)
    con = RaspberryController(v)
    for i in range(100):
        time.sleep(1)
        res = con.getTemp()
        # res = con.getNFCId()
        print(res)
