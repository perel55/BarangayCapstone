from django.shortcuts import render, redirect
from .models import Residents, Schedule, Request, Services
from .forms import ResidentProfileForm  # Import a form for the Residents model
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta, datetime
from django.http import JsonResponse


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

def view_events(request):
    return render(request, 'resident/residentEvents.html')




from django.http import JsonResponse
from .models import Residents

def get_resident_details(request, resident_id):
    resident = Residents.objects.get(id=resident_id)
    data = {
        "username": resident.auth_user.username,
        "email": resident.auth_user.email,
        "fname": resident.fname,
        "mname": resident.mname,
        "lname": resident.lname,
        "zone": resident.zone,
        "civil_status": resident.civil_status,
        "occupation": resident.occupation,
        "birthdate": resident.birthdate,
        "phone_number": resident.phone_number,
        "position": resident.position,
        "is_profile_complete": resident.is_profile_complete,
        "status": resident.status,
        "picture": resident.picture.url if resident.picture else None,
        "id_image": resident.id_image.url if resident.id_image else None,
    }
    return JsonResponse(data)
