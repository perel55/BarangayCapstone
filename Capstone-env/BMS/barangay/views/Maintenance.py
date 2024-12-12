from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
import json


@login_required
def bhwMaintenance(request):
    # Fetch schedules for maintenance service with verified status
    schedules = Schedule.objects.filter(bhwService__service_type='maintenance', status='Verify')
    
    return render(request, 'bhw/bhwMaintenance.html', {'schedules': schedules})

def releasedMaintenance(request, schedule_id):
    schedule = get_object_or_404(Schedule, id=schedule_id)

    # Fetch maintenance entries for the selected schedule
    maintenance_entries, total_weeks = get_maintenance_entries(schedule.id)

    # Prepare data for the graph
    graph_data = {
        'weeks': list(maintenance_entries.values_list('week', flat=True).distinct()),
        'weights': list(maintenance_entries.values_list('kg', flat=True)),
        'bp_readings': list(maintenance_entries.values_list('bp', flat=True)),
    }

    context = {
        'schedule': schedule,
        'maintenance_entries': maintenance_entries,
        'total_weeks': total_weeks,
        'graph_data': json.dumps(graph_data, cls=DjangoJSONEncoder),  # Pass JSON data
    }
    return render(request, 'bhw/HealthMaintenance.html', context)

def addMaintenance(request, schedule_id):
    schedule = get_object_or_404(Schedule, id=schedule_id)

    if request.method == "POST":
        week = request.POST.get('week')
        date = request.POST.get('date')
        kg = request.POST.get('kg')
        bp = request.POST.get('bp')

       
        maintenance = Maintenance.objects.create(
            week=week,
            date=date,
            kg=kg,
            bp=bp,
            schedule=schedule
        )

        maintenance_entries, total_weeks = get_maintenance_entries(schedule.id)

        return render(request, 'bhw/HealthMaintenance.html', {
            'schedule': schedule,
            'maintenance_entries': maintenance_entries,
            'total_weeks': total_weeks,  
        })
    return redirect('releasedMaintenance', schedule_id=schedule.id)

def get_maintenance_entries(schedule_id):
    schedule = get_object_or_404(Schedule, id=schedule_id)
    maintenance_entries = Maintenance.objects.filter(schedule=schedule).order_by('week', 'date')


    total_weeks = maintenance_entries.values_list('week', flat=True).distinct().count()

    return maintenance_entries, total_weeks
