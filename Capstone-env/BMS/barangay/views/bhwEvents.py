"""
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from .models import Announcement
from django.http import JsonResponse

class BhwEventsView(View): 
    def post(self, request):
        announcement_name = request.POST.get('announcement_name')
        announcement_description = request.POST.get('announcement_description')
        announcement_time = request.POST.get('announcement_time')
        announcement_type = request.POST.get('announcement_type')
        announcement_date = request.POST.get('announcement_date')
        
        if not all([announcement_name, announcement_description, announcement_time, announcement_type, announcement_date]):
            messages.error(request, 'All fields are required.')
            return redirect('bhwEvents')

        # Check for overlapping announcement
        overlapping_announcement = Announcement.objects.filter(
            announcement_name=announcement_name,
            announcement_time=announcement_time,
            announcement_type=announcement_type,
            announcement_date=announcement_date,
        )

        if overlapping_announcement.exists():
            messages.error(request, 'This event overlaps with an existing schedule.')
            return redirect('bhwEvents')

        try:
            announcement = Announcement(
                announcement_name=announcement_name,
                announcement_description=announcement_description,
                announcement_time=announcement_time,
                announcement_type=announcement_type,
                announcement_date=announcement_date,
            )
            announcement.save()
            messages.success(request, 'Announcement/Event added successfully!')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')

        return redirect('bhwEvents')

class AnnouncementDataView(View):
    def get(self, request):
        today = datetime.now().date()
        
        # Filter for today or future announcements
        announcements = Announcement.objects.filter(announcement_date__gte=today)
        events = []

        for announcement in announcements:
            start = f"{announcement.announcement_date}T{announcement.announcement_time}" if announcement.announcement_date and announcement.announcement_time else None
            
            events.append({
                'title': announcement.announcement_name,
                'start': start,
                'extendedProps': {
                    'description': announcement.announcement_description,
                    'type': announcement.announcement_type,
                    'id': announcement.id,
                    'date': announcement.announcement_date.isoformat() if announcement.announcement_date else None,
                },
            })

        return JsonResponse(events, safe=False)
"""