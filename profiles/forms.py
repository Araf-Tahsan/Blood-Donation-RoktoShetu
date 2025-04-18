from django import forms
from .models import UserProfile

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['blood_type', 'weight', 'medical_conditions', 'last_donation_date','profile_picture'] 