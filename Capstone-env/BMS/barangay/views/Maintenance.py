from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import *

@login_required
def bhwMaintenance(request):
    # Fetch schedules for maintenance service with verified status
    schedules = Schedule.objects.filter(bhwService__service_type='maintenance', status='Verify')
    
    return render(request, 'healthAdmin/bhwMaintenance.html', {'schedules': schedules})

def releasedMaintenance(request, schedule_id):
    schedule = get_object_or_404(Schedule, id=schedule_id)

    # Fetch maintenance entries for the selected schedule
    maintenance_entries = get_maintenance_entries(schedule.id)

    context = {
        'schedule': schedule,
        'maintenance_entries': maintenance_entries,
    }
    return render(request, 'healthAdmin/HealthMaintenance.html', context)

def addMaintenance(request, schedule_id):
    schedule = get_object_or_404(Schedule, id=schedule_id)

    if request.method == "POST":
        week = request.POST.get('week')
        date = request.POST.get('date')
        kg = request.POST.get('kg')
        bp = request.POST.get('bp')

        # Create a new Maintenance object (maintenance entry)
        maintenance = Maintenance.objects.create(
            week=week,
            date=date,
            kg=kg,
            bp=bp,
            schedule=schedule
        )

        # Debugging: Check if the Maintenance object was created
        print(f"New maintenance entry created: {maintenance}")

        # Fetch all maintenance entries related to the current schedule
        maintenance_entries = get_maintenance_entries(schedule.id)

        # Re-render the page with the updated entries
        return render(request, 'healthAdmin/HealthMaintenance.html', {
            'schedule': schedule,
            'maintenance_entries': maintenance_entries
        })
    return redirect('releasedMaintenance', schedule_id=schedule.id)

def get_maintenance_entries(schedule_id):
    # Fetch all maintenance entries for the given schedule ID
    schedule = get_object_or_404(Schedule, id=schedule_id)
    maintenance_entries = Maintenance.objects.filter(schedule=schedule).order_by('week', 'date')

    # Debugging: Print the entries
    print(maintenance_entries)

    return maintenance_entries
