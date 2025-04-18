from django.shortcuts import render
from .models import BloodStock

def blood_list(request):
    blood_data = BloodStock.objects.all()
    return render(request, 'blood_list.html', {'blood_data': blood_data})


# from django.shortcuts import render
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from .models import BloodStock
# from django.db.models import Q

# def blood_stock(request):
#     # Get query parameters
#     blood_group = request.GET.get('blood_group', '')
#     facility = request.GET.get('facility', '')
#     component = request.GET.get('component', '')
    
#     # Base queryset
#     queryset = BloodStock.objects.all().order_by('-last_updated')
    
#     # Apply filters if provided
#     if blood_group:
#         queryset = queryset.filter(blood_group=blood_group)
#     if facility:
#         queryset = queryset.filter(facility_name__icontains=facility)
#     if component:
#         queryset = queryset.filter(component=component)
    
#     # Pagination
#     page = request.GET.get('page', 1)
#     paginator = Paginator(queryset, 10)  # Show 10 records per page
    
#     try:
#         blood_stocks = paginator.page(page)
#     except PageNotAnInteger:
#         blood_stocks = paginator.page(1)
#     except EmptyPage:
#         blood_stocks = paginator.page(paginator.num_pages)
    
#     context = {
#         'blood_stocks': blood_stocks,
#     }
    
#     return render(request, 'blood_stock.html', context)