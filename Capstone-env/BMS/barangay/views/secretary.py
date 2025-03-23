from .models import *
from django.shortcuts import render, get_object_or_404, redirect
from .models import Household, Member
from .forms import HouseholdForm, MemberForm
from django.db.models import Prefetch
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from .models import Residents, Request, CommunityNotice
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.http import JsonResponse


def household_list(request):
    query = request.GET.get('q', '')  # Get the search query from the URL
    zone = request.GET.get('zone', '')  # Get the zone filter from the URL

    households_list = Household.objects.all()

    if query:
        households_list = households_list.filter(name__icontains=query)
    if zone:
        households_list = households_list.filter(zone=zone)

    paginator = Paginator(households_list, 10)  # Display 10 households per page
    page = request.GET.get('page')

    try:
        households = paginator.page(page)
    except PageNotAnInteger:
        households = paginator.page(1)
    except EmptyPage:
        households = paginator.page(paginator.num_pages)

    # Define the list of zones
    zones = ['1A', '1B', '2', '3', '4', '5', '6', '7', '8']

    return render(request, 'secretary/secHousehold.html', {
        'households': households,
        'query': query,
        'form': HouseholdForm(),
        'zone': zone,  # Pass the selected zone to the template
        'zones': zones,  # Pass the zone list to the template
    })



def household_create(request):
    if request.method == 'POST':
        form = HouseholdForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('household_list')
        else:
            # Handle form errors if needed
            messages.error(request, "Failed to create household. Please correct the errors.")
    else:
        form = HouseholdForm()
    return render(request, 'secretary/secHouseholdForm.html', {'form': form})


def household_update(request, pk):
    household = get_object_or_404(Household, pk=pk)
    if request.method == 'POST':
        form = HouseholdForm(request.POST, instance=household)
        if form.is_valid():
            form.save()
            return redirect('household_list')
    else:
        form = HouseholdForm(instance=household)
    return render(request, 'secretary/secHouseholdForm.html', {'form': form})

def household_delete(request, pk):
    household = get_object_or_404(Household, pk=pk)
    if request.method == 'POST':
        household.delete()
        return redirect('household_list')
    return render(request, 'household_confirm_delete.html', {'household': household})

def member_list(request, household_id):
    household = get_object_or_404(Household, pk=household_id)
    members = household.members.all()
    form = MemberForm()  # Create an instance of the form to pass to the template
    return render(request, 'secretary/secMemberList.html', {'household': household, 'members': members, 'form': form})

from django.db.models import Q

def member_create(request, household_id):
    household = get_object_or_404(Household, pk=household_id)
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            resident = form.cleaned_data['resident']
            
            # Check if the resident is already in another household
            existing_member = Member.objects.filter(resident=resident).exclude(household=household).first()
            if existing_member:
                messages.error(request, f"The resident {resident.auth_user.first_name} {resident.auth_user.last_name} is already a member of another household.")
                return redirect('member_list', household_id=household.id)
            
            # Save the new member
            member = form.save(commit=False)
            member.household = household
            member.save()
            messages.success(request, "Member added successfully!")
            return redirect('member_list', household_id=household.id)
        else:
            messages.error(request, "Failed to add member. Please check the form for errors.")
    else:
        form = MemberForm()
    return render(request, 'secretary/secMemberList.html', {'form': form, 'household': household})


@login_required
def resident_autocomplete(request):
    if 'term' in request.GET:  # Fetch the search term
        query = request.GET['term']
        qs = Residents.objects.filter(
            auth_user__first_name__icontains=query
        ) | Residents.objects.filter(auth_user__last_name__icontains=query)

        # Prepare results for Select2
        results = [
            {"id": resident.id, "text": f"{resident.auth_user.first_name} {resident.auth_user.last_name}"}
            for resident in qs
        ]
        return JsonResponse(results, safe=False)

    return JsonResponse([], safe=False)



def member_delete(request, member_id):
    member = get_object_or_404(Member, pk=member_id)
    if request.method == 'POST':
        member.delete()
        return redirect('member_list', household_id=member.household.id)
    return render(request, 'member_confirm_delete.html', {'member': member})

def member_detail(request, member_id):
    member = get_object_or_404(Member, pk=member_id)
    return render(request, 'secretary/secMemberDetail.html', {'member': member})



# ------------------------------------------ verify accounts --------------------------------------

def secVerifyAccounts(request):
    # Query Residents with pending, verified, or declined statuses
    residents = Residents.objects.filter(auth_user__isnull=False).prefetch_related(
        Prefetch(
            'accounts_set',
            queryset=Accounts.objects.filter(account_typeid__Account_type='Resident')
        )
    )

    context = {
        'residents': residents,
    }

    return render(request, 'secretary/secVerifyAccounts.html', context)

def approve_resident(request, resident_id):
    # Approve resident account
    resident = Residents.objects.get(id=resident_id)
    resident.status = "Verified"
    resident.save()
    return redirect('secVerifyAccounts')

def decline_resident(request, resident_id):
    # Decline resident account
    resident = Residents.objects.get(id=resident_id)
    resident.status = "Declined"
    resident.save()
    return redirect('secVerifyAccounts')


# ----------------------- ADD SERVICES ----------------------------

def secretary_service_list(request):
    services = Services.objects.all()
    return render(request, 'secretary/secServices.html', {'services': services})

def secretary_AddService(request):
    if request.method == "POST":
        service_name = request.POST.get('service_name')
        requirements = request.POST.get('requirements')
        service_description = request.POST.get('service_description')
        service_price = request.POST.get('service_price')

        image = request.FILES.get('image')

        new_service = Services(
            service_name=service_name,
            requirements=requirements,
            service_description=service_description,
            service_price=service_price,
            image=image,
        )
        new_service.save()
    
        return redirect('secretary_service_list')

    return render(request, 'secretary/secServices.html')

def secretary_update_service(request, service_id):
    service = get_object_or_404(Services, service_id=service_id)

    if request.method == "POST":
        service.service_name = request.POST.get('service_name')
        service.requirements = request.POST.get('requirements')
        service.service_description = request.POST.get('service_description')
        service.service_price = request.POST.get('service_price')

        if request.FILES.get('image'):
            service.image = request.FILES['image']

        service.save()
        return redirect('secretary_service_list')

    return render(request, 'admin/update_service.html', {'service': service})


def secretary_delete_service(request, service_id):
    service = get_object_or_404(Services, service_id=service_id)
    service.delete()
    return redirect('secretary_service_list')


# ------------------------------ Request ---------------------------

def secretary_Certificates(request):
    # Fetch only pending requests
    requests = Request.objects.filter(status='Pending')
    return render(request, 'secretary/secretaryRequest.html', {'requests': requests})

def secretary_update_request_status(request, request_id):
    req = Request.objects.get(id=request_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        req.status = new_status
        req.save()

        messages.success(request, f"Request status updated to {new_status}.")

        return redirect('secretary_Certificates')  

    return redirect('secretary_Certificates')  

def secretary_update_request_status(request, request_id):
    req = get_object_or_404(Request, id=request_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if req.status != new_status:  # Only act if the status has changed
            # Update the status
            req.status = new_status
            req.save()

            # Log the change in RequestHistory
            RequestHistory.objects.create(
                request=req,
                status=new_status,
                updated_by=request.user  # Assuming you track who made the change
            )

            messages.success(request, f"Request status updated to {new_status}.")

        return redirect('secretary_Certificates')

    return redirect('secretary_Certificates')

def request_details(request, request_id):
    req = Request.objects.get(id=request_id)
    history = req.history.all().order_by('-updated_at')  # Get request history

    return render(request, 'Secretary/SecretaryRequestDetails.html', {'request': req, 'history': history})

def secretary_request_history(request):
    # Fetch all requests that are either Approved or Declined
    history_requests = Request.objects.filter(status__in=['Approved', 'Declined']).order_by('-schedule_date')
    return render(request, 'secretary/requestHistory.html', {'history_requests': history_requests})


# ------------------ DASHBOARD VIEW -----------------------------




# ------------------- Edit Profile ---------------------------------
@login_required
def edit_secretary_profile(request):
    secretary = get_object_or_404(Secretary, auth_user=request.user)

    if request.method == "POST":
        secretary.mname = request.POST.get('mname', secretary.mname)
        secretary.zone = request.POST.get('zone', secretary.zone)
        secretary.civil_status = request.POST.get('civil_status', secretary.civil_status)
        secretary.occupation = request.POST.get('occupation', secretary.occupation)

        birthdate_str = request.POST.get('birthdate', secretary.birthdate)
        if birthdate_str:
            secretary.birthdate = datetime.strptime(birthdate_str, '%Y-%m-%d').date()

        secretary.phone_number = request.POST.get('phone_number', secretary.phone_number)
        if 'picture' in request.FILES:
            secretary.picture = request.FILES['picture']

        secretary.is_profile_complete = True
        secretary.save()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'message': 'Profile updated successfully'}, status=200)

        return redirect('edit_secretary_profile')

    birthdate_str = secretary.birthdate.strftime('%Y-%m-%d') if secretary.birthdate else ""
    return render(request, 'secretary/secEditProfile.html', {'secretary': secretary, 'birthdate_str': birthdate_str})
