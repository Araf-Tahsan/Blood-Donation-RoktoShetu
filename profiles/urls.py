from django.urls import path
from .views import profile_view, update_profile

urlpatterns = [
    path('', profile_view, name='profile'),  # Profile page
    path('update/', update_profile, name='update_profile'),  # Update page
]
