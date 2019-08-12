from django import forms
from django.utils import timezone
import datetime

from .models import RFIDCard


class WriteCardForm(forms.ModelForm):

    # # FIXME clean method works. Try again with clean_card_id and find the best way to show the error
    # def clean_card_id(self):
    #     card_id = self.cleaned_data['card_id']
    #     if RFIDCard.objects.filter(pk=card_id) == []:
    #         raise forms.ValidationError('Card not registered, please add it to the database first')
    #     return card_id

    def clean(self):
        # To keep the main validation and error messages
        cleaned_data = super(WriteCardForm, self).clean()

        card_id = self.cleaned_data['card_id']
        if not RFIDCard.objects.filter(pk=card_id).exists():
            self.add_error('card_id', "Card not registered, please add it to the database first")

        if cleaned_data['remaining_accesses'] <= 0:
            self.add_error('remaining_accesses', "Value must be greater than 0")

        if cleaned_data['expiration_date'] <= datetime.date.today():
            self.add_error('expiration_date', "Date must be in the future")

        return cleaned_data

    class Meta:
        model = RFIDCard
        fields = ["card_id", "remaining_accesses", "expiration_date"]
        widgets = {
            "card_id": forms.TextInput(attrs={'readonly': True, 'blank': True}),
            "expiration_date": forms.DateInput(attrs={'class': 'datepicker', 'id': 'datepicker'})
        }

# TODO change behaviour of form: from 'new remaining accesses number' to 'accesses increment'
#  e.g. remaining_accesses==2, type '10' in the form and new_remaining_accesses==12
