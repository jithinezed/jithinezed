from django.db import models
from accounts.models import Employee
from vehicles.models import Vehicle
from datetime import datetime
from accounts.models import Client
# Create your models here.

class DriveFolder(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    created_date =models.DateField(default=datetime.now,null=True,blank=True)
    edited_date =models.DateField(default=datetime.now,null=True,blank=True)
    parent_folder = models.IntegerField()
    tab_choice = (
    ("waste", "waste"),
    ("hills", "hills"),
    ("pumps", "pumps"),
    ("destruction", "destruction"))
    tab_type = models.CharField(max_length=50,
    choices=tab_choice,
    default="waste")
    site = models.ForeignKey(Client,on_delete=models.CASCADE,null=True,blank=True)
    sales_tab = models.BooleanField(default=False)
    generate_quote = models.BooleanField(default=False)
    attach_quote = models.BooleanField(default=False)
    intranet =  models.BooleanField(default=False)
    marketing = models.BooleanField(default=False)
    description_of_waste = models.BooleanField(default=False)
    power_point = models.BooleanField(default=False)
    pricing = models.BooleanField(default=False)
    tender = models.BooleanField(default=False)
    Intranet_top_bar_attachments = models.BooleanField(default=False)
    job_images = models.BooleanField(default=False)
    template = models.BooleanField(default=False)
    visibility = models.BooleanField(default=True,null=True,blank=True)
    accessibility = models.BooleanField(default=True,null=True,blank=True)
    accounts_files = models.BooleanField(default=False)
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE,null=True,blank=True)
    folder_type = (
    ("team-individual", "team-individual"),
    ("team-individual-private", "team-individual-private"),
    ("site-individual", "site-individual"),
    ("site-individual-private", "site-individual-private"),
    ("vehicle-individual-private", "vehicle-individual-private"),
    ("general", "general"))
    vehicle = models.BooleanField(default=False)
    vehicle_id= models.ForeignKey(Vehicle,on_delete = models.CASCADE,null=True,blank=True) 
    type = models.CharField(max_length=50,
    choices=folder_type,
    default="general")
    created_date_time = models.DateTimeField(auto_now_add=True, blank=True)
    edited_date_time = models.DateTimeField(auto_now=True, blank=True)
    vehicle_type = models.CharField(max_length=10,null=True,blank=True)

    class Meta:
        ordering = ['-created_date_time', '-id']
  
class Files(models.Model):
  file = models.FileField(upload_to='uploads/drive/file-archive/', max_length=254,null=True,blank=True)
  name = models.CharField(max_length=100,null=True,blank=True)    
  folder =models.ForeignKey(DriveFolder,on_delete=models.CASCADE)
  created_by = models.ForeignKey(Employee,on_delete=models.CASCADE,null=True,blank=True)
  created_site = models.ForeignKey(Client,on_delete=models.CASCADE,null=True,blank=True)
  template_pdf_file = models.FileField(upload_to='uploads/drive/file-archive/', max_length=254,null=True,blank=True)
  template_html =  models.TextField(null=True, blank=True)
  created_date_time = models.DateTimeField(auto_now_add=True, blank=True)
  edited_date_time = models.DateTimeField(auto_now=True, blank=True)
  expiry_date = models.DateField(null=True,blank=True)
  alert_before = models.DateField(null=True,blank=True)
  visibility = models.BooleanField(default=True,null=True,blank=True)
  accessibility = models.BooleanField(default=True,null=True,blank=True)
  class Meta:
        ordering = ['-created_date_time', '-id']


   
