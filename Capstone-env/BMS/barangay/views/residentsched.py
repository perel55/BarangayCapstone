from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from .models import Request, Services, Residents
from .models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.core.files.storage import FileSystemStorage
import logging

def residentSchedule(request):
    profile_picture = request.session.get('profile_picture', None)
    account_type = request.session.get('account_type', None)

    return render(request, 'resident/residentCalendar.html', {
        'profile_picture': profile_picture,
        'account_type': account_type
    })


@login_required
def ScheduleView(request):
    services = Services.objects.all()
    selected_service = None

    if request.method == "POST":
        service_id = request.POST.get('service-id')
        reason = request.POST.get('reason')
        total_price = request.POST.get('total-price')
        schedule_date = request.POST.get('schedule-date')
        schedule_start_time = request.POST.get('schedule-start-time')
        requirements_picture = request.FILES.get('requirements-picture')

        # Validate required fields
        if not (service_id and reason and total_price and schedule_date and schedule_start_time):
            messages.error(request, "Please fill all required fields.")
            return redirect('ScheduleView')

        # Get service and resident
        service = get_object_or_404(Services, pk=service_id)
        selected_service = service_id
        resident = Residents.objects.filter(auth_user=request.user).first()

        # Save file to the media folder
        request_file = None
        if requirements_picture:
            fs = FileSystemStorage()
            request_file = fs.save(requirements_picture.name, requirements_picture)

        # Save the request and associate it with the user
        new_request = Request(
            Resident_id=resident,
            service_id=service,
            reason=reason,
            total_price=total_price,
            schedule_date=schedule_date,
            schedule_start_time=schedule_start_time,
            request_requirements=request_file,
            user=request.user  # Associate the logged-in user
        )
        new_request.save()

        # Create a notification for the user
        Notification.objects.create(
            user=request.user,
            message=f"Your schedule for {service.service_name} on {schedule_date} has been created successfully."
        )

        messages.success(request, "Your schedule has been successfully created.")
        return redirect('residentPayment')

    return render(request, 'resident/ResidentCalendar.html', {'services': services, 'selected_service': selected_service})

# ----------------- NOTIFICATION ------------------------

@login_required
def update_schedule_status(request, schedule_id, new_status):
    schedule = get_object_or_404(Schedule, id=schedule_id)
    
    # Update the schedule status
    schedule.status = new_status
    schedule.save()

    # Notify the user about the status update
    Notification.objects.create(
        user=schedule.user,
        message=f"Your schedule has been {new_status.lower()}."
    )

    return redirect("schedule_list")  # Redirect to schedule list

@login_required
def get_notifications(request):
    notifications = Notification.objects.filter(user=request.user, is_read=False).order_by("-timestamp")
    
    data = {
        "notifications": [
            {"id": n.id, "message": n.message, "timestamp": n.timestamp.strftime("%Y-%m-%d %H:%M")}
            for n in notifications
        ],
        "count": notifications.count()  # Send unread notification count
    }
    
    return JsonResponse(data)



@csrf_exempt
def get_events(request):
    if not request.user.is_authenticated:
        return JsonResponse([], safe=False)  # Return an empty list for unauthenticated users

    # Fetch only the schedules belonging to the logged-in user
    schedules = Request.objects.filter(user=request.user)
    events = []
    for schedule in schedules:
        events.append({
            "id": schedule.id,
            "title": f"{schedule.service_id.service_name}",  # Display service name
            "start": f"{schedule.schedule_date}T{schedule.schedule_start_time}",  # Combine date and time
            "end": None,  # Add end time if needed
            "extendedProps": {
                "reason": schedule.reason,
                "total_price": schedule.total_price,
                "request_requirements": schedule.request_requirements.url if schedule.request_requirements else None,
                "schedule_type": "User-Specific",
                "schedule_id": schedule.id,
            }
        })
    return JsonResponse(events, safe=False)

logger = logging.getLogger(__name__)

@csrf_exempt
def delete_request(request, schedule_id):
    # Ensure the request is sent by an authenticated user
    if not request.user.is_authenticated:
        logger.warning(f"Unauthorized delete attempt for schedule {schedule_id} by user {request.user}")
        return JsonResponse({"error": "You must be logged in to delete a schedule."}, status=401)

    # Fetch the schedule
    try:
        schedule = get_object_or_404(Request, id=schedule_id)
    except Request.DoesNotExist:
        logger.error(f"Schedule with ID {schedule_id} does not exist.")
        return JsonResponse({"error": "Schedule not found."}, status=404)

    # Ensure that the logged-in user is the resident who created the schedule
    if schedule.user != request.user:
        logger.warning(f"User {request.user} tried to delete a schedule created by another user: {schedule_id}")
        return JsonResponse({"error": "You do not have permission to delete this schedule."}, status=403)

    # Delete the schedule
    schedule.delete()
    logger.info(f"Schedule {schedule_id} deleted successfully by user {request.user}")

    return JsonResponse({"message": "Schedule deleted successfully."})


def get_request_details(request, request_id):
    # Fetch the request from the database
    request_obj = get_object_or_404(Request, id=request_id)
    
    # Access the service_name from the related Services model
    service_name = request_obj.service_id.service_name
    
    # Return the request details as JSON, including the service name
    return JsonResponse({
        'id': request_obj.id,
        'reason': request_obj.reason,
        'schedule_date': request_obj.schedule_date,
        'schedule_start_time': request_obj.schedule_start_time,
        'schedule_end_time': request_obj.schedule_end_time,
        'total_price': request_obj.total_price,
        'request_requirements': request_obj.request_requirements.url if request_obj.request_requirements else None,
        'service_name': service_name,  # Adding the service name to the response
    })



def edit_resident_request(request, schedule_id):
    schedule = get_object_or_404(Request, id=schedule_id)

    if request.method == 'POST':
        # Extract data from POST
        reason = request.POST.get('reason')
        schedule_date = request.POST.get('schedule_date')
        schedule_start_time = request.POST.get('schedule_start_time')
        total_price = request.POST.get('total_price')
        request_requirements = request.FILES.get('request_requirements')

        # Validate fields
        if not reason:
            return JsonResponse({'success': False, 'error': 'Reason is required.'}, status=400)
        if not schedule_date:
            return JsonResponse({'success': False, 'error': 'Schedule date is required.'}, status=400)
        if not schedule_start_time:
            return JsonResponse({'success': False, 'error': 'Start time is required.'}, status=400)
        if not total_price or not total_price.isdigit() or int(total_price) < 0:
            return JsonResponse({'success': False, 'error': 'Invalid total price.'}, status=400)

        # Update schedule object with new values
        schedule.reason = reason
        schedule.schedule_date = schedule_date
        schedule.schedule_start_time = schedule_start_time
        schedule.total_price = int(total_price)

        # Handle file upload for 'request_requirements'
        if request_requirements:
            schedule.request_requirements = request_requirements

        # Save updated schedule
        schedule.save()

        # Respond with updated schedule data
        return JsonResponse({
            'success': True,
            'updated_schedule': {
                'id': schedule.id,
                'reason': schedule.reason,
                'schedule_date': schedule.schedule_date,
                'schedule_start_time': schedule.schedule_start_time,
                'total_price': schedule.total_price,
                'request_requirements': schedule.request_requirements.url if schedule.request_requirements else None,
            }
        })

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)



class ScheduleDataView(View):
    def get(self, request):
        today = datetime.now().date()
        schedules = Request.objects.filter(schedule_date__gte=today)
        events = []

        for schedule in schedules:
            start = f"{schedule.schedule_date}T{schedule.schedule_start_time}"
            end = f"{schedule.schedule_date}T{schedule.schedule_end_time}"
            events.append({
                'title': str(schedule.service_id.name),  # Assuming `service_id` has a `name` attribute.
                'start': start,
                'end': end,
                'extendedProps': {
                    'schedule_type': schedule.service_id.name,
                    'schedule_id': schedule.id,
                    'schedule_date': schedule.schedule_date.isoformat(),
                },
            })

        return JsonResponse(events, safe=False)

def fetch_services(request):
    services = list(Services.objects.values('service_id', 'service_name', 'service_price'))  # Include service_price
    return JsonResponse({'services': services})

