from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.


    
class Residents(models.Model):
    auth_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE) 
    mname = models.CharField(max_length=255)
    zone = models.CharField(max_length=255)
    civil_status = models.CharField(max_length=255)
    occupation = models.CharField(max_length=255)
    birthdate = models.DateField(max_length=255, null=True)
    phone_number = models.CharField(max_length=255)
    picture = models.ImageField(upload_to = 'images/', null=True)
    id_image = models.ImageField(upload_to = 'images/', null=True)
    position = models.CharField(max_length=255)
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
class Bsi(models.Model):
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

class HealthAdmin(models.Model):
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
class Account_Type(models.Model):
    Account_type = models.CharField(max_length =255)
    
    def __str__(self):
        return f"{self.Account_type}"

class Accounts(models.Model):
    ha_id = models.ForeignKey(HealthAdmin, on_delete=models.CASCADE, null=True)
    resident_id = models.ForeignKey(Residents, on_delete=models.CASCADE, null=True)
    bsi_id = models.ForeignKey(Bsi, on_delete=models.CASCADE, null=True)
    bhw_id = models.ForeignKey(Bhw, on_delete=models.CASCADE, null=True)
    admin_id = models.ForeignKey(Personnel, on_delete=models.CASCADE, null=True)
    account_typeid= models.ForeignKey(Account_Type, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Resident: {self.resident_id} | Admin: {self.admin_id} | BHW: {self.bhw_id} | Account Type: {self.account_typeid}"
    
 
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
    date = models.DateField(max_length=255)
    status = models.CharField(max_length=50, default="Pending")
    baby_name = models.CharField(max_length=255, null=True)
    father_name = models.CharField(max_length=255, null=True)   
    mother_name = models.CharField(max_length=255, null=True)
    image = models.ImageField(upload_to='images/', null=True)

    
    def __str__(self):
        return f"{self.date} {self.status} {self.baby_name} {self.father_name} {self.mother_name}"

    
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

    Resident_id = models.ForeignKey(Residents, on_delete=models.CASCADE, null=True)
    service_id = models.ForeignKey(Services, on_delete=models.CASCADE, null=True)
    reason = models.CharField(max_length=255)
    total_price = models.IntegerField(null=True)
    schedule_date = models.DateField(null=True)
    schedule_start_time = models.TimeField(null=True)
    request_requirements = models.ImageField(upload_to='images/', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)

    def __str__(self):
        return f"{self.Resident_id} - {self.service_id} - {self.schedule_date}"



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

    def __str__(self):
        return f"{self.announcement_name} {self.announcement_description} {self.announcement_date} {self.announcement_time} {self.announcement_type}"
    
class Maintenance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, null=True)
    resident_id = models.ForeignKey(Residents, on_delete=models.CASCADE, null=True)
    date = models.DateField(null=True)
    week = models.CharField(max_length=100, null=True)
    kg = models.IntegerField(null=True)
    bp = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=100, default="Pending", null=True)

    def __str__(self):
        return f"{self.date} {self.week} {self.kg} {self.bp} {self.status}"


class Medicine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, null=True)
    resident_id = models.ForeignKey(Residents, on_delete=models.CASCADE, null=True)
    maintenance = models.ForeignKey(Maintenance, on_delete=models.CASCADE, null=True)
    medicine_name = models.CharField(max_length=100)
    medicine_description = models.TextField(null=True)
    medicine_quantity = models.IntegerField(null=True)
    expiration_date = models.DateField(null=True)
    medicine_type = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='images/', null=True)
    released_quantity = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.medicine_name} {self.medicine_description} {self.medicine_quantity} {self.expiration_date} {self.medicine_type} {self.picture} {self.released_quantity}"

class Immunize(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, null=True)
    resident_id = models.ForeignKey(Residents, on_delete=models.CASCADE, null=True)
    vaccine_name = models.CharField(max_length=100)
    vaccine_quantity = models.IntegerField(null=True)
    vaccine_description = models.TextField(null=True)
    vaccine_dose = models.CharField(max_length=100, null=True)
    age = models.CharField(max_length=100)
    date = models.DateField(null=True)
    status = models.CharField(max_length=100, default="Pending", null=True)
    

    def __str__(self):
        return f"{self.vaccine_name} {self.vaccine_description} "
