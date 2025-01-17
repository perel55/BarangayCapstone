# admin.py
from django.contrib import admin
from .models import Household, Member, Residents

@admin.register(Household)
class HouseholdAdmin(admin.ModelAdmin):
    list_display = ('name', 'zone', 'address', 'created_at')

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('household', 'resident', 'relationship_to_head', 'is_head_of_household')

@admin.register(Residents)
class ResidentsAdmin(admin.ModelAdmin):
    list_display = ('auth_user', 'mname', 'zone', 'civil_status', 'phone_number')
