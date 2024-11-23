from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.

class Residents(models.Model):
    auth_user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, default=1)
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
class Account_Type(models.Model):
    Account_type = models.CharField(max_length =255)
    
    def __str__(self):
        return f"{self.Account_type}"

class Accounts(models.Model):
    resident_id = models.ForeignKey(Residents, on_delete=models.CASCADE, null=True)
    bhw_id = models.ForeignKey(Bhw, on_delete=models.CASCADE, null=True)
    admin_id = models.ForeignKey(Personnel, on_delete=models.CASCADE, null=True)
    account_typeid = models.ForeignKey(Account_Type, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Resident: {self.resident_id} | Admin: {self.admin_id} | BHW: {self.bhw_id} | Account Type: {self.account_typeid}"


class HealthService(models.Model):
    service_name = models.CharField(max_length =255)
    service_description = models.CharField(max_length =255)
    service_requirements = models.CharField(max_length =255)
    picture = models.ImageField(upload_to = 'images/', null=True)

    def __str__(self):
        return f"{self.service_name} {self.service_description} {self.service_requirements}  {self.picture}"
    
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

class Schedule(models.Model):
    bhwService= models.ForeignKey(HealthService, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    fname = models.CharField(max_length =255)
    lname = models.CharField(max_length =255)
    purok = models.IntegerField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    phonenum = models.CharField(max_length =255)
    date = models.DateField(max_length =255)
    time = models.CharField(max_length=100, null=True)   
 
    def __str__(self):
        return f"{self.fname} {self.lname} {self.phonenum}  {self.date}"
    
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
