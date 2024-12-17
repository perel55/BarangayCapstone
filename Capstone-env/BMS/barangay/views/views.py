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


# Create your views here.


#Register Residents
@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')  
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('register')  

        # Check if passwords match
        if password1 == password2:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name,
                
            )

            resident = Residents.objects.create(
                auth_user=user,
            )

            resident_account_type = Account_Type.objects.get(Account_type='Resident')

            newAcc = Accounts.objects.create(
                resident_id=resident,
                account_typeid=resident_account_type
            )

            # Automatically log the user in after registration
            user = authenticate(request, username=username, password=password1)
            if user is not None:
                login(request, user)  
                return redirect('residentdashboard')
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
            elif Accounts.objects.filter(bsi_id__auth_user=user).exists():
                profile = Accounts.objects.get(bsi_id__auth_user=user)
            elif Accounts.objects.filter(ha_id__auth_user=user).exists():
                profile = Accounts.objects.get(ha_id__auth_user=user)          

            if profile:
                account_type = profile.account_typeid.Account_type
                if account_type == 'Resident':
                    return redirect('residentdashboard')
                elif account_type == 'Admin':
                    return redirect('admindashboard')
                elif account_type == 'Bhw':
                    return redirect('bhwDashboard')
                elif account_type == 'BSI':
                    return redirect('bsiDashboard')
                elif account_type == 'HealthAdmin':
                    return redirect('healthDashboard')
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



@login_required
def logout(request):
    return render(request, 'accounts/logout.html')

def signup(request):
  template = loader.get_template('accounts/signup.html')
  return HttpResponse(template.render())

@login_required
def residentdashboard(request):
    return render(request, 'resident/userd.html')



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

@login_required
def bhwServices(request):
    try:
        resident = Residents.objects.get(auth_user=request.user)
        if resident.status == "Verify":
            bhwServices = HealthService.objects.all()
        else:
            bhwServices = HealthService.objects.none()
    
    except Residents.DoesNotExist:
        bhwServices = HealthService.objects.none()

    # Load the template
    template = loader.get_template('resident/residentHS.html')
    context = {
        'bhwServices': bhwServices,
    }
    return HttpResponse(template.render(context, request))

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import HealthService, Schedule, Residents


@login_required
def book_healthService(request, HealthService_id, resident_id): 
    bhwService = get_object_or_404(HealthService, id=HealthService_id)
    resident = get_object_or_404(Residents, id=resident_id)

    if request.method == 'POST':
        date = request.POST.get('date')
    

        Schedule.objects.create(
            user=request.user, 
            resident=resident, 
            bhwService=bhwService,
            date=date,
        )

        # Redirect to the 'bhwServices' page after successful booking
        return redirect(reverse('bhwServices'))


#immunization type of service
@login_required
def book_immunize(request, HealthService_id, resident_id): 
    bhwService = get_object_or_404(HealthService, id=HealthService_id)
    resident = get_object_or_404(Residents, id=resident_id)

    if request.method == 'POST':
        date = request.POST.get('date')
        father_name = request.POST.get('father_name')
        mother_name = request.POST.get('mother_name')
        baby_name = request.POST.get('baby_name')
        image = request.FILES.get('image')
    

        Schedule.objects.create(
            user=request.user, 
            resident=resident, 
            bhwService=bhwService,
            date=date,
            father_name=father_name,
            mother_name=mother_name,
            baby_name=baby_name,
            image=image,    
        )

        # Redirect to the 'bhwServices' page after successful booking
        return redirect(reverse('bhwServices'))

    
@login_required
def book_healthServiceform(request, HealthService_id):
    bhwService = get_object_or_404(HealthService, pk=HealthService_id)

    try:
        resident = Residents.objects.get(auth_user=request.user)
    except Residents.DoesNotExist:
        resident = None

    if bhwService.service_type == "immunization": 
        return render(request, 'resident/residentImmunize.html', {'bhwService': bhwService, 'resident': resident})
    else:
        return render(request, 'resident/Hsapplication.html', {'bhwService': bhwService, 'resident': resident})



#display the recent avail service to the resident sidecd 
def residentHistory(request):
    user = request.user
    schedules = Schedule.objects.filter(user__username=user.username)
    resident = Residents.objects.get(auth_user=request.user)
    return render(request, 'resident/residentHistory.html', {'schedules': schedules, 'resident': resident})

@login_required
def residentdashboard(request):
    resident = Residents.objects.filter(auth_user=request.user).first()

    # Check if profile is incomplete
    if resident and not resident.is_profile_complete:
        if request.method == 'POST':
            resident.mname = request.POST.get('mname')
            resident.zone = request.POST.get('zone')
            resident.civil_status = request.POST.get('civil_status')
            resident.occupation = request.POST.get('occupation')
            resident.birthdate = request.POST.get('birthdate')
            resident.phone_number = request.POST.get('phone_number')
            resident.position = request.POST.get('position')

            
            if 'picture' in request.FILES:
                resident.picture = request.FILES['picture']
            
            if 'id_image' in request.FILES:
                resident.id_image = request.FILES['id_image']
            
            resident.is_profile_complete = True
            resident.save()
            return redirect('residentdashboard')  # Reload dashboard after saving

        return render(request, 'resident/userd.html', {'resident': resident, 'show_modal': True})

    # Render dashboard normally if profile is complete
    return render(request, 'resident/userd.html', {'show_modal': False})