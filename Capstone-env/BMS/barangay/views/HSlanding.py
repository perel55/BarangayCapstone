from .models import HealthService, Services
from django.shortcuts import render

def residentHS(request): 
    healthService = HealthService.objects.all()
    return render(request, 'resident/HSlandingpage.html', {'healthService': healthService}) 

def residentAS(request): 
    adminService = Services.objects.all()
    return render(request, 'resident/ASlandingpage.html', {'adminService': adminService}) 