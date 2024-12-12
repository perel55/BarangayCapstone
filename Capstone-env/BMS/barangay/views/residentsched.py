from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from .models import Request, Services, Residents
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader


def residentSchedule(request):
    profile_picture = request.session.get('profile_picture', None)
    account_type = request.session.get('account_type', None)

    return render(request, 'resident/residentCalendar.html', {
        'profile_picture': profile_picture,
        'account_type': account_type
    })


def ScheduleView(request):
    services = Services.objects.all()  # Get all services
    selected_service = None

    if request.method == "POST":
        service_id = request.POST.get('service-id')
        reason = request.POST.get('reason')
        total_price = request.POST.get('total-price')
        schedule_date = request.POST.get('schedule-date')
        schedule_start_time = request.POST.get('schedule-start-time')
        service_requirements = request.POST.get('service-requirements')

        # Ensure valid data before proceeding
        if not (service_id and reason and total_price and schedule_date and schedule_start_time and service_requirements):
            messages.error(request, "Please fill all required fields.")
            return redirect('ScheduleView')

        service = get_object_or_404(Services, pk=service_id)
        selected_service = service_id  # Store the selected service ID

        # Check if user has a resident profile
        resident = Residents.objects.filter(auth_user=request.user).first()

        new_request = Request(
            Resident_id=resident,
            service_id=service,
            reason=reason,
            total_price=total_price,
            schedule_date=schedule_date,
            schedule_start_time=schedule_start_time,
            service_requirements=service_requirements,
        )
        new_request.save()

        messages.success(request, "Your schedule has been successfully created.")
        return redirect('ScheduleView')

    return render(request, 'resident/ResidentCalendar.html', {'services': services, 'selected_service': selected_service})



@csrf_exempt
def get_events(request):
    events = Request.objects.all()
    event_data = []
    for event in events:
        event_data.append({
            'id': event.id,
            'title': event.service_id.service_name,
            'start': f"{event.schedule_date}T{event.schedule_start_time}",
            'end': f"{event.schedule_date}T{event.schedule_end_time}",
            'extendedProps': {
                'schedule_id': event.id,
                'schedule_type': 'Not-Available',  # Assuming it's not available for booking after scheduling
            }
        })
    return JsonResponse(event_data, safe=False)

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

