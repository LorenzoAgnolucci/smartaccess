from django.db import models
import datetime
from django.utils import timezone


# TODO switch to django timezone lib


class RFIDCard(models.Model):
    card_id = models.IntegerField()
    remaining_accesses = models.IntegerField(default=0)
    expiration_date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return "Id: {}, remaining accesses: {}, expiration date: {}".format(self.card_id, self.remaining_accesses,
                                                                            self.expiration_date)


class Log(models.Model):
    id = models.AutoField(primary_key=True)
    card_id = models.ForeignKey(RFIDCard, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="{}.jpg".format(id))
    log_datetime = models.DateTimeField(default=datetime.datetime.now)
    age = models.IntegerField()
    sex = models.CharField(max_length=1, choices=(('M', 'Male'), ('F', 'Female')))

# TODO: Controllare se id come Autofield funziona
# FIXME: Capire per bene come fare store di immagini. Decidere se cancellare Log se si cancella card (ammesso che si possa cancellare una card)
