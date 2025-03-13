from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['user', 'email', 'membership_number', 'active_membership', 'date', 'slot', 'name']
