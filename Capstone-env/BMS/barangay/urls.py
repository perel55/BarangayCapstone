from django.urls import path, re_path
from .import views
from django.views.generic import TemplateView
from django.urls import path, include  # new
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', include('allauth.urls')),
    re_path(r'^validatelogin/$', views.validatelogin, name='validatelogin'),
    re_path(r'^register$', views.register, name='register'),
    re_path(r'^residentDashboard/$', views.residentdashboard, name='residentdashboard'),
    re_path('accounts/logout/', views.logout, name='logout'),
    re_path(r'^admindashboard/$', views.admindashboard, name='admindashboard'),
    re_path(r'^admin/accounts/$', views.adminAccounts, name='adminAccounts'),
    re_path(r'^admin/service/$', views.adminService, name='adminService'),
    re_path(r'^admin/certificates/$', views.adminCertificates, name='adminCertificates'),
    re_path(r'^admin/event/$', views.adminEvent, name='adminEvent'),
    re_path(r'^admin/payment/$', views.adminPayment, name='adminPayment'),
    re_path(r'^admin/resident/$', views.adminResident, name='adminResident'),
    re_path(r'^admin/addAdmin/$', views.addAdmin, name='addAdmin'),
    re_path(r'^adminregister$', views.adminregister, name='adminregister'),






    #----------------------------------------Bhw------------------------------------------------
    re_path(r'^bhwDashboard/$', views.bhwDashboard, name='bhwDashboard'),
    re_path(r'^bhwOutbreak/$', views.bhwOutbreak, name='bhwOutbreak'),
    re_path('bhw/addOutbreak/', views.addOutbreak, name = 'addOutbreak'),
    re_path(r'^update-outbreak/$', views.updateOutbreak, name='updateOutbreak'),
    re_path(r'^addBhw/$', views.addBhw, name='addBhw'),
    re_path(r'^bhwregister$', views.bhwregister, name='bhwregister'),
    re_path(r'^healthAdminreg$', views.healthAdminreg, name='healthAdminreg'),  
    re_path(r'^healthDashboard/$', views.healthDashboard, name='healthDashboard'),
    re_path(r'^addHA/$', views.addHA, name='addHA'),
    re_path('bhwList/', views.bhwList, name = 'bhwList'),
    re_path(r'^bhwService/$', views.bhwService, name='bhwService'),
    re_path(r'^bhwRecord/$', views.bhwRecord, name='bhwRecord'),
    re_path(r'^bhwMedic/$', views.bhwMedic, name='bhwMedic'),
    re_path('bhw/addservice/', views.addHealthservice, name = 'addHealthservice'),
    re_path('bhwEvents/', views.bhwEvents, name = 'bhwEvents'),
    re_path(r'^resident/service/$', views.bhwServices, name='bhwServices'),
    re_path(r'^delete_healthservice/(?P<HealthService_id>\d+)/$', views.delete_healthservice, name='deleteHealthservice'),
    re_path(r'^bhw/UpdateService/$', views.updateHealthservice, name='updateHealthservice'),
    re_path('bhwMaintenance/', views.bhwMaintenance, name = 'bhwMaintenance'),
    re_path(r'^approve-schedule/(?P<schedule_id>\d+)/$', views.approve_schedule, name='approve_schedule'),
    re_path(r'^reject-schedule/(?P<schedule_id>\d+)/$', views.reject_schedule, name='reject_schedule'),
    re_path(r'^approve-resident/(?P<resident_id>\d+)/$', views.approved_resident, name='approved_resident'),
    re_path(r'^declined-resident/(?P<resident_id>\d+)/$', views.declined_resident, name='declined_resident'),

    re_path(r'^releasedMaintenance/(?P<schedule_id>\d+)/$', views.releasedMaintenance, name='releasedMaintenance'),
    re_path(r'^addMaintenance/(?P<schedule_id>\d+)/$', views.addMaintenance, name='addMaintenance'),
    

    re_path(r'^active-status/(?P<outbreak_id>\d+)/$', views.active_status, name='active_status'),
    re_path(r'^inactive-status/(?P<outbreak_id>\d+)/$', views.inactive_status, name='inactive_status'),
    re_path(r'^addMedicine/$', views.addMedicine, name='addMedicine'),
    re_path(r'^update_maintenance/$', views.update_maintenance, name='update_maintenance'),




 #----------------------------------------BIS------------------------------------------------
     re_path(r'^addBSI/$', views.addBSI, name='addBSI'),
     re_path(r'^bsiDashboard/$', views.bsiDashboard, name='bsiDashboard'),
     re_path(r'^bsiregister$', views.bsiregister, name='bsiregister'),
     re_path(r'^bhwSanitary/$', views.bhwSanitary, name='bhwSanitary'),
     re_path(r'^approve_sanitary/(?P<schedule_id>\d+)/$', views.approve_sanitary, name='approve_sanitary'),
    
    
    
    


     #----------------------------------------Resident------------------------------------------------

    re_path(r'^bhw/book_healthServiceform/(?P<HealthService_id>\d+)/$', views.book_healthServiceform, name='book_healthServiceform'),
    re_path(r'^bhw/book_healthService/(?P<HealthService_id>\d+)/(?P<resident_id>\d+)/$', views.book_healthService, name='book_healthService'),
    re_path(r'^residentHistory/$', views.residentHistory, name='residentHistory'),
    re_path(r'^get_resident_details/(?P<resident_id>\d+)/$', views.get_resident_details, name='get_resident_details'),
    










     #----------------------------------------Erwin------------------------------------------------
    re_path(r'^AddService/$', views.AddService, name='AddService'),
    re_path(r'^service_list/$', views.service_list, name='service_list'),
    re_path(r'^service/update/<int:service_id>/$', views.update_service, name='update_service'),
    re_path(r'^service/delete/<int:service_id>/$', views.delete_service, name='delete_service'),
    re_path(r'^administrative-services/$', views.administrative_services_list, name='administrative_services_list'),
    re_path(r'^health-services/$', views.health_services_list, name='health_services_list'),

    re_path(r'^service/update/(?P<service_id>\d+)/$', views.update_service, name='update_service'),
    re_path(r'^service/delete/(?P<service_id>\d+)/$', views.delete_service, name='delete_service'),
    re_path(r'^administrative-services/$', views.administrative_services_list, name='administrative_services_list'),
    re_path(r'^health-services/$', views.health_services_list, name='health_services_list'),

    
    path('calendar/', views.calendar_view, name='calendar'),  # Calendar view for residents
    path('calendar/events/', views.get_events, name='calendar_events'),  # API to fetch events
    path('calendar/create/', views.create_event, name='create_event'),  # API to create an event
    path('api/get_services/', views.get_services, name='get_services'),



# -------------> TRY <------------
    # re_path(r'^ScheduleView/$', views.ScheduleView.as_view(), name='ScheduleView'),
    path('resident/schedule/', views.residentSchedule, name='residentSchedule'),

    path('schedule/', views.ScheduleView, name='ScheduleView'),
    path('api/schedules/', views.get_events, name='GetEvents'),




] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)