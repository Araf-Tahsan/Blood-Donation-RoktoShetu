from django.urls import path
from . import views

urlpatterns = [
    path('join/', views.join_as_donor, name='join_as_donor'),
    path('list/', views.donor_list, name='donor_list'),
]
