from django.db import models
from django.contrib.auth.models import User

class EmergencyBloodRequest(models.Model):
    BLOOD_TYPES = [
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blood_type = models.CharField(max_length=5, choices=BLOOD_TYPES)
    quantity = models.IntegerField(help_text="Enter the required blood quantity in units.")
    needed_by = models.DateField(help_text="Date when blood is needed.")
    reason = models.CharField(max_length=255, help_text="Reason for emergency blood need.")
    description = models.TextField()
    image = models.ImageField(upload_to='emergency_images/', blank=True, null=True)
    contact = models.CharField(max_length=15, help_text="Contact number for further communication.")
    location = models.CharField(max_length=255, help_text="Location where blood is needed.")
    hospital_name = models.CharField(max_length=255, help_text="Name of the hospital.")
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.blood_type} ({self.quantity} units)"

class Comment(models.Model):
    request = models.ForeignKey(EmergencyBloodRequest, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.request}"
