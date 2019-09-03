from django.forms import Form
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.utils import timezone
from django.views.generic import TemplateView
from .models import RFIDCard, Log
from .forms import WriteCardForm
# import mfrc522
# from RPLCD import CharLCD
import datetime
import json
import RPi.GPIO as GPIO

from rfid.programs import face_detect, RFIDSingleton
from rfid.programs.RFIDSingleton import RFIDSingleton


def clear_session_var(request):
    try:
        request.session.pop('card_id')
    except KeyError:
        pass


class IndexView(TemplateView):
    template_name = 'rfid/index.html'

    def setup(self, request, *args, **kwargs):
        # Delete cache before new operations
        clear_session_var(request)

        return super().setup(request, *args, **kwargs)


class AddCardScanView(TemplateView):
    template_name = 'rfid/add_card_scan.html'


class WriteCardScanView(TemplateView):
    template_name = 'rfid/write_card_scan.html'


class InfoCardScanView(TemplateView):
    template_name = 'rfid/info_card_scan.html'


class DeleteCardScanView(TemplateView):
    template_name = 'rfid/delete_card_scan.html'


# Displays the page waiting for the card, which redirect to the access view
class AccessMainView(TemplateView):
    template_name = 'rfid/access_main.html'


class AboutView(TemplateView):
    template_name = 'rfid/about.html'


def add_card(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You must authenticate before adding a card', extra_tags='alert-danger')
        return redirect('%s?next=%s' % (reverse('login'), reverse('rfid:add_card_scan')))

    try:
        card_id = request.session.pop('card_id')
    except KeyError:
        reader = RFIDSingleton()
        reader.set_reading(True)
        card_id = reader.read_id()
        reader.set_reading(False)
        # card_id = input('Type card id')

    if RFIDCard.objects.filter(card_id=card_id).exists():
        return render(request, 'rfid/add_card_fail.html', context={'card_id': card_id})

    new_card = RFIDCard(card_id=card_id)
    new_card.save()
    request.session['card_id'] = card_id
    return render(request, 'rfid/add_card_success.html', context={'card_id': card_id})


def write_card(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You must authenticate before writing on a card', extra_tags='alert-danger')
        return redirect('%s?next=%s' % (reverse('login'), reverse('rfid:write_card_scan')))
    # messages.info(request, 'Scan the card you want to write on')

    # check if the card has been scanned before
    try:
        card_id = request.session.pop('card_id')
    except KeyError:
        reader = RFIDSingleton()
        reader.set_reading(True)
        card_id = reader.read_id()
        reader.set_reading(False)
        # TODO remember to revert to read_id() function
        # card_id = '5279589593186'
        # card_id = input('Type card id')

    try:
        card = RFIDCard.objects.get(pk=card_id)
        old_remaining_accesses = card.remaining_accesses
        old_expiration_date = card.expiration_date

        if request.method == 'POST':
            # RFIDCard model bound form
            form = WriteCardForm(request.POST, instance=card, initial={"expiration_date": card.expiration_date})
            if form.is_valid():
                # Validation is done at form level in the clean() method override

                card.remaining_accesses += old_remaining_accesses
                if form.cleaned_data["expiration_date"] > old_expiration_date:
                    card.expiration_date = form.cleaned_data["expiration_date"]
                else:
                    card.expiration_date = old_expiration_date
                card.save()

                return render(request, 'rfid/write_card_success.html', context={'card_id': card_id,
                                                                                'remaining_accesses': card.remaining_accesses,
                                                                                'expiration_date': card.expiration_date})
        else:
            # unbound form
            form = WriteCardForm(initial={'card_id': card_id,
                                          'expiration_date': card.expiration_date})

        request.session['card_id'] = card_id
        return render(request, 'rfid/write_card.html', {'form': form})

    except RFIDCard.DoesNotExist:
        request.session['card_id'] = card_id
        return render(request, 'rfid/write_card_add_new.html', context={'card_id': card_id})


def info_card(request):
    reader = RFIDSingleton()
    reader.set_reading(True)
    card_id = reader.read_id()
    reader.set_reading(False)
    # card_id = input('Type card id')
    if RFIDCard.objects.filter(card_id=card_id).exists():
        card = RFIDCard.objects.get(card_id=card_id)
        context = {'card_id': card.card_id,
                   'remaining_accesses': card.remaining_accesses,
                   'expiration_date': card.expiration_date}
    else:
        context = {'card_id': card_id}
        messages.warning(request, 'Your card is not registered', extra_tags='alert-warning')
    return render(request, 'rfid/info_card.html', context=context)


def delete_card(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You must authenticate before deleting a card', extra_tags='alert-danger')
        return redirect('%s?next=%s' % (reverse('login'), reverse('rfid:delete_card_scan')))

    try:
        card_id = request.session.pop('card_id')
    except KeyError:
        reader = RFIDSingleton()
        reader.set_reading(True)
        card_id = reader.read_id()
        reader.set_reading(False)
        # TODO remember to revert to read_id() function
        # card_id = '5279589593186'
        # card_id = input('Type card id')

    if RFIDCard.objects.filter(card_id=card_id).exists():
        card = RFIDCard.objects.get(card_id=card_id)
        form = Form()
        context = {'card_id': card.card_id,
                   'remaining_accesses': card.remaining_accesses,
                   'expiration_date': card.expiration_date,
                   'form': form}
        # FIXME redirected to delete_card after submit
        if request.method == 'POST':
            card.delete()
            messages.success(request, 'The card {} has been deleted'.format(card_id), extra_tags='alert-success')
            return render(request, 'rfid/delete_card_scan.html', context=context)
        else:
            request.session['card_id'] = card_id
            return render(request, 'rfid/delete_card.html', context=context)
    else:
        context = {'card_id': card_id}
        messages.warning(request, 'Your card is not registered', extra_tags='alert-warning')
        return render(request, 'rfid/delete_card_scan.html', context=context)


# card_id is eventually passed from the URL (see rfid/urls.py)
def access_result(request, card_id=None):

    if card_id is None:
        try:
            reader = RFIDSingleton()
            reader.set_reading(True)
            card_id = reader.read_id()
            reader.set_reading(False)
        except:
            print("Exception")
        # card_id = input('Type card id')
    # lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[40, 38, 36, 32, 33, 31, 29, 23])
    # lcd.write_string(u'Scan your card')
    try:
        if RFIDCard.objects.get(card_id=card_id):
            card = RFIDCard.objects.get(card_id=card_id)
            if card.remaining_accesses > 0 and card.expiration_date >= datetime.date.today():
                card.remaining_accesses -= 1
                GPIO.output(18, GPIO.HIGH)

                # log_data = face_detect.get_photo_data(Log.objects.latest('id').id+1)
                # log_data['card'] = card
                # log_data['log_datetime'] = timezone.now()

                # TODO Code to add when you want to take a photo with the Raspberry (Part 1)
                new_log = Log(card=card, log_datetime=timezone.datetime.now())

                # new_log = Log(**log_data)
                card.save()
                new_log.save()

                # TODO Code to add when you want to take a photo with the Raspberry (Part 2)
                # new_log is saved two times because before the first save it does not have id needed by get_photo_data

                new_log = Log.objects.latest("id")
                GPIO.output(26, GPIO.HIGH)
                data = face_detect.get_photo_data(new_log.id)
                GPIO.output(26, GPIO.LOW)
                new_log.age = data["age"]
                new_log.sex = data["sex"]
                new_log.photo = data["photo"]
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
                GPIO.output(17, GPIO.HIGH)
                message = 'No accesses'
                description = 'You have no more accesses remained. ' \
                              'Please recharge your card at the reception'
                # lcd.write_string(u'No accesses\n\rPlease recharge')
                # time.sleep(3)
                # lcd.clear()
            else:
                GPIO.output(17, GPIO.HIGH)
                message = 'Card expired'
                description = 'We\'re sorry, your last {} accesses expired on {}, ' \
                              'please buy new accesses at the reception'.format(card.remaining_accesses,
                                                                                card.expiration_date)
                # lcd.write_string(u'Card expired')
                # time.sleep(3)
                # lcd.clear()
    except RFIDCard.DoesNotExist:
        GPIO.output(17, GPIO.HIGH)
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


def dashboard(request):
    clear_session_var(request)

    data = [[str(x.log_datetime.date().strftime('%A')), x.log_datetime.hour, x.sex, x.age] for x in Log.objects.all()]
    data.insert(0, ["Day", "Hour", "Sex", "Age"])
    return render(request, 'rfid/dashboard.html', context={'array': json.dumps(data)})


def logs(request):
    clear_session_var(request)

    if not request.user.is_authenticated:
        messages.error(request, 'Logs page contains private data, you must authenticate before accessing the logs', extra_tags='alert-danger')
        return redirect('%s?next=%s' % (reverse('login'), reverse('rfid:logs')))

    data = Log.objects.all()
    return render(request, 'rfid/logs.html', context={'data': data})

# FIXME if you change url during scanning the input continues to read in background
