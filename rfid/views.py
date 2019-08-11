import time

from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.utils import timezone
from django.views.generic import TemplateView
from .models import RFIDCard, Log
from .forms import WriteCardForm
# import mfrc522
# from RPLCD import CharLCD
import datetime
import random


class IndexView(TemplateView):
    template_name = 'rfid/index.html'


# class AddCardView(TemplateView):
#     template_name = "rfid/add_card.html"
#

def add_card(request):
    # reader = mfrc522.SimpleMFRC522()
    # card_id = reader.read_id()
    card_id = random.randint(10e11, 10e12)
    if RFIDCard.objects.filter(card_id=card_id).exists():
        return HttpResponse('The card is already in the database')
    new_card = RFIDCard(card_id=card_id, remaining_accesses=0, expiration_date=datetime.datetime.today())
    new_card.save()
    return HttpResponse('Added card {}'.format(card_id))


def write_card(request):
    messages.info(request, 'Scan the card you want to write on')
    # reader = mfrc522.SimpleMFRC522()
    # card_id = reader.read_id()
    # TODO remember to revert to read_id() function
    card_id = '5279589593186'
    if request.method == 'POST':
        try:
            # card must be scanned
            # TODO check condition forks
            f = WriteCardForm(request.POST)
            if f.is_valid():
                remaining_accesses = f.cleaned_data['remaining_accesses']
                expiration_date = f.cleaned_data['expiration_date']
                if remaining_accesses < 0:
                    messages.error(request, 'Remaining accesses must be greater than 0')
                    return render(request, 'rfid/index.html')
                if expiration_date <= datetime.date.today():
                    messages.error(request, 'New expiration date must be in the future')
                    return render(request, 'rfid/index.html')
                f.save()
            else:
                args = {'form': f}
                return render(request, 'rfid/write_card.html', args)

        except RFIDCard.DoesNotExist:
            messages.error(request, 'You have to add the card to the database before writing on it')
            return render(request, 'rfid/index.html')
        # return render(request, 'rfid/index.html', {'error_message': "You have to add the card to the database "
        #                                                             "before writing on it"})
        messages.success(request, 'Written on card')
        # return render(request, 'rfid/index.html')
        return HttpResponseRedirect(reverse('rfid:index'))

    else:
        f = WriteCardForm(initial={'card_id': card_id})
    return render(request, 'rfid/write_card.html', {'form': f})


def get_photo_data():
    # TODO shoot the photo, send it to Azure face or IBM watson, return crop, age and sex as a dict
    return {'photo': None, 'age': 27, 'sex': 'M'}


# Displays the page waiting for the card, which redirect to the access view
class AccessMainView(TemplateView):
    template_name = 'rfid/access_main.html'


def access_result(request, card_id=None):
    # reader = mfrc522.SimpleMFRC522()
    # card_id = reader.read_id()
    if card_id is None:
        card_id = input('Type card id')
    # lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[40, 38, 36, 32, 33, 31, 29, 23])
    # lcd.write_string(u'Scan your card')
    try:
        if RFIDCard.objects.get(card_id=card_id):
            card = RFIDCard.objects.get(card_id=card_id)
            if card.remaining_accesses > 0 and card.expiration_date >= datetime.date.today():
                card.remaining_accesses -= 1
                log_data = get_photo_data()
                log_data['card'] = card
                log_data['log_datetime'] = timezone.now()

                new_log = Log(**log_data)

                card.save()
                new_log.save()
                message = 'Welcome!'
                description = 'You have {} accesses left. ' \
                              'The card will expire on {}'.format(card.remaining_accesses,
                                                                  card.expiration_date)
                # TODO implement printing messages on LCD display and red/green led
                #  see http://www.circuitbasics.com/raspberry-pi-lcd-set-up-and-programming-in-python/
                # lcd.write_string(u'Welcome\n\r{} remaining'.format(card.remaining_accesses))
                # time.sleep(3)
                # lcd.clear()
            elif card.remaining_accesses == 0:
                message = 'No accesses'
                description = 'You have no more accesses remained. ' \
                              'Please recharge your card at the reception'
                # lcd.write_string(u'No accesses\n\rPlease recharge')
                # time.sleep(3)
                # lcd.clear()
            else:
                message = 'Card expired'
                description = 'We\'re sorry, your last {} accesses expired on {}, ' \
                              'please buy new accesses at the reception'.format(card.remaining_accesses,
                                                                                card.expiration_date)
                # lcd.write_string(u'Card expired')
                # time.sleep(3)
                # lcd.clear()
    except RFIDCard.DoesNotExist:
        message = 'Card not registered'
        description = 'It seems that we haven\'t registered this card. ' \
                      'Please ask for help at the reception'
        # lcd.write_string(u'Card not\n\rregistered')
        # time.sleep(3)
        # lcd.clear()
    return render(request, 'rfid/access_result.html', {
        'message': message,
        'description': description
    })

# FIXME: Alert vengono mostrati tutti dopo ogni reindirizzamento e dopo aver fatto scan della carta
# TODO change message display method, try using web pages redirect like in access_result view
#  (also using the message framework)
#  (forse perchè codice per messages è sia in index.html che in write_card.html)
#  controllare come cancellare vecchi messaggi
# TODO: Capire per bene come fare reindirizzamenti dopo POST per non fare submit due volte se si ricarica la pagina