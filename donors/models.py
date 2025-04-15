from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

DIVISIONS = [
    ('Dhaka', 'Dhaka'),
    ('Chattogram', 'Chattogram'),
    ('Rajshahi', 'Rajshahi'),
    ('Khulna', 'Khulna'),
    ('Barisal', 'Barisal'),
    ('Sylhet', 'Sylhet'),
    ('Rangpur', 'Rangpur'),
    ('Mymensingh', 'Mymensingh'),
]

DISTRICTS = [
    ('Bagerhat', 'Bagerhat'), ('Bandarban', 'Bandarban'), ('Barguna', 'Barguna'),
    ('Barisal', 'Barisal'), ('Bhola', 'Bhola'), ('Bogura', 'Bogura'),
    ('Brahmanbaria', 'Brahmanbaria'), ('Chandpur', 'Chandpur'), ('Chapai Nawabganj', 'Chapai Nawabganj'),
    ('Chattogram', 'Chattogram'), ('Chuadanga', 'Chuadanga'), ('Comilla', 'Comilla'),
    ('Cox\'s Bazar', 'Cox\'s Bazar'), ('Dhaka', 'Dhaka'), ('Dinajpur', 'Dinajpur'),
    ('Faridpur', 'Faridpur'), ('Feni', 'Feni'), ('Gaibandha', 'Gaibandha'),
    ('Gazipur', 'Gazipur'), ('Gopalganj', 'Gopalganj'), ('Habiganj', 'Habiganj'),
    ('Jamalpur', 'Jamalpur'), ('Jashore', 'Jashore'), ('Jhalokathi', 'Jhalokathi'),
    ('Jhenaidah', 'Jhenaidah'), ('Joypurhat', 'Joypurhat'), ('Khagrachari', 'Khagrachari'),
    ('Khulna', 'Khulna'), ('Kishoreganj', 'Kishoreganj'), ('Kurigram', 'Kurigram'),
    ('Kushtia', 'Kushtia'), ('Lakshmipur', 'Lakshmipur'), ('Lalmonirhat', 'Lalmonirhat'),
    ('Madaripur', 'Madaripur'), ('Magura', 'Magura'), ('Manikganj', 'Manikganj'),
    ('Meherpur', 'Meherpur'), ('Moulvibazar', 'Moulvibazar'), ('Munshiganj', 'Munshiganj'),
    ('Mymensingh', 'Mymensingh'), ('Naogaon', 'Naogaon'), ('Narail', 'Narail'),
    ('Narayanganj', 'Narayanganj'), ('Narsingdi', 'Narsingdi'), ('Natore', 'Natore'),
    ('Netrokona', 'Netrokona'), ('Nilphamari', 'Nilphamari'), ('Noakhali', 'Noakhali'),
    ('Pabna', 'Pabna'), ('Panchagarh', 'Panchagarh'), ('Patuakhali', 'Patuakhali'),
    ('Pirojpur', 'Pirojpur'), ('Rajbari', 'Rajbari'), ('Rajshahi', 'Rajshahi'),
    ('Rangamati', 'Rangamati'), ('Rangpur', 'Rangpur'), ('Satkhira', 'Satkhira'),
    ('Shariatpur', 'Shariatpur'), ('Sherpur', 'Sherpur'), ('Sirajganj', 'Sirajganj'),
    ('Sunamganj', 'Sunamganj'), ('Sylhet', 'Sylhet'), ('Tangail', 'Tangail'),
    ('Thakurgaon', 'Thakurgaon')
]


BLOOD_TYPES = [
    ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
    ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-'),
]

class Donor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    division = models.CharField(max_length=100, choices=DIVISIONS)
    district = models.CharField(max_length=100, choices=DISTRICTS)
    blood_type = models.CharField(max_length=5, choices=BLOOD_TYPES)
    last_donation_date = models.DateField()
    profile_picture = models.ImageField(upload_to='donors/', blank=True, null=True)

    def is_available(self):
        return (timezone.now().date() - self.last_donation_date).days >= 90

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
