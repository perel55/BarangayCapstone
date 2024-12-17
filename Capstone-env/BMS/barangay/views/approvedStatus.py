from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Schedule

@login_required
def approve_schedule(request, schedule_id):
    schedule = get_object_or_404(Schedule, id=schedule_id)
    schedule.status = "Verify"
    schedule.save()
    return redirect('bhwRecord') 

@login_required
def reject_schedule(request, schedule_id):
    schedule = get_object_or_404(Schedule, id=schedule_id)
    schedule.status = "Decline"
    schedule.save()
    return redirect('bhwRecord')  
