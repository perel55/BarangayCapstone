from .models import *
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from .models import Immunize, ImmunizeDate

@login_required
def bhwImmunize(request):
    # Fetch schedules for maintenance service with verified status
    schedules = Schedule.objects.filter(bhwService__service_type='immunization', status='Verify')
    
    return render(request, 'bhw/bhwImmunize.html', {'schedules': schedules})

def add_immunize(request):
    
    if request.method == "POST":
        vaccine_name = request.POST.get("vaccine_name")
        vaccine_dose = request.POST.get("vaccine_dose")
        at_birth = request.POST.get("at_birth")
        status = request.POST.get("status", "Pending")
        # Save the recor
        Immunize.objects.create(
            vaccine_name=vaccine_name,
            vaccine_dose=vaccine_dose,
            at_birth=at_birth,
            status=status,
        )

    return render(request, "bhw/add_immunize.html")


def Vaccine(request, schedule_id):
    schedule = get_object_or_404(Schedule, id=schedule_id)

    immunizations = Immunize.objects.filter()
    
    context = {
        'schedule': schedule,
        'immunizations': immunizations,

    }
    return render(request, 'bhw/bhwImmunizeVaccine.html', context)


from django.shortcuts import get_object_or_404, render
from django.core.exceptions import ValidationError
from django.http import HttpResponseBadRequest

def release_immunize(request, schedule_id):
    # Retrieve the schedule based on the given ID
    schedule = get_object_or_404(Schedule, id=schedule_id)

    if request.method == "POST":
        # Get the input values from the form
        first_visit = request.POST.get("first_visit")
        second_visit = request.POST.get("second_visit")
        third_visit = request.POST.get("third_visit")
        fourth_visit = request.POST.get("fourth_visit")
        fifth_visit = request.POST.get("fifth_visit")
        vaccine_name = request.POST.get("vaccine_name")  # Assume vaccine_name is passed

        # Validate date inputs
        try:
            immunize_data = ImmunizeDate.objects.create(
                schedule=schedule,
                first_visit=first_visit if first_visit else None,
                second_visit=second_visit if second_visit else None,
                third_visit=third_visit if third_visit else None,
                fourth_visit=fourth_visit if fourth_visit else None,
                fifth_visit=fifth_visit if fifth_visit else None,
            )
        except ValidationError as e:
            # Return an error response if the date is invalid
            return HttpResponseBadRequest(f"Invalid input: {e.messages}")

    immunizations = get_object_or_404(Immunize, schedule=schedule)

    return render(request, "bhw/bhwImmunizeVaccine.html", {
        'schedule': schedule,
        'immunizations': immunizations,
    })






