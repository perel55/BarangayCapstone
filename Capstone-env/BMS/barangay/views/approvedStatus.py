from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Schedule
from django.shortcuts import get_object_or_404, redirect
from .models import Payment

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


def approve_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    payment.status = "Completed"
    payment.save()
    return redirect('adminPayment')  

def decline_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    payment.status = "Incomplete"
    payment.save()
    return redirect('adminPayment')