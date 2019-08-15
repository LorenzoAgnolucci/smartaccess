from django import forms
from django.utils import timezone
import datetime

from .models import RFIDCard


class WriteCardForm(forms.ModelForm):

    def clean(self):
        # To keep the main validation and error messages
        cleaned_data = super(WriteCardForm, self).clean()

        card_id = self.cleaned_data['card_id']
        if not RFIDCard.objects.filter(pk=card_id).exists():
            self.add_error('card_id', "Card not registered, please add it to the database first")

        if cleaned_data['remaining_accesses'] < 0:
            self.add_error('remaining_accesses', "Value must be greater or equal than 0")

        if cleaned_data['expiration_date'] < datetime.date.today():
            self.add_error('expiration_date', "Date can't be in the past")

        return cleaned_data

    class Meta:
        model = RFIDCard
        fields = ["card_id", "remaining_accesses", "expiration_date"]
        widgets = {
            "card_id": forms.TextInput(attrs={'readonly': True, 'blank': True}),
            "expiration_date": forms.DateInput(attrs={'class': 'datepicker', 'id': 'datepicker'})
        }
        help_texts = {
            "remaining_accesses": "0 won't change the number of remaining accesses",
            "expiration_date" : "Today's date won't change the expiration date"
        }
        labels = {
            "remaining_accesses": "Accesses to add"
        }

# TODO change behaviour of form: from 'new remaining accesses number' to 'accesses increment'
#  e.g. remaining_accesses==2, type '10' in the form and new_remaining_accesses==12
