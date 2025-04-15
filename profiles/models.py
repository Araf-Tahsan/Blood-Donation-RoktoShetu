from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, date

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    blood_type = models.CharField(max_length=5, choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-'),])
    weight = models.FloatField(null=True, blank=True)
    medical_conditions = models.TextField(blank=True, null=True)
    last_donation_date = models.DateField(null=True, blank=True)

    def next_donation_date(self):
        """Calculates the next eligible blood donation date (assuming 3 months gap)."""
        if self.last_donation_date:
            return self.last_donation_date + timedelta(days=90)
        return None

    def __str__(self):
        return self.user.username
