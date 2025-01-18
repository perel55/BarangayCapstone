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
def healthAdminreg(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        if password1 == password2:
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name,
            )

            healthAdmin = HealthAdmin.objects.create(auth_user=user)  # Ensure the model name matches

            healthAdmin_account_type = Account_Type.objects.get(Account_type='HealthAdmin')  # Correct the field name

            newAcc = Accounts.objects.create(
                ha_id=healthAdmin, 
                account_typeid=healthAdmin_account_type  
            )

            user = authenticate(request, username=username, password=password1)
            if user is not None:
                login(request, user)  
                return redirect('healthDashboard')
        else:
            messages.error(request, "Passwords do not match.")

    return render(request, 'healthAdmin/addHA.html')

def addHA(request):
    return render(request, 'healthAdmin/addHA.html')

def healthDashboard(request):
    return render(request, 'healthAdmin/healthDashboard.html')





#add service 



