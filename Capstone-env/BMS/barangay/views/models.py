from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.

class Residents(models.Model):
    auth_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE) 
    fname = models.CharField(max_length=255)
    mname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    zone = models.CharField(max_length=255)
    civil_status = models.CharField(max_length=255)
    occupation = models.CharField(max_length=255)
    age = models.IntegerField(null=True, blank=True)
    birthdate = models.DateField(max_length=255, null=True)
    phone_number = models.CharField(max_length=255)
    picture = models.ImageField(upload_to = 'images/', null=True)
    position = models.CharField(max_length=255)
    is_profile_complete = models.BooleanField(default=False)
    status = models.CharField(max_length=50, default="Pending")


    def __str__(self):
        return f"{self.auth_user}"

class Personnel(models.Model):
    auth_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE) 
    fname = models.CharField(max_length=255)
    mname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    zone = models.CharField(max_length=255)
    civil_status = models.CharField(max_length=255)
    occupation = models.CharField(max_length=255)
    age = models.IntegerField(null=True, blank=True)
    birthdate = models.DateField(max_length=255, null=True)
    phone_number = models.CharField(max_length=255)
    picture = models.ImageField(upload_to = 'images/', null=True)
    position = models.CharField(max_length=255)

def __str__(self):
        return f"{self.auth_user}"
  
class Bhw(models.Model):
    auth_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE) 
    fname = models.CharField(max_length=255)
    mname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    zone = models.CharField(max_length=255)
    civil_status = models.CharField(max_length=255)
    occupation = models.CharField(max_length=255)
    age = models.IntegerField(null=True, blank=True)
    birthdate = models.DateField(max_length=255, null=True)
    phone_number = models.CharField(max_length=255)
    picture = models.ImageField(upload_to = 'images/', null=True)
    position = models.CharField(max_length=255)
 
    def __str__(self):
        return f"{self.auth_user}"
class Bsi(models.Model):
    auth_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE) 
    fname = models.CharField(max_length=255)
    mname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    zone = models.CharField(max_length=255)
    civil_status = models.CharField(max_length=255)
    occupation = models.CharField(max_length=255)
    age = models.IntegerField(null=True, blank=True)
    birthdate = models.DateField(max_length=255, null=True)
    phone_number = models.CharField(max_length=255)
    picture = models.ImageField(upload_to = 'images/', null=True)
    position = models.CharField(max_length=255)

def __str__(self):
        return f"{self.auth_user}"

class HealthAdmin(models.Model):
    auth_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE) 
    fname = models.CharField(max_length=255)
    mname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    zone = models.CharField(max_length=255)
    civil_status = models.CharField(max_length=255)
    occupation = models.CharField(max_length=255)
    age = models.IntegerField(null=True, blank=True)
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
    officials_id= models.ForeignKey(Personnel, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.service_id} {self.service_name} {self.requirements} {self.service_description} "

# models.py
class Schedule(models.Model):
    bhwService = models.ForeignKey(HealthService, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  
    resident = models.ForeignKey(Residents, on_delete=models.CASCADE, null=True)  
    date = models.DateField(max_length=255)
    status = models.CharField(max_length=50, default="Pending")

    def __str__(self):
        return f"{self.date}"

    
    
    
class Outbreaks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    outbreak_name = models.CharField(max_length=100) 
    total_cases =  models.IntegerField(null=True, blank=True)
    purok = models.CharField(max_length=100, null=True)
    severity = models.CharField(max_length=100, null=True)   
    fname = models.CharField(max_length =255,  null=True)
    lname = models.CharField(max_length =255,  null=True)
    date = models.DateField(max_length =255, null=True)

    def __str__(self):
        return f"{self.outbreak_name} {self.purok} "
class Request(models.Model):
    Resident_id = models.ForeignKey(Residents, on_delete=models.CASCADE, null=True)
    service_id = models.ForeignKey(Services, on_delete=models.CASCADE, null=True)
    reason = models.CharField(max_length =255)
    total_price = models.IntegerField(null=True)
    schedule_date = models.DateField(null=True)
    schedule_start_time = models.TimeField(null=True)
    schedule_end_time = models.TimeField(null=True)
    
    def __str__(self):
        return f"{self.Resident_id} {self.service_id} {self.schedule_date}"


class Announcement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    bhw_id = models.ForeignKey(Bhw, on_delete=models.CASCADE, null=True)
    admin_id = models.ForeignKey(Personnel, on_delete=models.CASCADE, null=True)
    announcement_name = models.CharField(max_length=100)
    announcement_description = models.TextField(null=True)
    announcement_date = models.DateField(null=True)
    announcement_time = models.TimeField(null=True)
    announcement_type = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.announcement_name} {self.announcement_description} {self.announcement_date} {self.announcement_time} {self.announcement_type}"