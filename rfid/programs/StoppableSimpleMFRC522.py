import mfrc522


class StoppableSimpleMFRC522(mfrc522.SimpleMFRC522):
	def __init__(self):
		super().__init__()
		self.continue_reading = True
		self.READER = mfrc522.MFRC522(pin_mode=11)

	def read_id(self):
		id = self.read_id_no_block()
		while not id and self.continue_reading:
			id = self.read_id_no_block()
		return id

	def set_reading(self, continue_reading):
		self.continue_reading = continue_reading
