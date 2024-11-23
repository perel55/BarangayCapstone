from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login as auth_login
from django.shortcuts import render, reverse
from .models import Residents, Account_Type, Accounts
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views import View
from .models import HealthService
from django.contrib.auth.decorators import login_required
from .models import *
from django.db.models import Prefetch
from django.db.models import Sum




@csrf_exempt
def bsiregister(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password1 == password2:
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password1,
            )

            bsi = Bsi.objects.create(auth_user=user)  # Ensure the model name matches

            bsi_account_type = Account_Type.objects.get(Account_type='BSI')  # Correct the field name

            newAcc = Accounts.objects.create(
                bsi_id=bsi,  # Use bis_id to match the field in the Accounts model
                account_typeid=bsi_account_type  # Use account_typeid to match the field in the Accounts model
            )

            user = authenticate(request, username=username, password=password1)
            if user is not None:
                login(request, user)  
                return redirect('bsiDashboard')
        else:
            messages.error(request, "Passwords do not match.")

    return render(request, 'bsi/addBSI.html')

def addBSI(request):
    return render(request, 'bsi/addBSI.html')

def bsiDashboard(request):
    return render(request, 'bsi/bsiDashboard.html')

def bsiSanitary(request):
    schedules = Schedule.objects.filter(bhwService__service_type='sanitary')  
    return render(request, 'bsi/bsiSanitary.html', {'schedules': schedules}) 


@login_required
def approve_sanitary(request, schedule_id):
    schedule = get_object_or_404(Schedule, id=schedule_id)
    schedule.status = "Verified"
    schedule.save()
    return redirect('bsiSanitary')  