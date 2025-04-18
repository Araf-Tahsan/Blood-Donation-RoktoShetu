from django.db import models

class BloodStock(models.Model):
    facility_name = models.CharField(max_length=255)
    blood_group = models.CharField(max_length=10)
    bag_number = models.CharField(max_length=50)
    component = models.CharField(max_length=100)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.facility_name} - {self.blood_group}"