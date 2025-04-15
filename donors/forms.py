from django import forms
from .models import Donor

class DonorForm(forms.ModelForm):
    class Meta:
        model = Donor
        exclude = ['user']
        widgets = {
            'last_donation_date': forms.DateInput(attrs={'type': 'date'}),
        }
