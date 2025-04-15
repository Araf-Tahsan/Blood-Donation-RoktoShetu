from django.shortcuts import render, redirect
from .forms import DonorForm
from .models import Donor
from django.contrib.auth.decorators import login_required

@login_required
def join_as_donor(request):
    if hasattr(request.user, 'donor'):
        return redirect('donor_list')

    if request.method == 'POST':
        form = DonorForm(request.POST, request.FILES)
        if form.is_valid():
            donor = form.save(commit=False)
            donor.user = request.user
            donor.save()
            return redirect('donor_list')
    else:
        form = DonorForm()

    return render(request, 'join_as_donor.html', {'form': form})


from django.http import JsonResponse

# donors/choices.py

DIVISION_DISTRICT_MAP = {
    'Dhaka': [
        'Dhaka', 'Gazipur', 'Kishoreganj', 'Manikganj', 'Munshiganj',
        'Narayanganj', 'Narsingdi', 'Rajbari', 'Shariatpur', 'Tangail',
        'Faridpur', 'Gopalganj', 'Madaripur'
    ],
    'Chattogram': [
        'Chattogram', 'Cox’s Bazar', 'Cumilla', 'Brahmanbaria', 'Chandpur',
        'Feni', 'Lakshmipur', 'Noakhali', 'Khagrachari', 'Rangamati', 'Bandarban'
    ],
    'Rajshahi': [
        'Rajshahi', 'Pabna', 'Natore', 'Naogaon', 'Joypurhat', 'Chapai Nawabganj',
        'Bogura', 'Sirajganj'
    ],
    'Khulna': [
        'Khulna', 'Bagerhat', 'Chuadanga', 'Jashore', 'Jhenaidah', 'Kushtia',
        'Magura', 'Meherpur', 'Narail', 'Satkhira'
    ],
    'Barisal': [
        'Barisal', 'Barguna', 'Bhola', 'Jhalokathi', 'Patuakhali', 'Pirojpur'
    ],
    'Sylhet': [
        'Sylhet', 'Habiganj', 'Moulvibazar', 'Sunamganj'
    ],
    'Mymensingh': [
        'Mymensingh', 'Netrokona', 'Sherpur', 'Jamalpur'
    ],
    'Rangpur': [
        'Rangpur', 'Dinajpur', 'Gaibandha', 'Kurigram', 'Lalmonirhat',
        'Nilphamari', 'Panchagarh', 'Thakurgaon'
    ]
}

DIVISION_CHOICES = [(key, key) for key in DIVISION_DISTRICT_MAP.keys()]

from .models import Donor, DIVISIONS, DISTRICTS, BLOOD_TYPES

def donor_list(request):
    donors = Donor.objects.all()

    division = request.GET.get('division')
    district = request.GET.get('district')
    blood_type = request.GET.get('blood_type')

    if division:
        donors = donors.filter(division=division)
    if district:
        donors = donors.filter(district=district)
    if blood_type:
        donors = donors.filter(blood_type=blood_type)

    return render(request, 'donor_list.html', {
        'donors': donors,
        'divisions': DIVISIONS,
        'districts': DISTRICTS,
        'blood_types': BLOOD_TYPES,
    })

# def donor_list(request):
#     donors = Donor.objects.all()

#     division = request.GET.get('division')
#     district = request.GET.get('district')
#     blood_type = request.GET.get('blood_type')

#     if division:
#         donors = donors.filter(division=division)
#     if district:
#         donors = donors.filter(district=district)
#     if blood_type:
#         donors = donors.filter(blood_type=blood_type)

#     return render(request, 'donor_list.html', {
#         'donors': donors,
#         'divisions': DIVISION_DISTRICT_MAP.keys(),
#         'district_map': DIVISION_DISTRICT_MAP,
#         'blood_types': Donor._meta.get_field('blood_type').choices,
#     })
