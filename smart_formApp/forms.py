from django import forms
from smart_formApp.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'subscribe_to_newsletter']

        labels = {
            'first_name': '',
            'last_name': '',
            'email': '',
            'subscribe_to_newsletter': 'Select to receive promotional emails and be added to our newsletter',
        }

        widgets = {
            'first_name': forms.TextInput(
                attrs={'class': "form-control", 'placeholder': 'First Name', 'id': 'first-name'}),
            'last_name': forms.TextInput(
                attrs={'class': "form-control", 'placeholder': 'Last Name', 'id': 'last-name'}),
            'email': forms.TextInput(
                attrs={'class': "form-control", 'placeholder': 'Email Address', 'id': 'email'}),
            'subscribe_to_newsletter': forms.CheckboxInput(
                attrs={'class': 'form-check-input', 'id': 'subscribe-to-newsletter'}),
        }


