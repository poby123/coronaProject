import time
from multiprocessing import Value
import MLX90614
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

class RaspberryController():
    def __init__(self, interrupt):
        self.temp_sensor = MLX90614.MLX90614()
        self.nfc_reader = SimpleMFRC522()
        self.interrupt = interrupt

    def getNFCId(self):
        n = 6
        for i in range(n):
            id, text = self.nfc_reader.read()
            if(self.interrupt.value):
                return 'INTERRUPTED'
            else:
                time.sleep(1)
        return id

    def getTemp(self):
        total = 0
        n = 6
        for i in range(n):
            total += float(self.temp_sensor.get_obj_temp()) 
            if(self.interrupt.value):
                return 'INTERRUPTED'
            time.sleep(0.5)
        return total / n
