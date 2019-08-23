from ..models import RFIDCard, Log
import random
import datetime


def random_RFIDCard():
    for card in RFIDCard.objects.all():
        card.remaining_accesses = random.randint(0, 10)
        m = random.randint(1, 12)
        d = random.randint(1, 28)
        card.expiration_date = datetime.date(2020, m, d)
        card.save()


def random_Log():
    cards = [1029061268929, 3781788120489, 5279589593186, 6036919168649, 6910589627279, 7557228076112]
    for _ in range(50):
        card_id = cards[random.randint(0, 5)]
        y = random.randint(2018, 2019)
        m = random.randint(1, 12)
        if m in [11, 4, 6, 9]:
            last_day = 30
        elif m == 2:
            last_day = 28
        else:
            last_day = 31
        d = random.randint(1, last_day)
        h = random.randint(7, 22)
        min = random.randint(0, 59)
        sec = random.randint(0, 59)
        time = datetime.datetime(y, m, d, h, min, sec)
        age = random.randint(16, 45)
        genders = ['M', 'F']
        sex = genders[random.randint(0,1)]

        log = Log(card_id=card_id, log_datetime=time, sex=sex, age=age, photo='5.jpg')
        log.save()
