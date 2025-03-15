from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# staff_panel/forms.py
class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff']
