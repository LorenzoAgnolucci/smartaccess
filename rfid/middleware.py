from rfid.programs.RFIDSingleton import RFIDSingleton
import RPi.GPIO as GPIO


class ReaderMiddleware:
	def __init__(self, get_response):
		self.get_response = get_response
		GPIO.setwarnings(False)
		self.reader = RFIDSingleton()

	def __call__(self, request):
		self.reader.set_reading(False)
		# self.reader.set_reading(True)
		GPIO.setwarnings(False)
		GPIO.cleanup()
		GPIO.setmode(GPIO.BCM)
		# Red LED
		GPIO.setup(17, GPIO.OUT)
		# Green LED
		GPIO.setup(18, GPIO.OUT)
		# Blue LED
		GPIO.setup(26, GPIO.OUT)

		GPIO.output(17, GPIO.LOW)
		GPIO.output(18, GPIO.LOW)
		GPIO.output(26, GPIO.LOW)

		response = self.get_response(request)

		return response

