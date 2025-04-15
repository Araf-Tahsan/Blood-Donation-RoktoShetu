from django.urls import path
from .views import (
    emergency_request_list,
    create_emergency_request,
    request_detail,
    update_emergency_request,
    delete_emergency_request
)

urlpatterns = [
    path('', emergency_request_list, name='emergency_request_list'),
    path('create/', create_emergency_request, name='create_emergency_request'),
    path('<int:request_id>/', request_detail, name='request_detail'),
    path('<int:request_id>/update/', update_emergency_request, name='update_emergency_request'),
    path('<int:request_id>/delete/', delete_emergency_request, name='delete_emergency_request'),
]
