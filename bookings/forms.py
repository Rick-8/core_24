from django import forms
from django.forms import ModelForm
from .models import Booking


# Custom DateInput widget for HTML5 date picker
class DateInput(forms.DateInput):
    input_type = 'date'


class BookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = ['date']  # Only include the date field
        widgets = {
            'date': DateInput(),  # Use HTML5 date picker
        }
