from django import forms
from .models import EmergencyBloodRequest, Comment

class EmergencyBloodRequestForm(forms.ModelForm):
    class Meta:
        model = EmergencyBloodRequest
        fields = [
            'blood_type', 'quantity', 'needed_by', 'reason',
            'description', 'image', 'contact', 'location', 'hospital_name'
        ]
        widgets = {
            'needed_by': forms.DateInput(attrs={'type': 'date'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
