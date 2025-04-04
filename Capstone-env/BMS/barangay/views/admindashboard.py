from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Prefetch


def admindashboard(request):
    return render(request, 'admin/admin.html')

def service_list(request):
    services = Services.objects.all()
    return render(request, 'admin/ServiceList.html', {'services': services})

def AddService(request):
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

        return redirect('service_list')

    return render(request, 'admin/ServiceList.html')

def update_service(request, service_id):
    service = get_object_or_404(Services, service_id=service_id)

    if request.method == "POST":
        service.service_name = request.POST.get('service_name')
        service.requirements = request.POST.get('requirements')
        service.service_description = request.POST.get('service_description')
        service.service_price = request.POST.get('service_price')

        if request.FILES.get('image'):
            service.image = request.FILES['image']

        service.save()
        return redirect('service_list')

    return render(request, 'admin/update_service.html', {'service': service})


def delete_service(request, service_id):
    service = get_object_or_404(Services, service_id=service_id)
    service.delete()
    return redirect('service_list')

def administrative_services_list(request):
    services = Services.objects.all()
    return render(request, 'admin/administrative_services_list.html', {'services': services})

def health_services_list(request):
    health_services = HealthService.objects.all()
    return render(request, 'admin/health_services_list.html', {'health_services': health_services})

def account_list(request):
    account_type = request.GET.get('type', 'all')  # Default to 'all'
    
    if account_type == 'Residents':
        accounts = Residents.objects.all()
    elif account_type == 'Bhw':
        accounts = Bhw.objects.all()
    elif account_type == 'Personnel':
        accounts = Personnel.objects.all()
    else:
        accounts = Accounts.objects.all()  # Shows all accounts if 'all' is selected

    context = {
        'accounts': accounts,
        'account_type': account_type,
    }
    return render(request, 'admin/adminAccounts.html', context)


#----------------------------> SECRETARY <-----------------------------
@login_required
def add_notice(request):
    if request.method == 'POST':
        notice_name = request.POST.get('notice_name')
        notice_description = request.POST.get('notice_description')
        notice_image = request.FILES.get('notice_image')
        notice_StartDate = request.POST.get('notice_StartDate')
        notice_EndDate = request.POST.get('notice_EndDate')
        notice_StartTime = request.POST.get('notice_StartTime')
        notice_EndTime = request.POST.get('notice_EndTime')
        notice_type = request.POST.get('notice_type')
        notice_color = request.POST.get('notice_color')

        # Get the current user
        user = request.user
        bhw_id = None  # Replace this with logic to fetch the appropriate BHW instance
        admin_id = None  # Replace this with logic to fetch the appropriate Admin instance

        # Save the notice
        CommunityNotice.objects.create(
            user=user,
            bhw_id=bhw_id,
            admin_id=admin_id,
            notice_name=notice_name,
            notice_description=notice_description,
            notice_image=notice_image,
            notice_StartDate=notice_StartDate,
            notice_EndDate=notice_EndDate,
            notice_StartTime=notice_StartTime,
            notice_EndTime=notice_EndTime,
            notice_type=notice_type,
            notice_color=notice_color,
        )

        return redirect('adminAddEvent')  # Redirect to the desired page

  

def get_notices(request):
    """API to fetch notices as events."""
    notices = CommunityNotice.objects.all()
    events = []
    for notice in notices:
        events.append({
            'id': notice.id,
            'title': notice.notice_name,
            'start': f"{notice.notice_StartDate}T{notice.notice_StartTime}",
            'end': f"{notice.notice_EndDate}T{notice.notice_EndTime}" if notice.notice_EndDate and notice.notice_EndTime else None,
            'description': notice.notice_description,
            'type': notice.notice_type,
            'color': notice.notice_color,
        })
    return JsonResponse(events, safe=False)

import json

@login_required
def edit_notice(request, notice_id):
    notice = CommunityNotice.objects.get(id=notice_id)
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            notice.notice_name = data.get('notice_name')
            notice.notice_description = data.get('notice_description')
            notice.notice_StartDate = data.get('notice_StartDate')
            notice.notice_EndDate = data.get('notice_EndDate')
            notice.notice_StartTime = data.get('notice_StartTime')
            notice.notice_EndTime = data.get('notice_EndTime')
            notice.notice_type = data.get('notice_type')
            notice.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

@csrf_exempt
def delete_notice(request, notice_id):
    notice = get_object_or_404(Notice, pk=notice_id)
    
    if request.method == 'DELETE':
        notice.delete()
        return JsonResponse({'success': True})
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)



def accounts_view(request):
     # Retrieve session data
    account_type = request.session.get('account_type', None)

    # Query Bhw accounts and count
    bhws = Bhw.objects.filter(auth_user__isnull=False).prefetch_related(
        Prefetch(
            'accounts_set', 
            queryset=Accounts.objects.filter(account_typeid__Account_type='Bhw')
        )
    )
    total_bhws = bhws.count()

    # Query Residents accounts and count
    residents = Residents.objects.filter(auth_user__isnull=False).prefetch_related(
        Prefetch(
            'accounts_set', 
            queryset=Accounts.objects.filter(account_typeid__Account_type='Resident')
        )
    )
    total_residents = residents.count()

    # Query Officials accounts and count
    officials = Personnel.objects.filter(auth_user__isnull=False).prefetch_related(
        Prefetch(
            'accounts_set', 
            queryset=Accounts.objects.filter(account_typeid__Account_type='Admin')
        )
    )
    total_officials = officials.count()

    # Prepare context data with totals
    context = {
        'account_type': account_type,
        'bhws': bhws,
        'residents': residents,
        'officials': officials,
        'total_bhws': total_bhws,
        'total_residents': total_residents,
        'total_officials': total_officials,
    }

    # Render the template with context
    return render(request, 'admin/adminAccounts.html', context)





def adminRecord(request):
    all_schedules = Schedule.objects.all().order_by('-date')
    highblood_schedules = Schedule.objects.filter(bhwService__service_name="HighBlood").order_by('-date')
    tb_schedules = Schedule.objects.filter(bhwService__service_name="TB").order_by('-date')
    immunize_schedules = Schedule.objects.filter(bhwService__service_type="immunization").order_by('-date')
    other_schedules = Schedule.objects.filter(bhwService__service_type="other").order_by('-date')
    
    return render(request, 'admin/adminHealthRecords.html', {
        'all_schedules': all_schedules,
        'highblood_schedules': highblood_schedules,
        'tb_schedules': tb_schedules,
        'immunize_schedules': immunize_schedules, 
        'other_schedules':  other_schedules, 
        
    })




def admindashboard(request):
    # Fetch data counts
    pending_residents_count = Residents.objects.filter(status='pending').count()
    pending_requests_count = Request.objects.filter(status='pending').count()
    active_outbreaks_count = Outbreaks.objects.filter(status='active').count()
    total_residents_count = Residents.objects.count()

    # Debugging: Print data to check if counts are correct
    print("Dashboard Data:", {
        "pending_residents_count": pending_residents_count,
        "pending_requests_count": pending_requests_count,
        "upcoming_notices_count": upcoming_notices_count,
        "active_outbreaks_count": active_outbreaks_count,
        "total_residents_count": total_residents_count,
    })

    return render(request, 'admin/admin.html', {
        'pending_residents_count': pending_residents_count,
        'pending_requests_count': pending_requests_count,
        'upcoming_notices_count': upcoming_notices_count,
        'active_outbreaks_count': active_outbreaks_count,
        'total_residents_count': total_residents_count,
        'show_modal': True,  # Ensure modal works if needed
    })

