from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login as auth_login
from django.shortcuts import render, reverse
from .models import Residents, Account_Type, Accounts
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views import View
from .models import HealthService
from django.contrib.auth.decorators import login_required
from .models import *
from django.db.models import Prefetch
from django.db.models import Sum


@csrf_exempt
def healthAdminreg(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password1 == password2:
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password1,
            )

            healthAdmin = HealthAdmin.objects.create(auth_user=user)  # Ensure the model name matches

            healthAdmin_account_type = Account_Type.objects.get(Account_type='HealthAdmin')  # Correct the field name

            newAcc = Accounts.objects.create(
                ha_id=healthAdmin, 
                account_typeid=healthAdmin_account_type  
            )

            user = authenticate(request, username=username, password=password1)
            if user is not None:
                login(request, user)  
                return redirect('healthDashboard')
        else:
            messages.error(request, "Passwords do not match.")

    return render(request, 'healthAdmin/addHA.html')

def addHA(request):
    return render(request, 'healthAdmin/addHA.html')

def healthDashboard(request):
    return render(request, 'healthAdmin/healthDashboard.html')


def bhwList(request):   
    # Retrieve session data
    account_type = request.session.get('account_type', None)

    # Query Bhw accounts
    bhws = Bhw.objects.filter(
        auth_user__isnull=False,
    ).prefetch_related(
        Prefetch(
            'accounts_set', 
            queryset=Accounts.objects.filter(account_typeid__Account_type='Bhw')
        )
    )

    bsi = Bsi.objects.filter(
        auth_user__isnull=False,
    ).prefetch_related(
        Prefetch(
            'accounts_set', 
            queryset=Accounts.objects.filter(account_typeid__Account_type='BSI')
        )
    )

    healthadmin = HealthAdmin.objects.filter(
        auth_user__isnull=False,
    ).prefetch_related(
        Prefetch(
            'accounts_set', 
            queryset=Accounts.objects.filter(account_typeid__Account_type='HealhAdmin')
        )
    )
    # Query Residents accounts
    residents = Residents.objects.filter(
        auth_user__isnull=False
    ).prefetch_related(
        Prefetch(
            'accounts_set', 
            queryset=Accounts.objects.filter(account_typeid__Account_type='Resident')
        )
    )

    # Query Officials accounts
    officials = Personnel.objects.filter(
        auth_user__isnull=False
    ).prefetch_related(
        Prefetch(
            'accounts_set', 
            queryset=Accounts.objects.filter(account_typeid__Account_type='Admin')
        )
    )

    # Prepare context data
    context = {
        'account_type': account_type,
        'bhws': bhws,
        'bsis': bsi,
        'healthadmins': healthadmin,
        'residents': residents,
        'officials': officials,
    }

    # Render the template with context
    return render(request, 'healthAdmin/bhwList.html', context)




#add service 
def addHealthservice(request):
    if request.method == 'POST':
        # Extract data from the POST request
        service_name = request.POST.get('service_name')
        service_description = request.POST.get('service_description')
        service_requirements = request.POST.get('service_requirements')
        picture = request.FILES.get('picture')
        service_type = request.POST.get('service_type')

        # Basic validation (optional, can be improved)
        if service_name and service_description and service_requirements and picture:
            # Create and save the HealthService object
            new_service = HealthService(
                service_name=service_name, 
                service_description=service_description, 
                service_requirements=service_requirements, 
                picture=picture,
                service_type=service_type
            )
            new_service.save()
            return redirect('bhwService') 
        else:
            error_message = "All fields are required."



# Service deletion function
def delete_healthservice(request, HealthService_id):
    bhwService = get_object_or_404(HealthService, pk=HealthService_id)
    
    if request.method == 'POST':
        bhwService.delete()

    return redirect('bhwService')

def updateHealthservice(request):
    if request.method == 'POST':
        healthservice_id = request.POST.get('healthservice_id')
        bhwService = get_object_or_404(HealthService, id=healthservice_id)

        # Update the fields
        bhwService.service_name = request.POST.get('service_name')
        bhwService.service_description = request.POST.get('service_description')
        bhwService.service_requirements = request.POST.get('service_requirements')
        bhwService.service_type = request.POST.get('service_type')

        # Handle picture upload if it exists
        if 'picture' in request.FILES:
            bhwService.picture = request.FILES['picture']

        bhwService.save()
        return redirect('bhwService')  

    return HttpResponse("Invalid method", status=405)
 


#-------------------bhw Side-------------------
def bhwService(request):
     bhwServices = HealthService.objects.all() 
     return render(request, 'healthAdmin/bhwService.html', {'bhwServices': bhwServices})

def bhwEvents(request):
    return render(request, 'healthAdmin/bhwEvents.html')

#fetch Health records in bhw side
@login_required
def bhwRecord(request):
    schedules = Schedule.objects.exclude(bhwService__service_type='sanitary')  # Fetch all schedules
    return render(request, 'healthAdmin/bhwHealthrecords.html', {'schedules': schedules})


def bhwMedic(request):
    return render(request, 'healthAdmin/bhwMI.html')