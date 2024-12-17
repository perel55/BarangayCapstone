from .models import *
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

@login_required
def bhwImmunize(request):
    # Fetch schedules for maintenance service with verified status
    schedules = Schedule.objects.filter(bhwService__service_type='immunization', status='Verify')
    
    return render(request, 'bhw/bhwImmunize.html', {'schedules': schedules})

def addImmunize(request, schedule_id):
    schedule = get_object_or_404(Schedule, id=schedule_id)

    if request.method == "POST":
        # Retrieve data from the form
        vaccine_name = request.POST.get('vaccine_name')
        vaccine_description = request.POST.get('vaccine_description')
        vaccine_dose = request.POST.get('vaccine_dose')
        vaccine_quantity = request.POST.get('vaccine_quantity')
        age = request.POST.get('age')
        date = request.POST.get('date')
        
        # Create a new Immunize record
        Immunize.objects.create(
            vaccine_name=vaccine_name,
            vaccine_description=vaccine_description,
            vaccine_dose=vaccine_dose,
            vaccine_quantity=vaccine_quantity,
            age=age,
            date=date,
            schedule=schedule
        )
        
        # Fetch the updated immunize entries
        immunize_entries = get_immunize_entries(schedule.id)

        # Render the same template with updated data
        return render(request, 'bhw/bhwImmunizeVaccine.html', {
            'schedule': schedule,
            'immunize_entries': immunize_entries,  # Updated entries
        })
    
    # In case of a GET request, redirect back to Vaccine view
    return redirect('Vaccine', schedule_id=schedule.id)


def Vaccine(request, schedule_id):
    schedule = get_object_or_404(Schedule, id=schedule_id)

    immunize_entries = get_immunize_entries(schedule.id)

    context = {
        'schedule': schedule,
        'immunize_entries':immunize_entries,

    }
    return render(request, 'bhw/bhwImmunizeVaccine.html', context)

def get_immunize_entries(schedule_id):
    schedule = get_object_or_404(Schedule, id=schedule_id)
    immunize_entries = Immunize.objects.filter(schedule=schedule).order_by('vaccine_dose', 'date')

    return immunize_entries


@login_required
def complete_immunize(request, immunize_id):
    immunize = get_object_or_404(Immunize, id=immunize_id)
    immunize.status = "Complete"
    immunize.save()

    # Pass the required 'schedule_id' to the redirect
    return redirect('Vaccine', schedule_id=immunize.schedule_id)

@login_required
def incomplete_immunize(request, immunize_id):
    immunize = get_object_or_404(Immunize, id=immunize_id)
    immunize.status = "Incomplete"
    immunize.save()

    # Pass the required 'schedule_id' to the redirect
    return redirect('Vaccine', schedule_id= immunize.schedule_id)