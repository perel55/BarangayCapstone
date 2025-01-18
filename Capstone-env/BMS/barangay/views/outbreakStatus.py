from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Outbreaks

@login_required
def  active_status(request, outbreak_id):
    outbreak = get_object_or_404(Outbreaks, id=outbreak_id)
    outbreak.status = "Active"
    outbreak.save()
    return redirect('bhwOutbreak') 

@login_required
def  inactive_status(request, outbreak_id):
    outbreak = get_object_or_404(Outbreaks, id=outbreak_id)
    outbreak.status = "Inactive"
    outbreak.save()
    return redirect('bhwOutbreak') 