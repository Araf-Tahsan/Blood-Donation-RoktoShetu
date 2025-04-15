from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import EmergencyBloodRequest, Comment
from .forms import EmergencyBloodRequestForm, CommentForm

@login_required
def emergency_request_list(request):
    requests = EmergencyBloodRequest.objects.all().order_by('-posted_at')
    return render(request, 'request_list.html', {'requests': requests})

@login_required
def create_emergency_request(request):
    if request.method == "POST":
        form = EmergencyBloodRequestForm(request.POST, request.FILES)
        if form.is_valid():
            blood_request = form.save(commit=False)
            blood_request.user = request.user
            blood_request.save()
            return redirect('emergency_request_list')
    else:
        form = EmergencyBloodRequestForm()
    return render(request, 'create_request.html', {'form': form})

@login_required
def request_detail(request, request_id):
    blood_request = get_object_or_404(EmergencyBloodRequest, id=request_id)
    comments = blood_request.comments.all()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.request = blood_request
            comment.save()
            return redirect('request_detail', request_id=request_id)
    else:
        form = CommentForm()
    return render(request, 'request_detail.html', {
        'blood_request': blood_request,
        'comments': comments,
        'form': form
    })

@login_required
def update_emergency_request(request, request_id):
    blood_request = get_object_or_404(EmergencyBloodRequest, id=request_id, user=request.user)
    
    if request.method == "POST":
        form = EmergencyBloodRequestForm(request.POST, request.FILES, instance=blood_request)
        if form.is_valid():
            form.save()
            messages.success(request, "Your emergency blood request has been updated.")
            return redirect('request_detail', request_id=request_id)
    else:
        form = EmergencyBloodRequestForm(instance=blood_request)
    
    return render(request, 'update_request.html', {'form': form, 'blood_request': blood_request})

@login_required
def delete_emergency_request(request, request_id):
    blood_request = get_object_or_404(EmergencyBloodRequest, id=request_id, user=request.user)

    if request.method == "POST":
        blood_request.delete()
        messages.success(request, "Your emergency blood request has been deleted.")
        return redirect('emergency_request_list')

    return render(request, 'delete_request.html', {'blood_request': blood_request})
