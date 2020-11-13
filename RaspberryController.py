import time
from multiprocessing import Value
import MLX90614
import RPi.GPIO as GPIO
from mfrc522 import MyMFRC522

class RaspberryController():
	def __init__(self, interrupt):
		self.temp_sensor = MLX90614.MLX90614()
		self.nfc_reader = MyMFRC522(interrupt)
		self.interrupt = interrupt

	def getNFCId(self):
		try:
			id = self.nfc_reader.read_id()
		finally:
			GPIO.cleanup()
		return id

	def getTemp(self):
		total = 0
		n = 6
		for i in range(n):
			total += float(self.temp_sensor.get_obj_temp()) 
		if(self.interrupt.value):
			return 'INTERRUPTED'
		#time.sleep(0.5)
		return total / n

if __name__ == '__main__':
	v = Value('b', False)
	con = RaspberryController(v)
	#res = con.getTemp()
	res = con.getNFCId()
	print(res)
