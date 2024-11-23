from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Schedule

@login_required
def bhwMaintenance(request):
    # Fetch schedules with related HealthService records having service_type "maintenance"
    schedules = Schedule.objects.filter(bhwService__service_type='maintenance', status='Verified')
    
    return render(request, 'healthAdmin/bhwMaintenance.html', {'schedules': schedules})

