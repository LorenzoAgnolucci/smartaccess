from django import forms
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
        super(WriteCardForm, self).clean()

        card_id = self.cleaned_data['card_id']
        if not RFIDCard.objects.filter(pk=card_id).exists():
            # self._errors['card_id'] = 'Card not registered'
            raise forms.ValidationError('Card not registered, please add it to the database first')

    class Meta:
        model = RFIDCard
        fields = ["card_id", "remaining_accesses", "expiration_date"]
        widgets = {
            "card_id": forms.TextInput(attrs={'readonly': False, 'blank': True}),
            "expiration_date": forms.DateInput(attrs={'class': 'datepicker', 'id': 'datepicker'})
        }

# TODO add validators
# TODO change behaviour of form: from 'new remaining accesses number' to 'accesses increment'
#  e.g. remaining_accesses==2, type '10' in the form and new_remaining_accesses==12
# TODO revert to readonly mode
