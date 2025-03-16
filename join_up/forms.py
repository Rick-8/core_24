from django import forms
from .models import Customer


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone_number_1', 'phone_number_2']
        widgets = {
            'name': forms.TextInput(
                attrs={'type': 'text', 'placeholder': 'Name'}),
            'email': forms.TextInput(
                attrs={'type': 'email', 'placeholder': 'Email'}),
            'phone_number_1': forms.TextInput(
                attrs={'type': 'tel', 'placeholder': 'Phone Number 1'}),
            'phone_number_2': forms.TextInput(
                attrs={'type': 'tel', 'placeholder': 'Phone Number 2 (optional)'}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError("Name is required!")
        return name
