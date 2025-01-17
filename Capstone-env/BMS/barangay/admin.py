from django.contrib import admin
from .views.models import Accounts, Residents, Bhw, Account_Type, Personnel, HealthService, Schedule, Services, Outbreaks, Request, Bsi,HealthAdmin, Maintenance,Medicine, CommunityNotice,Immunize, Secretary, RequestHistory
from .views.models import Accounts, Residents, Bhw, Account_Type, Personnel, HealthService, Schedule, Services, Outbreaks, Request, Bsi,HealthAdmin, Maintenance,Medicine, CommunityNotice



# Register your models here.
admin.site.register(Accounts)
admin.site.register(Residents)
admin.site.register(Bhw)
admin.site.register(Account_Type)
admin.site.register(Personnel)
admin.site.register(HealthService)
admin.site.register(Schedule)
admin.site.register(Outbreaks)
admin.site.register(Request)
admin.site.register(Services)
admin.site.register(Bsi)
admin.site.register(HealthAdmin)
admin.site.register(Maintenance)
admin.site.register(Medicine)
admin.site.register(CommunityNotice)
admin.site.register(Immunize)
admin.site.register(Secretary)
admin.site.register(RequestHistory)


