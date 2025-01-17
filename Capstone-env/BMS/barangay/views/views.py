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
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import HealthService, Schedule, Residents
from django.utils import timezone
from datetime import date, timedelta



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

@csrf_exempt
def adminregister(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        account_type = request.POST.get('account_type')

        if password1 == password2:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name,
            )

            account_type_obj = Account_Type.objects.get(Account_type=account_type)

            if account_type == "Admin":
                personnel = Personnel.objects.create(auth_user=user)
                Accounts.objects.create(
                    admin_id=personnel,
                    account_typeid=account_type_obj
                )
            elif account_type == "HealthAdmin":
                health_admin = HealthAdmin.objects.create(auth_user=user)
                Accounts.objects.create(
                    ha_id=health_admin,
                    account_typeid=account_type_obj
                )
            elif account_type == "BSI":
                bsi = Bsi.objects.create(auth_user=user)
                Accounts.objects.create(
                    bsi_id=bsi,
                    account_typeid=account_type_obj
                )
            elif account_type == "Bhw":
                bhw = Bhw.objects.create(auth_user=user)
                Accounts.objects.create(
                    bhw_id=bhw,
                    account_typeid=account_type_obj
                )
            elif account_type == "Secretary":
                secretary = Secretary.objects.create(auth_user=user)
                Accounts.objects.create(
                    secretary_id=secretary,
                    account_typeid=account_type_obj
                )
            elif account_type == "Resident":
                resident = Residents.objects.create(auth_user=user)
                Accounts.objects.create(
                    resident_id=resident,
                    account_typeid=account_type_obj
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
            elif Accounts.objects.filter(secretary_id__auth_user=user).exists():
                profile = Accounts.objects.get(secretary_id__auth_user=user)              

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
                elif account_type == 'Secretary':
                    return redirect('secretarydashboard')
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

from django.contrib.auth import logout as auth_logout

@login_required
def logout(request):
    if request.method == 'POST':
        logout(request)  
        return redirect('validatelogin')  
    return render(request, 'account/logout.html')

@login_required
def bhwlogout(request):
    if request.method == 'POST':
        logout(request)  
        return redirect('validatelogin')  #
    return render(request, 'account/bhwlogout.html')  
          

@login_required
def secretarylogout(request):
    if request.method == 'POST':
        logout(request)  
        return redirect('validatelogin')  
    return render(request, 'account/secretarylogout.html') 
         

@login_required
def adminlogout(request):
    if request.method == 'POST':
        logout(request)  
        return redirect('validatelogin')  #
    return render(request, 'account/adminlogout.html') 
                 
    


def signup(request):
  template = loader.get_template('accounts/signup.html')
  return HttpResponse(template.render())


#-------------------Admin-------------------
def admindashboard(request):
    return render(request, 'admin/admin.html')

def adminAccounts(request):
    return render(request, 'admin/adminAccounts.html')

def adminService(request):
    return render(request, 'admin/adminService.html')

def adminCertificates(request):
    # Query the Request model to get all requests
    requests = Request.objects.all()  # You can adjust the query to filter by status, date, etc.

    # Pass the requests to the template
    return render(request, 'admin/adminCertificates.html', {'requests': requests})

def update_request_status(request, request_id):
    # Get the request object
    req = Request.objects.get(id=request_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        req.status = new_status
        req.save()

        # Provide feedback to the admin
        messages.success(request, f"Request status updated to {new_status}.")

        return redirect('adminCertificates')  # Adjust the redirect to the appropriate page

    return redirect('adminCertificates')  # Handle GET request, redirect as needed


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
def bhwServices(request): #display the available services for verified status
    try:
        resident = Residents.objects.get(auth_user=request.user)
        if resident.status == "Verified":
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
        )

        # Redirect to the 'bhwServices' page after successful booking
        return redirect(reverse('bhwServices'))


#immunization type of service
@login_required
def book_immunize(request, HealthService_id, resident_id): 
    bhwService = get_object_or_404(HealthService, id=HealthService_id)
    resident = get_object_or_404(Residents, id=resident_id)

    if request.method == 'POST':
        father_name = request.POST.get('father_name')
        mother_name = request.POST.get('mother_name')
        baby_name = request.POST.get('baby_name')
        birthdate = request.POST.get('birthdate')
        sex = request .POST.get('sex')
        birth_place = request.POST.get('birth_place')

        Schedule.objects.create(
            user=request.user, 
            resident=resident, 
            bhwService=bhwService,
            father_name=father_name,
            mother_name=mother_name,
            baby_name=baby_name,
            birthdate=birthdate,
            sex=sex,
            birth_place=birth_place, 
        )

        # Redirect to the 'bhwServices' page after successful booking
        return redirect(reverse('bhwServices'))
    

#maintenance
@login_required
def book_maintenance(request, HealthService_id, resident_id): 
    bhwService = get_object_or_404(HealthService, id=HealthService_id)
    resident = get_object_or_404(Residents, id=resident_id)

    if request.method == 'POST':
        date= request.POST.get('date')
        time= request.POST.get('time')
     

        Schedule.objects.create(
            user=request.user, 
            resident=resident, 
            bhwService=bhwService,
            date=date,
            time=time,
         
        )

       
        return redirect(reverse('bhwServices'))

#Other Service type
@login_required
def book_otherService(request, HealthService_id, resident_id): 
    bhwService = get_object_or_404(HealthService, id=HealthService_id)
    resident = get_object_or_404(Residents, id=resident_id)

    if request.method == 'POST':
        date= request.POST.get('date')
        time= request.POST.get('time')
     

        Schedule.objects.create(
            user=request.user, 
            resident=resident, 
            bhwService=bhwService,
            date=date,
            time=time,
         
        )

        return redirect(reverse('bhwServices'))


    
@login_required
def book_healthServiceform(request, HealthService_id):
    bhwService = get_object_or_404(HealthService, pk=HealthService_id)

    try:
        resident = Residents.objects.get(auth_user=request.user)
    except Residents.DoesNotExist:
        resident = None

    if bhwService.service_type == "immunnization": 
        return render(request, 'resident/residentImmunize.html', {'bhwService': bhwService, 'resident': resident})
    elif bhwService.service_type == "maintenance":
        return render(request, 'resident/residentTB.html', {'bhwService': bhwService, 'resident': resident})
    elif bhwService.service_type == "other":
        return render(request, 'resident/OtherForm.html', {'bhwService': bhwService, 'resident': resident})
    else:
        return render(request, 'resident/Hsapplication.html', {'bhwService': bhwService, 'resident': resident})





#display the recent avail service to the resident sidecd 
def residentHistory(request):
    user = request.user

    # Get the logged-in resident
    resident = Residents.objects.get(auth_user=request.user)

    # Fetch schedules and requests for the logged-in user
    schedules = Schedule.objects.filter(user=user)  # Assuming 'user' field in Schedule links to auth user
    requests = Request.objects.filter(user=user)  # Fetch only the requests of the logged-in user

    return render(request, 'resident/residentHistory.html', {
        'schedules': schedules,
        'requests': requests,
        'resident': resident
    })

from django.contrib.auth import logout
from django.shortcuts import redirect
from django.utils.timezone import now
from django.db.models import Count

from datetime import date, timedelta
from django.db.models import Count

@login_required
def residentdashboard(request):
    # Check if session is active
    if not request.user.is_authenticated:
        logout(request)
        return redirect('login')

    resident = Residents.objects.filter(auth_user=request.user).first()

    # Automatically fetch first and last name from the auth_user model
    user_first_name = request.user.first_name
    user_last_name = request.user.last_name

    # Fetch additional data for the dashboard
    today = date.today()
    recent_schedules = Schedule.objects.filter(date__gte=today - timedelta(days=7)).order_by('-date')
    upcoming_notices = CommunityNotice.objects.filter(notice_StartDate__gte=today).order_by('notice_StartDate')
    recent_requests = Request.objects.filter(schedule_date__gte=today - timedelta(days=7)).order_by('-schedule_date')
    outbreaks_data = Outbreaks.objects.values('outbreak_name').annotate(count=Count('id')).order_by('-count')
    popular_services = Services.objects.annotate(request_count=Count('request')).order_by('-request_count')[:5]

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
            return redirect('residentdashboard')

        context = {
            'resident': resident,
            'show_modal': True,
            'user_first_name': user_first_name,
            'user_last_name': user_last_name,
            'recent_schedules': recent_schedules,
            'upcoming_notices': upcoming_notices,
            'recent_requests': recent_requests,
            'outbreaks_data': outbreaks_data,
            'popular_services': popular_services,
        }

        return render(request, 'resident/userd.html', context)

    # Context when the resident profile is already complete
    context = {
        'show_modal': False,
        'recent_schedules': recent_schedules,
        'upcoming_notices': upcoming_notices,
        'recent_requests': recent_requests,
        'outbreaks_data': outbreaks_data,
        'popular_services': popular_services,
    }

    return render(request, 'resident/userd.html', context)



def profile_check(request):
    # Log the user out
    logout(request)
    
    # Redirect to the login page after logging out
    return redirect('login')  # Make sure the 'login' URL pattern is correct in your urls.py



@login_required
def secretarydashboard(request):
    secretary = Secretary.objects.filter(auth_user=request.user).first()

    # Automatically fetch first and last name from the auth_user model
    user_first_name = request.user.first_name
    user_last_name = request.user.last_name

    # Dashboard statistics
    pending_residents_count = Residents.objects.filter(status='Pending').count()
    pending_requests_count = Request.objects.filter(status='Pending').count()
    today = timezone.now().date()
    upcoming_notices_count = CommunityNotice.objects.filter(notice_EndDate__gte=today).count()
    active_outbreaks_count = Outbreaks.objects.filter(status="Active").count()
    total_residents_count = Residents.objects.count()

    # Check if secretary profile is incomplete
    show_modal = secretary and not all([
        secretary.mname,
        secretary.zone,
        secretary.civil_status,
        secretary.occupation,
        secretary.birthdate,
        secretary.phone_number,
        secretary.picture,
        secretary.position
    ])

    if request.method == 'POST':
        # Update the secretary profile
        if secretary:
            secretary.mname = request.POST.get('mname', secretary.mname)
            secretary.zone = request.POST.get('zone', secretary.zone)
            secretary.civil_status = request.POST.get('civil_status', secretary.civil_status)
            secretary.occupation = request.POST.get('occupation', secretary.occupation)
            secretary.birthdate = request.POST.get('birthdate', secretary.birthdate)
            secretary.phone_number = request.POST.get('phone_number', secretary.phone_number)

            # Handle file uploads
            if request.FILES.get('picture'):
                secretary.picture = request.FILES['picture']
            if request.FILES.get('id_image'):
                secretary.id_image = request.FILES['id_image']

            secretary.position = request.POST.get('position', secretary.position)
            secretary.is_profile_complete = True
            secretary.save()

            return redirect('secretarydashboard')

    context = {
        'secretary': secretary,
        'pending_residents_count': pending_residents_count,
        'pending_requests_count': pending_requests_count,
        'upcoming_notices_count': upcoming_notices_count,
        'active_outbreaks_count': active_outbreaks_count,
        'total_residents_count': total_residents_count,
        'show_modal': show_modal,
        'user_first_name': user_first_name,
        'user_last_name': user_last_name,
    }

    return render(request, 'secretary/secDashboard.html', context)







