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

def is_resident_approved(resident):
    return resident.status == 'Verified'


@login_required
def calendar_view(request):
    resident = get_object_or_404(Residents, auth_user=request.user)
    
    # Check if the resident is approved
    if not resident or resident.status.lower() != 'verified':
        return redirect('pending_approval')  # Replace with your "Pending Approval" view name or URL

    requests = Request.objects.filter(Resident_id=resident)
    events = []

    for req in requests:
        events.append({
            'title': f"{req.service_id.service_name} - {req.reason}",
            'start': req.schedule_date.isoformat(),
            'end': (req.schedule_date + timezone.timedelta(hours=1)).isoformat(),
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

def pending_approval(request):
    return render(request, 'resident/pending.html')


def view_events(request):
    resident = Residents.objects.filter(auth_user=request.user).first()
    
    # Check if the resident exists and is verified
    if not resident or resident.status.lower() != 'verified':
        return redirect('pending_approval')  # Replace with your "Pending Approval" view name or URL
    
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



# ------------------------> OUTBREAKS <---------------------------

from django.http import JsonResponse
from django.db.models import Count
from .models import Outbreaks

def resident_outbreaks_view(request):
    return render(request, 'resident/residentOutbreaks.html')


def outbreak_chart_data(request):
    # Group outbreaks by `purok` and collect outbreak names
    data = (
        Outbreaks.objects.values('purok')
        .annotate(
            count=Count('id'),  # Count the number of outbreaks in each purok
            outbreak_names=Count('outbreak_name')  # Collect outbreak names for each purok
        )
        .order_by('purok')  # Optional: Order by purok
    )

    # Prepare the response structure
    chart_data = {
        "labels": [item['purok'] for item in data],  # Purok labels
        "counts": [item['count'] for item in data],  # Outbreak counts
        "names": {
            item["purok"]: list(
                Outbreaks.objects.filter(purok=item["purok"]).values_list("outbreak_name", flat=True)
            )
            for item in data
        }  # Outbreak names grouped by purok
    }

    return JsonResponse(chart_data)


# ------------------------> SERVICE LIST <-----------------------

def resident_services(request):
    services = Services.objects.all()  # Query all services
    return render(request, 'resident/residentServices.html', {'services': services})


@login_required
def residentHealthRecords(request):
    # Fetch all schedules for the logged-in user
    schedules = Schedule.objects.filter(user=request.user, bhwService__service_type='immunnization')

    # Initialize list to store immunizations per schedule
    immunizations = []

    # Loop through each schedule and filter immunizations based on schedule.id
    for schedule in schedules:
        pentavalent = Immunize.objects.filter(vaccine_name="Pentavalent Vaccine", schedule_id=schedule.id)
        opv = Immunize.objects.filter(vaccine_name="Oral Polio Vaccine (OPV)", schedule_id=schedule.id)
        ipv = Immunize.objects.filter(vaccine_name="Inactivated Polio Vaccine", schedule_id=schedule.id)
        pcv = Immunize.objects.filter(vaccine_name="Pneumococcal Conjugate Vaccine", schedule_id=schedule.id)
        mmr = Immunize.objects.filter(vaccine_name="Measles, Mumps, Rubella", schedule_id=schedule.id)

        # Store the immunizations for each schedule
        immunizations.append({
            'schedule': schedule,
            'pentavalent': pentavalent,
            'opv': opv,
            'ipv': ipv,
            'pcv': pcv,
            'mmr': mmr,
        })

    return render(request, 'resident/residentHealthRecords.html', {
        'immunizations': immunizations,
    })


def residentPayment(request):
    return render(request, 'resident/residentPayment.html')

from .models import BarangayClearance, Residents
from .forms import BarangayClearanceForm
from django.contrib import messages

# Resident: Request Barangay Clearance
@login_required
def request_clearance(request):
    resident = Residents.objects.filter(auth_user=request.user).first()
    
    if not resident:
        messages.error(request, "You need to complete your profile before requesting clearance.")
        return redirect('complete_profile') 

    form = BarangayClearanceForm(request.POST or None)
    
    if form.is_valid():
        clearance = form.save(commit=False)
        clearance.resident = resident
        clearance.save()
        messages.success(request, "Barangay clearance request submitted successfully!")
        return redirect('clearance_status')

    return render(request, 'resident/request_clearance.html', {'form': form})

# Resident: View Clearance Status
@login_required
def clearance_status(request):
    resident = Residents.objects.filter(auth_user=request.user).first()
    
    if not resident:
        return render(request, 'resident/error.html', {'message': 'You are not registered as a resident.'})

    clearances = BarangayClearance.objects.filter(resident=resident)
    return render(request, 'resident/clearance_status.html', {'clearances': clearances})
