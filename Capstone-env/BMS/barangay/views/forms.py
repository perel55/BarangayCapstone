# forms.py
from django import forms
from .models import Residents, Member, Household, BarangayClearance

class ResidentProfileForm(forms.ModelForm):
    class Meta:
        model = Residents
        fields = ['mname',  'zone', 'civil_status', 'occupation','birthdate', 'phone_number', 'picture', 'id_image']

class HouseholdForm(forms.ModelForm):
    ZONE_CHOICES = [
        ('1A', '1A'),
        ('1B', '1B'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
    ]

    zone = forms.ChoiceField(choices=ZONE_CHOICES, label="Zone", widget=forms.Select(attrs={
        'class': 'form-control',
    }))

    class Meta:
        model = Household
        fields = ['name', 'zone']

class MemberForm(forms.ModelForm):
    resident = forms.ModelChoiceField(
        queryset=Residents.objects.all(),
        widget=forms.Select(attrs={
            "class": "autocomplete-resident",  # Target this in JavaScript
            "placeholder": "Search resident..."
        }),
        label="Resident"
    )

    class Meta:
        model = Member
        fields = ['resident', 'relationship_to_head', 'is_head_of_household']

class BarangayClearanceForm(forms.ModelForm):
    class Meta:
        model = BarangayClearance
        fields = ['purpose', 'native_of']