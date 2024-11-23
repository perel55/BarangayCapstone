from django.contrib import admin
from .views.models import Accounts, Residents, Bhw, Account_Type, Personnel, HealthService, Schedule, Request, Services



# Register your models here.
admin.site.register(Accounts)
admin.site.register(Residents)
admin.site.register(Bhw)
admin.site.register(Account_Type)
admin.site.register(Personnel)
admin.site.register(HealthService)
admin.site.register(Schedule)
admin.site.register(Request)
admin.site.register(Services)

