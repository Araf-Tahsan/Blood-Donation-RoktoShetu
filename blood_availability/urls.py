from django.urls import path
from .views import blood_list

urlpatterns = [
    path('blood_availability/', blood_list, name='blood_list'),
]
