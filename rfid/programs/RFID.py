import mfrc522
from time import sleep
from datetime import datetime


reader = mfrc522.SimpleMFRC522()
correct_value = False
text = ""
value = ""


while not correct_value:
	text = input("Insert the integer number of accesses or an expiration date (format YYYY-MM-DD): ")
	if text.isdigit():
		correct_value = True
		break
	try:
		datetime.strptime(text, "%Y-%m-%d")
		correct_value = True
	except ValueError:
		print("Insert a correct value (for example: 10 or 1997-03-15)")
print("Now scan a card")
id_w, text_w = reader.write(text)
print(id_w, text_w)

sleep(5)

print("Read a card")
id_r, text_r = reader.read()
text_r = text_r.rstrip(" ")
try:
	if text_r.isdigit():
		value = int(text_r)
		print("Number of accesses: {}".format(value))
	else:
		value = datetime.strptime(text, "%Y-%m-%d").date()
		print("Expiration date: {}".format(value))
except ValueError:
	print("Error")
