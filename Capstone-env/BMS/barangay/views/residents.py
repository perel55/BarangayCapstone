from django.shortcuts import render, redirect, get_object_or_404
from .models import Residents, Schedule, Request, Services
from .forms import ResidentProfileForm  # Import a form for the Residents model
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta, datetime
from django.http import JsonResponse
from .models import *
from datetime import datetime
from django.http import HttpResponse

@login_required
def edit_profile(request):
    # Fetch the resident profile for the logged-in user
    resident = get_object_or_404(Residents, auth_user=request.user)
    
    if request.method == "POST":
        # Retrieve data from POST request
        resident.fname = request.POST.get('fname', resident.fname)
        resident.mname = request.POST.get('mname', resident.mname)
        resident.lname = request.POST.get('lname', resident.lname)
        resident.zone = request.POST.get('zone', resident.zone)
        resident.civil_status = request.POST.get('civil_status', resident.civil_status)
        resident.occupation = request.POST.get('occupation', resident.occupation)
        resident.age = request.POST.get('age', resident.age)
        
        # Convert the birthdate from string to date
        birthdate_str = request.POST.get('birthdate', resident.birthdate)
        if birthdate_str:
            resident.birthdate = datetime.strptime(birthdate_str, '%Y-%m-%d').date()
        
        resident.phone_number = request.POST.get('phone_number', resident.phone_number)
        resident.position = request.POST.get('position', resident.position)
        
        # Handle file upload for the picture
        if 'picture' in request.FILES:
            resident.picture = request.FILES['picture']
        
        # Mark the profile as complete
        resident.is_profile_complete = True
        resident.save()

        # Redirect to a profile view or another page
        return redirect('view_events')  # Replace 'profile' with the actual name of your profile view
    
    # Render the edit profile page with current data
    # Ensure birthdate is passed as a string in the correct format
    birthdate_str = resident.birthdate.strftime('%Y-%m-%d') if resident.birthdate else ""
    return render(request, 'resident/residentEditProfile.html', {'resident': resident, 'birthdate_str': birthdate_str})



# View to render the calendar
def calendar_view(request):
    # Fetch all requests for the resident (use request.user if a resident is logged in)
    resident = Residents.objects.get(auth_user=request.user)  # Assuming 'request.user' is the logged-in resident
    requests = Request.objects.filter(Resident_id=resident)  # Filter requests by the logged-in resident
    
    events = []

    # Convert the request data into event format for FullCalendar
    for req in requests:
        events.append({
            'title': f"{req.service_id.service_name} - {req.reason}",  # Display service name and reason as event title
            'start': req.schedule_date.isoformat(),  # Use the request date for the event start time
            'end': (req.schedule_date + timezone.timedelta(hours=1)).isoformat(),  # Assume an event duration of 1 hour
        })

    return render(request, 'resident/ResidentCalendar.html', {'events': events})

# API endpoint to fetch events (if you're using Ajax to load data)
def get_events(request):
    # Fetch all requests for the logged-in resident
    resident = Residents.objects.get(auth_user=request.user)
    requests = Request.objects.filter(Resident_id=resident)
    
    events = []
    for req in requests:
        events.append({
            'title': f"{req.service_id.service_name} - {req.reason}",
            'start': req.r_date.isoformat(),
            'end': (req.r_date + timezone.timedelta(hours=1)).isoformat(),  # Duration of 1 hour
        })

    return JsonResponse(events, safe=False)

# API endpoint to create events (if you're submitting data via form submission or Ajax)
def create_event(request):
    if request.method == 'POST':
        service_id = request.POST.get('service_id')
        reason = request.POST.get('reason')
        r_date = request.POST.get('r_date')
        r_date = timezone.make_aware(datetime.fromisoformat(r_date))  # Convert to timezone-aware datetime

        # Assuming the logged-in resident is the one making the request
        resident = Residents.objects.get(auth_user=request.user)

        # Fetch the service object
        service = Services.objects.get(service_id=service_id)

        # Create the request record
        new_request = Request.objects.create(
            Resident_id=resident,
            service_id=service,
            reason=reason,
            r_date=r_date,
            total_price=service.service_price,  # Assuming price is on the service
        )

        return JsonResponse({'status': 'success'}, status=201)

    return JsonResponse({'status': 'error'}, status=400)


def get_services(request):
    services = Services.objects.all()
    services_list = [{'service_id': service.service_id, 'service_name': service.service_name} for service in services]
    
    return JsonResponse(services_list, safe=False)

# ----------------------------> Community Notices <---------------------------

def view_events(request):
    """Render the page with the calendar."""
    return render(request, 'resident/residentEvents.html')

def get_resident_notices(request):
    """Fetch the notices to display on the calendar."""
    notices = CommunityNotice.objects.all()
    events = []

    for notice in notices:
        event = {
            'title': notice.notice_name,
            'start': f"{notice.notice_StartDate}T{notice.notice_StartTime}",
            'end': f"{notice.notice_EndDate}T{notice.notice_EndTime}" if notice.notice_EndDate else None,
            'notice_id': notice.id,
            'description': notice.notice_description,
            'image': notice.notice_image.url if notice.notice_image else None,
            'notice_type': notice.notice_type,
            'notice_color': notice.notice_color,
        }
        events.append(event)

    return JsonResponse(events, safe=False)


def get_notice_detail(request, notice_id):
    try:
        notice = CommunityNotice.objects.get(id=notice_id)
        data = {
            'notice_name': notice.notice_name,
            'notice_description': notice.notice_description,
            'notice_image': notice.notice_image.url if notice.notice_image else None,
            'notice_StartDate': notice.notice_StartDate,
            'notice_EndDate': notice.notice_EndDate,
            'notice_StartTime': notice.notice_StartTime.strftime('%I:%M %p') if notice.notice_StartTime else None,
            'notice_EndTime': notice.notice_EndTime.strftime('%I:%M %p') if notice.notice_EndTime else None,
            'notice_type': notice.notice_type,
        }
        return JsonResponse(data)
    except CommunityNotice.DoesNotExist:
        return JsonResponse({'error': 'Notice not found'}, status=404)



def notice_details_view(request, notice_id):
    """Render the full details of a specific notice."""
    notice = get_object_or_404(CommunityNotice, id=notice_id)
    return render(request, 'resident/notice_details.html', {
        'notice': notice,
    })


def fetch_notices(request):
    notices = CommunityNotice.objects.all()
    events = [
        {
            'title': notice.notice_name,
            'start': f"{notice.notice_StartDate}T{notice.notice_StartTime}",
            'end': f"{notice.notice_EndDate}T{notice.notice_EndTime}" if notice.notice_EndDate else None,
            'extendedProps': {
                'notice_id': notice.id,  # Add the notice_id inside extendedProps
                'description': notice.notice_description,
                'image': notice.notice_image.url if notice.notice_image else None,
                'notice_type': notice.notice_type,
                'notice_color': notice.notice_color,
            },
        }
        for notice in notices
    ]
    return JsonResponse(events, safe=False)





    


# --------------------------> RESIDENT PROFILE <-------------------------------

from datetime import datetime

@login_required
def edit_profile(request):
    resident = get_object_or_404(Residents, auth_user=request.user)

    if request.method == "POST":
        resident.fname = request.POST.get('fname', resident.fname)
        resident.mname = request.POST.get('mname', resident.mname)
        resident.lname = request.POST.get('lname', resident.lname)
        resident.zone = request.POST.get('zone', resident.zone)
        resident.civil_status = request.POST.get('civil_status', resident.civil_status)
        resident.occupation = request.POST.get('occupation', resident.occupation)
        resident.age = request.POST.get('age', resident.age)

        birthdate_str = request.POST.get('birthdate', resident.birthdate)
        if birthdate_str:
            resident.birthdate = datetime.strptime(birthdate_str, '%Y-%m-%d').date()

        resident.phone_number = request.POST.get('phone_number', resident.phone_number)
        resident.position = request.POST.get('position', resident.position)

        if 'picture' in request.FILES:
            resident.picture = request.FILES['picture']

        resident.is_profile_complete = True
        resident.save()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'message': 'Profile updated successfully'}, status=200)

        return redirect('edit_profile')

    birthdate_str = resident.birthdate.strftime('%Y-%m-%d') if resident.birthdate else ""
    return render(request, 'resident/residentEditProfile.html', {'resident': resident, 'birthdate_str': birthdate_str})



# ------------------------> MAP <---------------------------

def barangay_map(request):
    return render(request, 'resident/residentOutbreaks.html')


# ------------------------> SERVICE LIST <-----------------------

def resident_services(request):
    services = Services.objects.all()  # Query all services
    return render(request, 'resident/residentServices.html', {'services': services})

def get_resident_details(request, resident_id):
    # Fetch the resident object by ID
    resident = get_object_or_404(Residents, id=resident_id)

    # Prepare the response data
    data = {
        'username': resident.auth_user.username,
        'email': resident.auth_user.email,
        'fname': resident.auth_user.first_name,
        'mname': resident.auth_user.middle_name,
        'lname': resident.auth_user.last_name,
        'zone': resident.zone,
        'civil_status': resident.civil_status,
        'occupation': resident.occupation,
        'phone_number': resident.phone_number,
        'picture': resident.picture.url if resident.picture else None,
        'id_image': resident.id_image.url if resident.id_image else None,
        'status': resident.status,
    }
    return JsonResponse(data)