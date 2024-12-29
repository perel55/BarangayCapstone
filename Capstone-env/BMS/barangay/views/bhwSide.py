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
from django.db.models import Count
from django.shortcuts import render
from .models import Outbreaks
from django.db.models import Q

def bhwOutbreak(request):
    # Fetch all outbreaks
    outbreaks = Outbreaks.objects.all()

    active_outbreak_counts = (
        Outbreaks.objects.filter(status="Active")
        .values('purok')  # Group by purok
        .annotate(total_active_cases=Count('id'))  
        .order_by('purok') 
    )
    context = {
        'outbreaks': outbreaks,
        'active_outbreak_counts': active_outbreak_counts,
    }
    return render(request, 'bhw/bhwOutbreaks.html', context)

def addOutbreak(request):
     if request.method == "POST":
        # Retrieve form data from the POST request
        outbreak_name = request.POST.get('outbreak_name')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        purok = request.POST.get('purok')
        date = request.POST.get('date')
        status = request.POST.get("status", "Active")

     
        Outbreaks.objects.create(
            outbreak_name=outbreak_name,
            fname=fname,
            lname=lname,
            purok=purok,
            date=date,
            status=status,
             
        )
        
        return redirect('bhwOutbreak')  
     
def updateOutbreak(request):
    if request.method == "POST":
        outbreak_id = request.POST.get('outbreak_id')  
        outbreak = get_object_or_404(Outbreaks, id=outbreak_id)  


        outbreak.outbreak_name = request.POST.get('outbreak_name')
        outbreak.fname = request.POST.get('fname')
        outbreak.lname = request.POST.get('lname')
        outbreak.purok = request.POST.get('purok')
        outbreak.date = request.POST.get('date')


        outbreak.save()
        return redirect('bhwOutbreak')  

    return HttpResponse("Invalid method", status=405)  

@csrf_exempt
def bhwregister(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        if password1 == password2:
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name,
            )

            bhw = Bhw.objects.create(
                auth_user=user,
            )

            bhw_account_type = Account_Type.objects.get(Account_type='Bhw')

            newAcc = Accounts.objects.create(
                bhw_id=bhw,
                account_typeid=bhw_account_type
            )


            user = authenticate(request, username=username, password=password1)
            if user is not None:
                login(request, user)  
                return redirect('bhwDashboard')
        else:
            messages.error(request, "Passwords do not match.")

    return render(request, 'bhw/addBhw.html')

def bhwDashboard(request):
    total_bhw = Accounts.objects.filter(account_typeid__Account_type='Bhw').count()
    total_admin = Accounts.objects.filter(account_typeid__Account_type='Admin').count()
    total_resident = Accounts.objects.filter(account_typeid__Account_type='Resident').count()
    verified_resident = Residents.objects.filter(status='Verify').count()
    total_healthService = HealthService.objects.all().count()
    active_outbreaks = Outbreaks.objects.filter(status='Active').count()
    inactive_outbreaks = Outbreaks.objects.filter(status='Inactive').count()
    total_maintenance = Schedule.objects.filter(bhwService__service_type='maintenance' ).count()
    total_immunization = Schedule.objects.filter(bhwService__service_type='immunization' ).count()
    total_medicine = Medicine.objects.all().count()



    context = {
        'total_bhw': total_bhw,
        'total_admin': total_admin,
        'total_resident': total_resident,
        'total_healthService': total_healthService,
        'active_outbreaks':  active_outbreaks,
        'inactive_outbreaks':  inactive_outbreaks,
        'total_maintenance':  total_maintenance,
        'verified_resident':  verified_resident,
        'total_immunization':  total_immunization,
        'total_medicine':  total_medicine,
    }

    return render(request, 'bhw/bhwDashboard.html', context)


def addBhw(request):
    return render(request, 'bhw/addBhw.html')



def bhwList(request):
    # Retrieve session data
    account_type = request.session.get('account_type', None)

    # Query Bhw accounts and count
    bhws = Bhw.objects.filter(auth_user__isnull=False).prefetch_related(
        Prefetch(
            'accounts_set', 
            queryset=Accounts.objects.filter(account_typeid__Account_type='Bhw')
        )
    )
    total_bhws = bhws.count()

    # Query BSI accounts and count
    bsi = Bsi.objects.filter(auth_user__isnull=False).prefetch_related(
        Prefetch(
            'accounts_set', 
            queryset=Accounts.objects.filter(account_typeid__Account_type='BSI')
        )
    )
    total_bsi = bsi.count()

    # Query HealthAdmin accounts and count
    healthadmin = HealthAdmin.objects.filter(auth_user__isnull=False).prefetch_related(
        Prefetch(
            'accounts_set', 
            queryset=Accounts.objects.filter(account_typeid__Account_type='HealhAdmin')
        )
    )
    total_healthadmins = healthadmin.count()

    # Query Residents accounts and count
    residents = Residents.objects.filter(auth_user__isnull=False).prefetch_related(
        Prefetch(
            'accounts_set', 
            queryset=Accounts.objects.filter(account_typeid__Account_type='Resident')
        )
    )
    total_residents = residents.count()

    # Query Officials accounts and count
    officials = Personnel.objects.filter(auth_user__isnull=False).prefetch_related(
        Prefetch(
            'accounts_set', 
            queryset=Accounts.objects.filter(account_typeid__Account_type='Admin')
        )
    )
    total_officials = officials.count()

    # Prepare context data with totals
    context = {
        'account_type': account_type,
        'bhws': bhws,
        'bsis': bsi,
        'healthadmins': healthadmin,
        'residents': residents,
        'officials': officials,
        'total_bhws': total_bhws,
        'total_bsi': total_bsi,
        'total_healthadmins': total_healthadmins,
        'total_residents': total_residents,
        'total_officials': total_officials,
    }

    # Render the template with context
    return render(request, 'bhw/bhwList.html', context)



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
     return render(request, 'bhw/bhwService.html', {'bhwServices': bhwServices})

def bhwEvents(request):
    return render(request, 'bhw/bhwEvents.html')

#fetch Health records in bhw side
@login_required
def bhwRecord(request):
    all_schedules = Schedule.objects.all()
    highblood_schedules = Schedule.objects.filter(bhwService__service_name="HighBlood")
    tb_schedules = Schedule.objects.filter(bhwService__service_name="TB")
    immunize_schedules = Schedule.objects.filter(bhwService__service_type="immunization")
    return render(request, 'bhw/bhwHealthrecords.html', {
        'all_schedules': all_schedules,
        'highblood_schedules': highblood_schedules,
        'tb_schedules': tb_schedules,
        'immunize_schedules': immunize_schedules,
    })





#not use
def bhwSanitary(request):
    # Filter schedules with service type 'sanitary' or 'none'
    schedules = Schedule.objects.filter(
        Q(bhwService__service_type='sanitary') | Q(bhwService__service_type='none')
    )
    return render(request, 'bhw/bhwSanitary.html', {'schedules': schedules})


@login_required
def approve_sanitary(request, schedule_id):
    schedule = get_object_or_404(Schedule, id=schedule_id)
    schedule.status = "Verified"
    schedule.save()
    return redirect('bhwSanitary')  

