from django import forms
from smart_formApp.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

        
        labels = {
            'first_name': '',
            'last_name': '',
            'emai': '',
            
        }

        widgets = {

        'first_name': forms.TextInput(
            attrs={'class': "form-control", 'placeholder': 'First Name', 'id': 'first-name'}),

        'last_name': forms.TextInput(
            attrs={'class': "form-control", 'placeholder': 'Last Name', 'id': 'last-name'}),
        
        'email': forms.TextInput(
            attrs={'class': "form-control", 'placeholder': 'Email Address', 'id': 'email'}),
        
        
    }
