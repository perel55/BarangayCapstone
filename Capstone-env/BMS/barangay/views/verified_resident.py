from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Residents
"""
@login_required
def approved_resident(request, resident_id):
    resident = get_object_or_404(Residents, id=resident_id)
    resident.status = "Verify"
    resident.save()
    return redirect('bhwList') 

@login_required
def declined_resident(request, resident_id):
    resident = get_object_or_404(Residents, id=resident_id)
    resident.status = "Decline"
    resident.save()
    return redirect('bhwList')  
"""