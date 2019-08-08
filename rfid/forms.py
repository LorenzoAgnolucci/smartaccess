from django import forms
from .models import RFIDCard


class WriteCardForm(forms.ModelForm):
    class Meta:
        model = RFIDCard
        fields = ["card_id", "remaining_accesses", "expiration_date"]
        widgets = {
            "card_id": forms.TextInput(attrs={'readonly': True, 'blank': True}),
            "expiration_date": forms.DateInput(attrs={'class': 'datepicker', 'id': 'datepicker'})
        }
