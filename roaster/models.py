from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
from accounts.models import Employee

class Roaster(models.Model):
    active_status = models.BooleanField(default=True)
    technician = models.ForeignKey(Employee,on_delete=models.CASCADE)
    day = models.DateField(null=True,blank=True)
    scheduled_time = models.CharField(max_length = 200,null=True,blank=True)
    type_of_service = models.CharField(max_length = 200, null=True,blank=True)
    company_name = models.CharField(max_length = 200)
    contact_name = models.CharField(max_length = 200, null=True,blank=True)
    site_adddress = models.CharField(max_length = 1000)
    comments_info = models.CharField(max_length = 200)
    end_time = models.DateField()
    slot = models.IntegerField()
    amount = models.IntegerField(null=True,blank=True)
    job_status = models.CharField(max_length = 200,default='not started')