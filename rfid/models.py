from django.db import models
from django.utils import timezone


# The primary-key is the card id
class RFIDCard(models.Model):
    card_id = models.IntegerField(primary_key=True)
    remaining_accesses = models.IntegerField(default=0)
    expiration_date = models.DateField(default=timezone.datetime.now)

    def __str__(self):
        return "Id: {}, remaining accesses: {}, expiration date: {}".format(self.card_id, self.remaining_accesses,
                                                                            self.expiration_date)


class Log(models.Model):
    id = models.AutoField(primary_key=True)
    card = models.ForeignKey(RFIDCard, on_delete=models.CASCADE, null=True)
    photo = models.ImageField(upload_to="{}.jpg".format(id), null=True)
    log_datetime = models.DateTimeField(default=timezone.datetime.now)
    age = models.IntegerField(null=True)
    sex = models.CharField(max_length=1, choices=(('M', 'Male'), ('F', 'Female')), null=True)

    def __str__(self):
        return 'Id: {}, card: {}, time: {}'.format(self.id, self.card, self.log_datetime)

