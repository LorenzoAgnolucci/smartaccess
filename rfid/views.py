from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from .models import RFIDCard, Log
from .forms import WriteCardForm
# import mfrc522
import datetime
import random


def index(request):
    return render(request, "rfid/index.html")


def add_card(request):
    # reader = mfrc522.SimpleMFRC522()
    card_id = random.randint(10e11, 10e12)
    if RFIDCard.objects.filter(card_id=card_id).exists():
        return HttpResponse("The card is already in the database")
    new_card = RFIDCard(card_id=card_id, remaining_accesses=0, expiration_date=datetime.datetime.today())
    new_card.save()
    return HttpResponse("Added card {}".format(card_id))


def write_card(request):
    messages.info(request, "Scan the card you want to write on")
    # reader = mfrc522.SimpleMFRC522()
    # card_id = reader.read_id()
    # TODO remember to revert to read_id() function
    card_id = "6052484996928"
    if request.method == "POST":
        form = WriteCardForm(request.POST)
        if form.is_valid():
            card_id = form.cleaned_data["card_id"]
            try:
                card = RFIDCard.objects.get(card_id=card_id)
                remaining_accesses = form.cleaned_data["remaining_accesses"]
                expiration_date = form.cleaned_data["expiration_date"]
                if remaining_accesses != 0:
                    card.remaining_accesses = remaining_accesses
                elif expiration_date != datetime.date.today():
                    card.expiration_date = expiration_date
                card.save()
            except RFIDCard.DoesNotExist:
                messages.error(request, "You have to add the card to the database before writing on it")
                return render(request, "rfid/index.html")
            # return render(request, 'rfid/index.html', {'error_message': "You have to add the card to the database "
            #                                                             "before writing on it"})
            messages.success(request, "Written on card")
            # return render(request, "rfid/index.html")
            return HttpResponseRedirect(reverse('index'))

    else:
        form = WriteCardForm(initial={"card_id": card_id})
    return render(request, "rfid/write_card.html", {"form": form})

# FIXME: Dopo Submit non si viene reindirizzati a index (forse per posizione di read())
# FIXME: Alert vengono mostrati tutti dopo ogni reindirizzamento e dopo aver fatto scan della carta
#  (forse perchè codice per messages è sia in index.html che in write_card.html)
#   controllare come cancellare vecchi messaggi
# TODO: Capire per bene come fare reindirizzamenti dopo POST per non fare submit due volte se si ricarica la pagina
# TODO: Aggiungere una riga al database Log ogni volta che viene fatto qualcosa (forse solo quando si legge una scheda)
