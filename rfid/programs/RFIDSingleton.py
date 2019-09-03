from rfid.programs.StoppableSimpleMFRC522 import StoppableSimpleMFRC522


class RFIDSingleton(object):

	__instance = None

	def __new__(cls, *args, **kwargs):
		if cls.__instance is None:
			cls.__instance = StoppableSimpleMFRC522()
			cls.__instance.name = "The only reader"
		return cls.__instance



