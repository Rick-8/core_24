from django import forms
from django.forms import ModelForm
from .models import Booking, Profile


class DateInput(forms.DateInput):
    input_type = 'date'


class BookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = ['date']
        widgets = {'date': DateInput()}


class ProfileForm(forms.ModelForm):
    """
    Form for creating or updating a user's profile, including fields for
    personal details such as email, address, and phone numbers.
    """

    class Meta:
        model = Profile
        fields = [
            'email', 'membership_number', 'personal_address',
            'phone_number_1', 'phone_number_2'
        ]
        widgets = {
            'email': forms.TextInput(attrs={
                'placeholder': 'Enter your email', 'class': 'form-control'
            }),
            'membership_number': forms.TextInput(attrs={
                'readonly': 'readonly', 'class': 'form-control'
            }),
            'personal_address': forms.Textarea(attrs={
                'placeholder': 'Enter your address', 'class': 'form-control',
                'rows': 4
            }),
            'phone_number_1': forms.TextInput(attrs={
                'placeholder': 'Enter primary phone number',
                'class': 'form-control'
            }),
            'phone_number_2': forms.TextInput(attrs={
                'placeholder': 'Enter secondary phone number',
                'class': 'form-control'
            }),
        }
