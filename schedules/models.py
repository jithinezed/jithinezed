from django.db import models
from jobs.models import Job
from  accounts.models import Client,Employee
from vehicles.models import Vehicle
from drive.models import Files


class Schedule_comment(models.Model):
    comment = models.CharField(max_length=1000,null=True,blank=True)
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE,null=True,blank=True)

    created_date_time = models.DateTimeField(auto_now_add=True, blank=True)
    edited_date_time = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        ordering = ['-created_date_time', '-id']   

class Schedule(models.Model):
    tab_choice = (
    ("waste", "waste"),
    ("hills", "hills"),
    ("pumps", "pumps"),
    ("destruction", "destruction"))
    tab_type = models.CharField(max_length=50,choices=tab_choice,default="waste")
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=100, default='pending')
    team_employees = models.ManyToManyField(Employee, related_name='team_employees',blank=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, null=True, blank=True)
    gallery = models.ManyToManyField(Files,related_name='gallery', blank=True)
    image = models.FileField(upload_to='schedule/signature/images/', max_length=254,null=True, blank=True)
    created_date_time = models.DateTimeField(auto_now_add=True, blank=True)
    edited_date_time = models.DateTimeField(auto_now=True, blank=True)
    comments = models.ManyToManyField(Schedule_comment,related_name="commets", blank=True)
    end_date = models.DateField(null=True, blank=True)
    class Meta:
        ordering = ['-created_date_time', '-id']    
    
class AdditionalVehicles(models.Model):
    schedule = models.ForeignKey(Schedule,on_delete=models.CASCADE,blank=True,null=True)
    vehicles = models.ManyToManyField(Vehicle,related_name='additional_vehicle',blank=True)
    created_date_time = models.DateTimeField(auto_now_add=True, blank=True)
    edited_date_time = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        ordering = ['-created_date_time', '-id']   
