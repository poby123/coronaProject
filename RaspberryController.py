import time
from multiprocessing import Value
import MLX90614
import RPi.GPIO as GPIO
from mfrc522 import MyMFRC522


class RaspberryController():
    def __init__(self, interrupt):
        self.nfc_reader = MyMFRC522(interrupt)
        self.interrupt = interrupt

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
        for i in range(n):
            total += float(temp_sensor.get_obj_temp())
            if(self.interrupt.value):
                return 'INTERRUPTED'
            time.sleep(0.5)
        return round(total / n, 2)


if __name__ == '__main__':
    v = Value('b', False)
    con = RaspberryController(v)
    for i in range(100):
        time.sleep(1)
        res = con.getTemp()
        # res = con.getNFCId()
        print(res)
