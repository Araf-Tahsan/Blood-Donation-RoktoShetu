from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import ProfileUpdateForm

@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)  # Ensures a profile exists
    return render(request, 'profile.html', {'profile': profile})

# @login_required
# def update_profile(request):
#     profile, created = UserProfile.objects.get_or_create(user=request.user)
#     if request.method == "POST":
#         form = ProfileUpdateForm(request.POST, instance=profile)
#         if form.is_valid():
#             form.save()
#             return redirect('profile')  # Ensure 'profile' is a valid URL name
#     else:
#         form = ProfileUpdateForm(instance=profile)
#     return render(request, 'update_profile.html', {'form': form}) 
@login_required
def update_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)  # <-- ADD request.FILES
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=profile)
    return render(request, 'update_profile.html', {'form': form})

