from .models import *
from django.shortcuts import render, get_object_or_404, redirect,  HttpResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from .models import Immunize, Schedule
from django.shortcuts import redirect
from django.core.exceptions import ValidationError
from django.http import JsonResponse


def add_immunize(request, schedule_id):
    if request.method == "POST":
        # Retrieve the schedule instance
        schedule = get_object_or_404(Schedule, id=schedule_id)

        # Get form data
        vaccine_name = request.POST.get('vaccine_name')
        first_visit = request.POST.get('first_visit') or None
        second_visit = request.POST.get('second_visit') or None
        third_visit = request.POST.get('third_visit') or None
        fourth_visit = request.POST.get('fourth_visit') or None
        fifth_visit = request.POST.get('fifth_visit') or None

        # Check if a record with the same vaccine name exists for the schedule
        existing_immunize = Immunize.objects.filter(schedule=schedule, vaccine_name=vaccine_name).first()

        if existing_immunize:
            # Loop through the visits and clear the existing values if the new values are provided
            if first_visit is not None:
                existing_immunize.first_visit = first_visit
            if second_visit is not None:
                existing_immunize.second_visit = second_visit
            if third_visit is not None:
                existing_immunize.third_visit = third_visit
            if fourth_visit is not None:
                existing_immunize.fourth_visit = fourth_visit
            if fifth_visit is not None:
                existing_immunize.fifth_visit = fifth_visit

            try:
                # Save the updated record
                existing_immunize.save()
                return redirect('Vaccine', schedule_id=schedule_id)  # Replace with your success URL
            except ValidationError as e:
                # Handle validation errors
                return render(request, 'bhw/bhwImmunizeVaccine.html', {'error': e.messages})
        else:
            # Create a new immunization record if no existing one is found
            try:
                immunize = Immunize.objects.create(
                    schedule=schedule,
                    vaccine_name=vaccine_name,
                    first_visit=first_visit,
                    second_visit=second_visit,
                    third_visit=third_visit,
                    fourth_visit=fourth_visit,
                    fifth_visit=fifth_visit,
                )
                immunize.save()
                return redirect('Vaccine', schedule_id=schedule_id)  # Replace with your success URL
            except ValidationError as e:
                # Handle validation errors
                return render(request, 'bhw/bhwImmunizeVaccine.html', {'error': e.messages})

    # Redirect for non-POST requests
    return redirect('Vaccine')  # Replace with your error URL


    
def Vaccine(request, schedule_id):
    # Retrieve the schedule instance
    schedule = get_object_or_404(Schedule, id=schedule_id)

    # Fetch immunizations linked to this schedule
    immunizations = Immunize.objects.filter(schedule_id=schedule_id)

    # Pass the schedule and related immunizations to the template
    context = {
        'schedule': schedule,
        'immunizations': immunizations,
    }
    return render(request, 'bhw/bhwImmunizeVaccine.html', context)

def bhwReport(request):
    # Fetch all schedules
    schedules = Schedule.objects.filter(bhwService__service_type='immunnization')

    # Initialize lists to store immunizations per schedule
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

    return render(request, 'bhw/bhwReports.html', {
        'immunizations': immunizations,
    })


  





