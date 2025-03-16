from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from bookings.models import ClosedDay


# staff_panel/forms.py
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff']


class ClosedDayForm(forms.ModelForm):
    class Meta:
        model = ClosedDay
        fields = ['date', 'reason']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
