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
from .forms import ResidentProfileForm

# Create your views here.


@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password')
        password2 = request.POST.get('password2')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('register')

        if password1 == password2:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
            )
            resident = Residents.objects.create(auth_user=user)
            resident_account_type = Account_Type.objects.get(Account_type='Resident')
            Accounts.objects.create(resident_id=resident, account_typeid=resident_account_type)

            # Automatically log the user in after registration
            user = authenticate(request, username=username, password=password1)
            if user is not None:
                login(request, user)
                return redirect('residentdashboard')  # Redirect to resident dashboard
        else:
            messages.error(request, "Passwords do not match.")

    return render(request, 'account/signup.html')


#Register Admin
@csrf_exempt
def adminregister(request):
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

            personnel = Personnel.objects.create(
                auth_user=user,
            )

            personnel_account_type = Account_Type.objects.get(Account_type='Admin')

            newAcc = Accounts.objects.create(
                admin_id=personnel,
                account_typeid=personnel_account_type
            )


            user = authenticate(request, username=username, password=password1)
            if user is not None:
                login(request, user)  
                return redirect('admindashboard')
        else:
            messages.error(request, "Passwords do not match.")

    return render(request, 'admin/addAdmin.html')

@csrf_exempt
def validatelogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # Find the correct profile based on user type
            profile = None
            if Accounts.objects.filter(resident_id__auth_user=user).exists():
                profile = Accounts.objects.get(resident_id__auth_user=user)
            elif Accounts.objects.filter(bhw_id__auth_user=user).exists():
                profile = Accounts.objects.get(bhw_id__auth_user=user)
            elif Accounts.objects.filter(admin_id__auth_user=user).exists():
                profile = Accounts.objects.get(admin_id__auth_user=user)

            if profile:
                account_type = profile.account_typeid.Account_type
                if account_type == 'Resident':
                    return redirect('residentdashboard')
                elif account_type == 'Admin':
                    return redirect('admindashboard')
                elif account_type == 'Bhw':
                    return redirect('bhwDashboard')
                else:
                    return redirect('defaultdashboard')
            else:
                # If no profile is found, treat it as an invalid login
                messages.error(request, "Invalid username or password.")
                return redirect('login')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')
    
    return render(request, 'account/login.html')




def index(request):
    return render(request, 'index.html')

def signup(request):
  template = loader.get_template('accounts/signup.html')
  return HttpResponse(template.render())

@login_required
def residentdashboard(request):
    resident = Residents.objects.filter(auth_user=request.user).first()

    # Check if profile is incomplete
    if resident and not resident.is_profile_complete:
        if request.method == 'POST':
            resident.fname = request.POST.get('fname')
            resident.mname = request.POST.get('mname')
            resident.lname = request.POST.get('lname')
            resident.zone = request.POST.get('zone')
            resident.civil_status = request.POST.get('civil_status')
            resident.occupation = request.POST.get('occupation')
            resident.age = request.POST.get('age') or None  # Handle null values
            resident.birthdate = request.POST.get('birthdate')
            resident.phone_number = request.POST.get('phone_number')
            resident.position = request.POST.get('position')
            
            if 'picture' in request.FILES:
                resident.picture = request.FILES['picture']
            
            resident.is_profile_complete = True
            resident.save()
            return redirect('residentdashboard')  # Reload dashboard after saving

        return render(request, 'resident/userd.html', {'resident': resident, 'show_modal': True})

    # Render dashboard normally if profile is complete
    return render(request, 'resident/userd.html', {'show_modal': False})





#-------------------Admin-------------------
def admindashboard(request):
    return render(request, 'admin/admin.html')

def adminAccounts(request):
    return render(request, 'admin/adminAccounts.html')

def adminService(request):
    return render(request, 'admin/adminService.html')

def adminCertificates(request):
    return render(request, 'admin/adminCertificates.html')

def adminEvent(request):
    return render(request, 'admin/adminEvent.html')

def adminPayment(request):
    return render(request, 'admin/adminPayment.html')

def adminResident(request):
    return render(request, 'admin/adminResident.html')

def addAdmin(request):
    return render(request, 'admin/addAdmin.html')




#-------------------BHW Secretary & Nurse-------------------
@csrf_exempt
def bhwregister(request):
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
    return render(request, 'bhw/bhwDashboard.html')

def addBhw(request):
    return render(request, 'bhw/addBhw.html')


def bhwOutbreak(request):
    return render(request, 'bhw/bhwOutbreaks.html')

#fetch Health records in bhw side
@login_required
def bhwRecord(request):
    schedules = Schedule.objects.all()  # Fetch all schedules
    return render(request, 'bhw/bhwHealthrecords.html', {'schedules': schedules})

def bhwMedic(request):
    return render(request, 'bhw/bhwMI.html')


def bhwEvents(request):
    return render(request, 'bhw/bhwEvents.html')


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
        'residents': residents,
        'officials': officials,
    }

    # Render the template with context
    return render(request, 'bhw/bhwList.html', context)





#add service 
def addHealthservice(request):
    if request.method == 'POST':
        # Extract data from the POST request
        service_name = request.POST.get('service_name')
        service_description = request.POST.get('service_description')
        service_requirements = request.POST.get('service_requirements')
        picture = request.FILES.get('picture')

        # Basic validation (optional, can be improved)
        if service_name and service_description and service_requirements and picture:
            # Create and save the HealthService object
            new_service = HealthService(
                service_name=service_name, 
                service_description=service_description, 
                service_requirements=service_requirements, 
                picture=picture
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
    return render(request, 'bhw/bhwDeleteservice.html', {'bhwService': bhwService})

#Update Health Service
def update_healthservice(request, HealthService_id):
    bhwService = get_object_or_404(HealthService, pk=HealthService_id)
    
    if request.method == 'POST':
        
        bhwService.service_name = request.POST.get('service_name')
        bhwService.service_description = request.POST.get('service_description')
        bhwService.service_requirements = request.POST.get('service_requirements')
        
    
        if 'picture' in request.FILES:
            bhwService.picture = request.FILES['picture']

        bhwService.save()

        
        return redirect('bhwService')
   
    return render(request, 'bhw/bhwUpdateservice.html', { 'bhwService': bhwService})

#-------------------Resident Side-------------------
def bhwService(request):
    bhwService = HealthService.objects.all()
    template = loader.get_template('bhw/bhwService.html')
    context = {
        'bhwService': bhwService,
    }
    return HttpResponse(template.render(context, request))

#service display for resident side 
def bhwServices(request):
    bhwServices = HealthService.objects.all()
    template = loader.get_template('resident/residentHS.html')
    context = {
        'bhwServices': bhwServices,
    }
    return HttpResponse(template.render(context, request))

# Book service  
@login_required
def book_healthService(request, HealthService_id):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        age = request.POST.get('age')
        purok = request.POST.get('purok')
        time = request.POST.get('time')
        date = request.POST.get('date')
        phonenum = request.POST.get('phone')
        user_id = request.user.id  # Get the user ID
        bhwService = HealthService.objects.get(id=HealthService_id)  # Get the service
        
        # Create a new booking object and save it to the database
        schedule = Schedule.objects.create(
            user_id=user_id, 
            bhwService=bhwService, 
            fname=fname, 
            lname=lname, 
            age=age, 
            purok=purok, 
            date=date, 
            time=time, 
            phonenum=phonenum
        )
    
        return redirect(reverse('bhwServices'))


#display service
def book_healthServiceform(request, HealthService_id):
    bhwService = HealthService.objects.get(pk=HealthService_id)
    return render(request, 'resident/Hsapplication.html', {'bhwService': bhwService})

#display the recent avail service to the resident side
def residentHistory(request):
    user = request.user
    
    schedules = Schedule.objects.filter(user__username=user.username)
    return render(request, 'resident/residentHistory.html', {'schedules': schedules})

