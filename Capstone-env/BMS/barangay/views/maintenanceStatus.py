from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *

@login_required
def complete_maintenance(request, maintenance_id):
    maintenance = get_object_or_404(Maintenance, id=maintenance_id)
    maintenance.status = "Complete"
    maintenance.save()

    # Pass the required 'schedule_id' to the redirect
    return redirect('releasedMaintenance', schedule_id=maintenance.schedule_id)

@login_required
def incomplete_maintenance(request, maintenance_id):
    maintenance = get_object_or_404(Maintenance, id=maintenance_id)
    maintenance.status = "Incomplete"
    maintenance.save()

    # Pass the required 'schedule_id' to the redirect
    return redirect('releasedMaintenance', schedule_id=maintenance.schedule_id)
