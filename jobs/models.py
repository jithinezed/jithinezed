from django.db import models
import uuid
from  accounts.models import Client,Employee
from sales_quotes.models import Quote
# from schedules.models import Schedule
from vehicles.models import Vehicle
from versatileimagefield.fields import VersatileImageField

class Job(models.Model):
    tab_choice = (
    ("waste", "waste"),
    ("hills", "hills"),
    ("pumps", "pumps"),
    ("destruction", "destruction"))

    tab_type = models.CharField(max_length=50,choices=tab_choice,default="waste")
    uuid = models.UUIDField(default = uuid.uuid4)    
    created_by = models.ForeignKey(Employee, on_delete =models.CASCADE)
    client = models.ForeignKey(Client,on_delete=models.CASCADE)
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, null=True, blank=True)
    amount =  models.CharField(max_length=50, null=True,blank=True)
    paid_amount = models.CharField(max_length=50, default="0")
    reoccurring = models.BooleanField(default=False)
    status = models.CharField(max_length =50,default="pending", null=True,blank=True)
    schedule_status = models.BooleanField(default=False)
    job_type = models.CharField(max_length=200, null=True,blank=True)
    ready_for_schedule =  models.BooleanField(default=None,null=True,blank=True)
    created_date_time = models.DateTimeField(auto_now_add=True, blank=True) 
    edited_date_time = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        ordering = ['-created_date_time', '-id']
class JobCard(models.Model):
    tab_choice = (
    ("waste", "waste"),
    ("hills", "hills"),
    ("pumps", "pumps"),
    ("destruction", "destruction"))
    tab_type = models.CharField(max_length=50,choices=tab_choice,default="waste")
    custom_client_email = models.CharField(max_length=200, null=True,blank=True)
    custom_job = models.ForeignKey(Job,on_delete=models.CASCADE,null=True,blank=True)
    custom_quote = models.ForeignKey(Quote,on_delete=models.CASCADE,null=True,blank=True)
    custom_location_logitude = models.CharField(max_length=200, null=True,blank=True)
    custom_location_latitude = models.CharField(max_length=200, null=True,blank=True)
    custom_place = models.CharField(max_length=200, null=True,blank=True)
    custom_quote_auto_create = models.CharField(max_length=200, null=True,blank=True)
    custom_building = models.CharField(max_length=200,null=True, blank=True)
    custom_device_capacity = models.CharField(max_length=200,null=True, blank=True)
    custom_device_waste = models.CharField(max_length=200,null=True, blank=True)
    custom_barcode = models.CharField(max_length=200,null=True, blank=True)  
    custom_site_address =models.CharField(max_length=250,null=True, blank=True)
    custom_site_suburb = models.CharField(max_length=250,null=True, blank=True)
    custom_post_code =models.CharField(max_length=200, null=True,blank=True)
    custom_bar_code_for_grease_trap_only = models.CharField(max_length=250,null=True, blank=True)          
    custom_pit_location = models.TextField(null=True, blank=True)
    custom_access_restriction =models.TextField(null=True, blank=True)  
    custom_company_suburb = models.CharField(max_length=250,null=True, blank=True) 
    custom_company_mobile_number =  models.CharField(max_length=250,null=True, blank=True)
    custom_company_contact_number = models.CharField(max_length=250,null=True, blank=True) 
    custom_company_email =  models.CharField(max_length=200, null=True,blank=True)
    custom_company_postcode = models.CharField(max_length=200, null=True,blank=True)
    custom_information = models.TextField(null=True, blank=True)
    custom_induction_type =models.CharField(max_length=200, null=True,blank=True)
    
    created_date_time = models.DateTimeField(auto_now_add=True, blank=True) 
    edited_date_time = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        ordering = ['-created_date_time', '-id'] 
class Services(models.Model):
    no =    models.CharField(max_length=250, null=True,blank=True) 
    waste_type = models.CharField(max_length=250, null=True,blank=True)
    capacity = models.CharField(max_length=250, null=True,blank=True)
    frequency = models.CharField(max_length=250, null=True,blank=True)
    pit_location = models.CharField(max_length=250, null=True,blank=True)

    created_date_time = models.DateTimeField(auto_now_add=True, blank=True) 
    edited_date_time = models.DateTimeField(auto_now=True, blank=True)
    # class Meta:
    #     ordering = ['-created_date_time', '-id']   
               

class JobcardInfo(models.Model):
    tab_choice = (
    ("waste", "waste"),
    ("hills", "hills"),
    ("pumps", "pumps"),("destruction", "destruction"))
    payment_details_choice = (
    ("cod", "cod"),
    ("account", "account"),("credit_card", "credit_card"))
    tab_type = models.CharField(max_length=50,choices=tab_choice,default="waste")
    quote = models.ForeignKey(Quote,on_delete=models.CASCADE,null=True,blank=True)
    client = models.ForeignKey(Client,on_delete=models.CASCADE,null=True)
    payment_details = models.CharField(max_length=15,choices=payment_details_choice,default="cod")
    company_name = models.CharField(max_length=250, null=True,blank=True)
    company_address =models.CharField(max_length=1000, null=True,blank=True)
    suburb = models.CharField(max_length=250, null=True,blank=True)
    postal_code = models.CharField(max_length=250, null=True,blank=True)
    job_site_address = models.CharField(max_length=250, null=True,blank=True)
    building_name = models.CharField(max_length=250, null=True,blank=True)
    contact_email_address = models.CharField(max_length=250, null=True,blank=True)
    contact_number=  models.CharField(max_length=250, null=True,blank=True)
    job_site_contact_name =  models.CharField(max_length=250, null=True,blank=True)
    services = models.ManyToManyField(Services,related_name="services",blank=True)
    access_restriction = models.CharField(max_length=250, null=True,blank=True)
    tc_required = models.BooleanField(default=False)
    waste_data_form =  models.BooleanField(default=False)
    access_height = models.CharField(max_length=250, null=True,blank=True)
    key_required = models.BooleanField(default=False)
    security_required = models.BooleanField(default=False)
    induction_required = models.BooleanField(default=False)
    contact_name = models.CharField(max_length=250, null=True,blank=True)
    phone_number = models.CharField(max_length=250, null=True,blank=True)
    type_of_induction = models.CharField(max_length=250, null=True,blank=True)
    pit_distacnce_from_truck_location = models.CharField(max_length=50, null=True,blank=True)
    water_tap_location = models.CharField(max_length=250, null=True,blank=True)
    gumy_required =  models.BooleanField(default=False)
    confined_space =  models.BooleanField(default=False)
    number_of_trucks_required =  models.CharField(max_length=250, null=True,blank=True)
    specific_ppe_reqired = models.BooleanField(default=False)
    service_time =  models.CharField(max_length=250, null=True,blank=True)
    if_yes_specify =  models.CharField(max_length=650, null=True,blank=True)
    completed_by =  models.CharField(max_length=250, null=True,blank=True)
    date = models.DateTimeField(null=True,blank=True)

    
    created_date_time = models.DateTimeField(auto_now_add=True, blank=True) 
    edited_date_time = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        ordering = ['quote']   