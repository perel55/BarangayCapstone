from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.timezone import now
# Create your models here.


    
class Residents(models.Model):
    auth_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE,  related_name="resident_profile") 
    mname = models.CharField(max_length=255)
    zone = models.CharField(max_length=255)
    civil_status = models.CharField(max_length=255)
    occupation = models.CharField(max_length=255)
    birthdate = models.DateField(max_length=255, null=True)
    phone_number = models.CharField(max_length=255)
    picture = models.ImageField(upload_to='images/', null=True)
    id_image = models.ImageField(upload_to='images/', null=True)
    is_profile_complete = models.BooleanField(default=False)
    status = models.CharField(max_length=50, default="Pending")

    def __str__(self):
        return f"{self.auth_user}"


class Personnel(models.Model):
    auth_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE) 
    mname = models.CharField(max_length=255)
    zone = models.CharField(max_length=255)
    civil_status = models.CharField(max_length=255)
    occupation = models.CharField(max_length=255)
    birthdate = models.DateField(max_length=255, null=True)
    phone_number = models.CharField(max_length=255)
    picture = models.ImageField(upload_to = 'images/', null=True)
    position = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.auth_user}"
  
class Bhw(models.Model):
    auth_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE) 
    mname = models.CharField(max_length=255)
    zone = models.CharField(max_length=255)
    civil_status = models.CharField(max_length=255)
    occupation = models.CharField(max_length=255)
    birthdate = models.DateField(max_length=255, null=True)
    phone_number = models.CharField(max_length=255)
    picture = models.ImageField(upload_to = 'images/', null=True)
    position = models.CharField(max_length=255)
 
    def __str__(self):
        return f"{self.auth_user}"



    

class Secretary(models.Model):
    auth_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE) 
    mname = models.CharField(max_length=255)
    zone = models.CharField(max_length=255)
    civil_status = models.CharField(max_length=255)
    occupation = models.CharField(max_length=255)
    birthdate = models.DateField(max_length=255, null=True)
    phone_number = models.CharField(max_length=255)
    picture = models.ImageField(upload_to = 'images/', null=True)
    position = models.CharField(max_length=255)
    is_profile_complete = models.BooleanField(default=False)
    status = models.CharField(max_length=50, default="Pending")

    def __str__(self):
        return f"{self.auth_user}"


class Account_Type(models.Model):
    Account_type = models.CharField(max_length =255)
    
    def __str__(self):
        return f"{self.Account_type}"

class Accounts(models.Model):
    resident_id = models.ForeignKey(Residents, on_delete=models.CASCADE, null=True)
    bhw_id = models.ForeignKey(Bhw, on_delete=models.CASCADE, null=True)
    admin_id = models.ForeignKey(Personnel, on_delete=models.CASCADE, null=True)
    secretary_id = models.ForeignKey(Secretary, on_delete=models.CASCADE, null=True)
    account_typeid= models.ForeignKey(Account_Type, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Resident: {self.resident_id} | Admin: {self.admin_id} | BHW: {self.bhw_id} | Account Type: {self.account_typeid}"
    
 
class HealthService(models.Model):
    service_name = models.CharField(max_length =255)
    service_description = models.CharField(max_length =255)
    service_requirements = models.CharField(max_length =255)
    picture = models.ImageField(upload_to = 'images/', null=True)
    service_type = models.CharField(max_length =255, null=True)

    def __str__(self):
        return f"{self.service_name} {self.service_description} {self.service_requirements}  {self.picture} {self.service_type}"
    
class Services(models.Model):
    service_id = models.AutoField(primary_key=True)
    service_name = models.CharField(max_length=255)
    requirements = models.CharField(max_length=255)
    service_description = models.TextField(null=True)
    service_price = models.IntegerField(null=True)
    image = models.ImageField(upload_to='images/', null=True)

    def __str__(self):
        return f"{self.service_id} {self.service_name} {self.requirements} {self.service_description} "

# models.py
class Schedule(models.Model):
    bhwService = models.ForeignKey(HealthService, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  
    resident = models.ForeignKey(Residents, on_delete=models.CASCADE, null=True)  
    status = models.CharField(max_length=50, default="Pending")
    baby_name = models.CharField(max_length=255, null=True)
    father_name = models.CharField(max_length=255, null=True)   
    mother_name = models.CharField(max_length=255, null=True)
    birth_place = models.CharField(max_length=255, null=True)
    birthdate = models.DateField(max_length=255, null=True)
    sex = models.CharField(max_length=255, null=True)
    date = models.DateField(max_length=255, null=True)
    time = models.CharField(max_length=100, null=True)


    
    def __str__(self):
        return f"{self.status} {self.baby_name} {self.father_name} {self.mother_name}"

    
class Outbreaks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    outbreak_name = models.CharField(max_length=100) 
    
    status = models.CharField(max_length=100, default="Active")   
    fname = models.CharField(max_length =255,  null=True)
    lname = models.CharField(max_length =255,  null=True)
    date = models.DateField(max_length =255, null=True)

    Purok_CHOICES = (      
        ('1A', '1A'),
        ('1B', '1B'),   
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
    )
    purok = models.CharField(max_length=100, null=True)
    def __str__(self):
        return f"{self.outbreak_name} {self.purok} "
    
    
class Request(models.Model):
    PENDING = 'Pending'
    APPROVED = 'Approved'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
    ]

    PENDING = 'Pending'
    APPROVED = 'Approved'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
    ]

    Resident_id = models.ForeignKey(Residents, on_delete=models.CASCADE, null=True)
    service_id = models.ForeignKey(Services, on_delete=models.CASCADE, null=True)
    reason = models.CharField(max_length=255)
    reason = models.CharField(max_length=255)
    total_price = models.IntegerField(null=True)
    schedule_date = models.DateField(null=True)
    schedule_start_time = models.TimeField(null=True)
    request_requirements = models.ImageField(upload_to='images/', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)

    def __str__(self):
        return f"{self.Resident_id} - {self.service_id} - {self.schedule_date}"
    
class RequestHistory(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name="history")
    status = models.CharField(max_length=20)  # e.g., Approved, Declined
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.request} - {self.status} at {self.updated_at}"

class CommunityNotice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    bhw_id = models.ForeignKey(Bhw, on_delete=models.CASCADE, null=True)
    admin_id = models.ForeignKey(Personnel, on_delete=models.CASCADE, null=True)
    notice_name = models.CharField(max_length=100)
    notice_description = models.TextField(null=True)
    notice_image = models.ImageField(upload_to = 'images/', null=True)
    notice_StartDate = models.DateField(null=True)
    notice_EndDate = models.DateField(null=True)
    notice_StartTime = models.TimeField(null=True)
    notice_EndTime = models.TimeField(null=True)
    notice_type = models.CharField(max_length=100)
    notice_color = models.CharField(max_length=7, default='#007bff')

 
    
class Maintenance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, null=True)
    resident_id = models.ForeignKey(Residents, on_delete=models.CASCADE, null=True)
    week = models.CharField(max_length=100, null=True)
    date = models.DateField(null=True)
    week = models.CharField(max_length=100, null=True)
    kg = models.IntegerField(null=True)
    bp = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=100, default="Pending", null=True)
    month = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.date} {self.week} {self.kg} {self.bp} {self.status}"


class Immunize(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, null=True)
    vaccine_name = models.CharField(max_length=100, null=True)
    vaccine_dose = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=100, default="Pending", null=True)
    at_birth = models.CharField(max_length=100, null=True)  
    status = models.CharField(max_length=100, default="Pending", null=True)
    first_visit = models.DateField(null=True, blank=True)
    second_visit = models.DateField(null=True, blank=True)
    third_visit = models.DateField(null=True, blank=True)
    fourth_visit = models.DateField(null=True, blank=True)
    fifth_visit = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.vaccine_name}"
class ResidentImmunize(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, null=True)
    immunize = models.ForeignKey(Immunize, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.schedule} {self.immunize} "
    
    
        return f"{self.vaccine_name} {self.vaccine_description} "
    
class Household(models.Model):
    name = models.CharField(max_length=255)  
    zone = models.CharField(max_length=255)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.zone}"

class Member(models.Model):
    household = models.ForeignKey(Household, on_delete=models.CASCADE, related_name="members")
    resident = models.OneToOneField('Residents', on_delete=models.CASCADE, null=True, blank=True)
    relationship_to_head = models.CharField(max_length=100)
    is_head_of_household = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.resident.auth_user.username} - {self.relationship_to_head} ({'Head' if self.is_head_of_household else 'Member'})"

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    resident = models.ForeignKey(Residents, on_delete=models.CASCADE, null=True)
    service = models.ForeignKey(Services, on_delete=models.CASCADE, null=True)
    request_id = models.ForeignKey(Request, on_delete=models.CASCADE, null=True)
    date_paid = models.DateField()
    sender_name = models.CharField(max_length=100, null=True)
    reference_number = models.CharField(max_length=100, null=True) 
    proof = models.ImageField(upload_to='images/', null=True)
    status = models.CharField(max_length=100, default="Pending")

    def __str__(self):
        return f"{self.resident} - {self.service}  - {self.date_paid}  - {self.status}"
    
class BarangayClearance(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    resident = models.ForeignKey(
        Residents, 
        on_delete=models.CASCADE, 
        related_name="clearances",
        null=True,  # Allow NULL values
        blank=True  # Allow empty values in forms
    )
    full_name = models.CharField(max_length=255, blank=True)
    age = models.IntegerField(blank=True, null=True)
    civil_status = models.CharField(max_length=20, choices=[
        ('single', 'Single'),
        ('married', 'Married'),
        ('widow', 'Widow')
    ], blank=True)
    native_of = models.CharField(max_length=255)
    purok = models.CharField(max_length=255, blank=True)
    purpose = models.TextField()
    remarks = models.CharField(max_length=255, default="No Derogatory Record and is known of Good Moral Character")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    date_requested = models.DateTimeField(default=now)

    def save(self, *args, **kwargs):
        """Auto-fill resident details before saving"""
        if self.resident:
            self.full_name = f"{self.resident.auth_user.first_name} {self.resident.auth_user.last_name}"
            self.age = self.calculate_age()
            self.civil_status = self.resident.civil_status
            self.purok = self.resident.zone  # Assuming 'zone' is the purok
            
        super().save(*args, **kwargs)

    def calculate_age(self):
        """Calculate age from birthdate"""
        if self.resident.birthdate:
            from datetime import date
            today = date.today()
            return today.year - self.resident.birthdate.year - ((today.month, today.day) < (self.resident.birthdate.month, self.resident.birthdate.day))
        return None

    def __str__(self):
        return f"{self.full_name} - {self.status}"