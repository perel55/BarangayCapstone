from django.contrib import admin
from .views.models import Accounts, Residents, Bhw, Account_Type, Personnel, HealthService, Schedule, Services, Outbreaks, Request, Maintenance, CommunityNotice,Immunize, Secretary, RequestHistory, Household
from .views.models import Accounts, Residents, Bhw, Account_Type, Personnel, HealthService, Schedule, Services, Outbreaks, Request, Maintenance, CommunityNotice,Immunize, Secretary, RequestHistory, Household,Payment, BarangayClearance



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
admin.site.register(Maintenance)
admin.site.register(CommunityNotice)
admin.site.register(Immunize)
admin.site.register(Secretary)
admin.site.register(RequestHistory)
admin.site.register(Household)
admin.site.register(BarangayClearance)

admin.site.register(Payment)



