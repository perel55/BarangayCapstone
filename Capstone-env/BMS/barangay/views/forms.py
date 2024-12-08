# forms.py
from django import forms
from .models import Residents

class ResidentProfileForm(forms.ModelForm):
    class Meta:
        model = Residents
        fields = ['fname', 'mname', 'lname', 'zone', 'civil_status', 'occupation','birthdate', 'phone_number', 'picture', 'id_image', 'position']
