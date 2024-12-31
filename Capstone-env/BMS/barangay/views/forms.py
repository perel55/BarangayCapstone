# forms.py
from django import forms
from .models import Residents, Member, Household

class ResidentProfileForm(forms.ModelForm):
    class Meta:
        model = Residents
        fields = ['mname',  'zone', 'civil_status', 'occupation','birthdate', 'phone_number', 'picture', 'id_image', 'position']

class HouseholdForm(forms.ModelForm):
    class Meta:
        model = Household
        fields = ['name', 'address', 'zone']

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['resident', 'relationship_to_head', 'is_head_of_household']