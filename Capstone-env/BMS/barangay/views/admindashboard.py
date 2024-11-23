from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login as auth_login
from django.contrib import messages
from .models import *
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView


def admindashboard(request):
    return render(request, 'admin/admin.html')

def service_list(request):
    services = Services.objects.all()
    return render(request, 'admin/ServiceList.html', {'services': services})

def AddService(request):
    if request.method == "POST":
        service_name = request.POST.get('service_name')
        requirements = request.POST.get('requirements')
        service_description = request.POST.get('service_description')
        service_price = request.POST.get('service_price')

        image = request.FILES.get('image')

        new_service = Services(
            service_name=service_name,
            requirements=requirements,
            service_description=service_description,
            service_price=service_price,
            image=image,
        )
        new_service.save()

        return redirect('service_list')

    return render(request, 'modal/AddServices.html')

def update_service(request, service_id):
    service = get_object_or_404(Services, service_id=service_id)

    if request.method == "POST":
        service.service_name = request.POST.get('service_name')
        service.requirements = request.POST.get('requirements')
        service.service_description = request.POST.get('service_description')
        service.service_price = request.POST.get('service_price')

        if request.FILES.get('image'):
            service.image = request.FILES['image']

        service.save()
        return redirect('service_list')

    return render(request, 'admin/update_service.html', {'service': service})


def delete_service(request, service_id):
    service = get_object_or_404(Services, service_id=service_id)
    service.delete()
    return redirect('service_list')

def administrative_services_list(request):
    services = Services.objects.all()
    return render(request, 'admin/administrative_services_list.html', {'services': services})

def health_services_list(request):
    health_services = HealthService.objects.all()
    return render(request, 'admin/health_services_list.html', {'health_services': health_services})

def account_list(request):
    account_type = request.GET.get('type', 'all')  # Default to 'all'
    
    if account_type == 'Residents':
        accounts = Residents.objects.all()
    elif account_type == 'Bhw':
        accounts = Bhw.objects.all()
    elif account_type == 'Personnel':
        accounts = Personnel.objects.all()
    else:
        accounts = Accounts.objects.all()  # Shows all accounts if 'all' is selected

    context = {
        'accounts': accounts,
        'account_type': account_type,
    }
    return render(request, 'admin/adminAccounts.html', context)
