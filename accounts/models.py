from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import BooleanField
from django.utils import timezone
from django.utils.translation import activate
from versatileimagefield.fields import VersatileImageField

permissions_choices = (
     ("accounts-manager", "accounts-manager"), 
    ("accounts-staff", "accounts-staff"),   
    ("admin", "admin"),
    ("director", "director"),
    ("driver-factory-hand", "driver-factory-hand"),
    ("driver-liquid-waste-technician", "driver-liquid-waste-technician"),
    ("manager","manager"),
    ("operations-assistance-manager", "operations-assistance-manager"),
    ("operations-manager", "operations-manager"),   
    ("pump-coordinator","pump-coordinator"),
    ("pump-manager", "pump-manager"), 
    ("pump-technician","pump-technician"),
    ("sales-staff", "sales-staff"),
    ("scheduler", "scheduler"),
    ("superadmin","superadmin"),
    ("whs-manager", "whs-manager"), 
    )

class EmployeeCertification(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField()
    certification_number = models.IntegerField(20)
    certification_type = models.CharField(max_length=200)    

class Employee(models.Model):
    employee_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=200)
    user_choice = (
    ("accounts-manager", "accounts-manager"), 
    ("accounts-staff", "accounts-staff"),   
    ("admin", "admin"),
    ("director", "director"),
    ("driver-factory-hand", "driver-factory-hand"),
    ("driver-liquid-waste-technician", "driver-liquid-waste-technician"),
    ("manager","manager"),
    ("operations-assistance-manager", "operations-assistance-manager"),
    ("operations-manager", "operations-manager"),   
    ("pump-coordinator","pump-coordinator"),
    ("pump-manager", "pump-manager"), 
    ("pump-technician","pump-technician"),
    ("sales-staff", "sales-staff"),
    ("scheduler", "scheduler"),
    ("superadmin","superadmin"),
    ("whs-manager", "whs-manager"), 
    )

    user_type = models.CharField(max_length=50,
                  choices=user_choice,
                  default="scheduler")
    permission_type =models.CharField(max_length=100,choices=permissions_choices,default="scheduler",null=True,blank=True)

    contact_number = models.CharField(max_length=20)
    date_of_birth = models.DateField(null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    active_status = models.BooleanField(default=True)
    date_joined = models.DateField()
    dp =VersatileImageField(upload_to='uploads/employee/dp/' ,default= 'default/user/dp.jpg',null=True, blank=True) 
    bio = models.CharField(max_length=1000,blank=True)
    instagram_link = models.CharField(max_length=1000,blank=True,null=True)
    facebook_link = models.CharField(max_length=1000,blank=True,null=True)
    linkedin_link = models.CharField(max_length=1000,blank=True,null=True)
    cover_image = VersatileImageField(upload_to='uploads/employee/cover/', default= 'default/cover.jpg', null=True, blank=True)  
    email = models.EmailField(max_length=254,null=True,blank=True)

    personal_email = models.EmailField(max_length=254,null=True,blank=True)
    emergency_contact_name = models.CharField(max_length=200,null=True,blank=True)
    emergency_contact = models.CharField(max_length=50,null=True,blank=True)
    termination_date = models.DateField(null=True,blank=True)
    employement_status_choice = (
    ("full_time", "full_time"),
    ("casual","casual"),
    ("part_time","part_time"))
    employement_status = models.CharField(max_length=100,
                  choices=employement_status_choice,
                  default="full_time")
    
    address = models.TextField(null=True, blank=True)
    created_date_time = models.DateTimeField(auto_now_add=True, blank=True)
    edited_date_time = models.DateTimeField(auto_now=True, blank=True)
    class Meta:
        ordering = ['name']





class Client(models.Model):
    tab_choice = (
    ("waste", "waste"),
    ("hills", "hills"),
    ("pumps", "pumps"),
    ("destruction", "destruction"))

    tab_type = models.CharField(max_length=50,choices=tab_choice,default="waste")
    client_id = models.CharField(max_length=200,null=True,blank=True)
    client_choice = (
    ("Temporary", "Temporary"),
    ("Permenant", "Permenant"))
    client_type = models.CharField(max_length=9,
                  choices=client_choice,
                  default="Permenant")
    client_name = models.CharField(max_length=200)
    client_email = models.EmailField(max_length=254)
    date_joined = models.DateField(null=True, blank=True)
    location_logitude = models.CharField(max_length=200, null=True, blank=True)
    location_latitude = models.CharField(max_length=200, null=True, blank=True)
    place = models.CharField(max_length=200, null=True, blank=True)
    active_status = models.BooleanField(default=True)
    building = models.CharField(max_length=200,null=True, blank=True)
    dp = VersatileImageField(upload_to='uploads/client/dp/', default= 'default/user/dp.jpg', null=True, blank=True)
    
    device_waste = models.CharField(max_length=200,null=True, blank=True)
        
    site_address =models.CharField(max_length=250,null=True, blank=True)
    site_suburb = models.CharField(max_length=250,null=True, blank=True)
    site_post_code =models.CharField(max_length=250,null=True, blank=True)
    site_phone_no = models.CharField(max_length=250,null=True,blank=True)
    site_contact_person = models.CharField(max_length=250,null=True,blank=True)
    site_contact_mob = models.CharField(max_length=250,null=True,blank=True)
    induction_type =models.CharField(max_length=250,null=True, blank=True)
    
    bar_code_for_grease_trap_only = models.CharField(max_length=250,null=True, blank=True)    
    call_choice = (
    ("Received", "Received"),
    ("Rejected", "Rejected"))

    call_type = models.CharField(max_length=100,
                  choices=call_choice,
                  default="Received")
    account_status_choice = (
    ("Active", "Active"),
    ("Credit stop", "Credit stop"),
    ("Pending", "Pending"))
    account_type = models.CharField(max_length=100,
                  choices=account_status_choice,
                  default="Pending")
    pit_location = models.TextField(null=True, blank=True)
    access_restriction =models.TextField(null=True, blank=True)  

    company_name = models.CharField(max_length=250,null=True, blank=True) 
    company_contact_name = models.CharField(max_length=250,null=True, blank=True) 
    company_name = models.CharField(max_length=250,null=True, blank=True) 
    company_address =models.TextField(null=True, blank=True)
    company_suburb = models.CharField(max_length=250,null=True, blank=True) 
    company_contact_number = models.CharField(max_length=250,null=True, blank=True) 
    company_mobile_number =  models.CharField(max_length=250,null=True, blank=True)
    company_landline_number = models.CharField(max_length=250,null=True, blank=True)
    company_email =  models.EmailField(max_length=254,null=True, blank=True)        
    company_postcode = models.CharField(max_length=250,null=True, blank=True)
    sales_person = models.CharField(max_length=250,null=True, blank=True)
    information = models.TextField(null=True, blank=True)

    #invoice 
    invoice_name = models.CharField(max_length=250,null=True, blank=True)
    invoice_address =models.TextField(null=True, blank=True)
    invoice_phone= models.CharField(max_length=250,null=True, blank=True)
    invoice_email =  models.EmailField(max_length=254,null=True, blank=True)  
    invoice_account_status = models.CharField(max_length=250,null=True, blank=True)
    invoice_terms_of_account = models.TextField(null=True, blank=True)
    invoice_reason_for_cancelling= models.TextField(null=True, blank=True)


    payment_type_str = models.CharField(max_length=550,null=True, blank=True)
    invoice_purchase_no =  models.CharField(max_length=250,null=True, blank=True)               


    #waste service
    waste_service_choice = (
    ("chep", "chep"),
    ("plain","plain"),
    ("loscam","loscam"))
    waste_service_type = models.CharField(max_length=100,
                  choices=waste_service_choice,
                  default="chep")
    device_capacity = models.CharField(max_length=200,null=True, blank=True)    
    frequency =    models.CharField(max_length=200,null=True, blank=True)   
    barcode = models.CharField(max_length=200,null=True, blank=True)      

    price= models.CharField(max_length=250,null=True, blank=True) 
    next_service = models.DateField(null=True, blank=True)   
    last_service = models.DateField(null=True, blank=True) 
    job_duration = models.CharField(max_length =100,null=True, blank=True)
    # key_required_type = models.BooleanField(default=False) 
    key_required_type_str= models.CharField(max_length=250,null=True, blank=True)
    job_status = models.CharField(max_length=250,null=True,blank=True)
    alarm_code = models.CharField(max_length=250,null=True,blank=True)
    weigh_bridge_required = models.CharField(max_length=250,null=True,blank=True)
    # pellets_to_be_exchanged = models.BooleanField(default=False) 
    pellets_to_be_exchanged_str = models.CharField(max_length=250,null=True, blank=True)

    quantity = models.CharField(max_length=250,null=True, blank=True) 

    next_service_1 = models.DateTimeField(null=True, blank=True)     
    next_service_2 = models.DateTimeField(null=True, blank=True)   
    frequency_weeks = models.CharField(max_length=250,null=True, blank=True)
    frequency_days = models.CharField(max_length=250,null=True, blank=True)   
    account_status = models.CharField(max_length=250,null=True, blank=True)  
    
    access_status_choice = (("1","1"),("2","2"))
    access_status  = models.CharField(max_length=10,choices=access_status_choice,default="1")
    next_service_due = models.DateTimeField(null=True, blank=True) 
    induction_required_str = models.CharField(max_length=250,null=True, blank=True)
    

    created_date_time = models.DateTimeField(auto_now_add=True, blank=True)
    edited_date_time = models.DateTimeField(auto_now=True, blank=True)

    Reason_for_cancelling = models.CharField(max_length=1000,null=True,blank=True)

    # waste_type = models.CharField(max_length=100,choices=waste_type_choice,null=True,blank=True)
    waste_type_str = models.CharField(max_length=1000,null=True,blank=True)

    class Meta:
        ordering = ['-created_date_time', '-id']    
class SiteDetails(models.Model):
    site_details = models.ForeignKey(Client,on_delete=models.CASCADE,null=True,blank=True)
    owner = models.CharField(max_length=1000,null=True,blank=True)
    pump_assetNo = models.CharField(max_length=1000,null=True,blank=True)
    location = models.CharField(max_length=1000,null=True,blank=True)
    frequency = models.CharField(max_length=1000,null=True,blank=True)
    last_service = models.DateTimeField(null=True,blank=True)
    next_service = models.DateTimeField(null=True,blank=True)
    service_description = models.CharField(max_length=1000,null=True,blank=True)
    edited_date_time = models.DateTimeField(auto_now=True, blank=True)
    created_date_time = models.DateTimeField(auto_now_add=True, blank=True)
    active_status = models.BooleanField(default=True)
    class Meta:
        ordering = ['-created_date_time', '-id']                           

class StaticImages(models.Model):
    dp = VersatileImageField(upload_to='uploads/client/dp/', null=True, blank=True)
    facebook = models.ImageField(upload_to='mail/signature/',null=True, blank=True)
    twitter = models.ImageField(upload_to='mail/signature/',null=True, blank=True)
    youtube = models.ImageField(upload_to='mail/signature/',null=True, blank=True)
    
    likedin = models.ImageField(upload_to='mail/signature/',null=True, blank=True)
    instagram = models.ImageField(upload_to='mail/signature/',null=True, blank=True)
    pinterest = models.ImageField(upload_to='mail/signature/',null=True, blank=True)
    banner = models.ImageField(upload_to='mail/signature/',null=True, blank=True)
    logo = models.ImageField(upload_to='mail/signature/',null=True, blank=True)
    email_icon = models.ImageField(upload_to='mail/signature/',null=True, blank=True)
    address_icon = models.ImageField(upload_to='mail/signature/',null=True, blank=True)
    mobile_icon = models.ImageField(upload_to='mail/signature/',null=True, blank=True)
    phone_icon = models.ImageField(upload_to='mail/signature/',null=True, blank=True)
    website_icon = models.ImageField(upload_to='mail/signature/',null=True, blank=True)
    demo_pc1 = models.ImageField(upload_to='mail/signature/',null=True, blank=True)
    demo_pic2  = models.ImageField(upload_to='mail/signature/',null=True, blank=True)
    demo_pic3  = models.ImageField(upload_to='media/uploads/drive/file-archive/',null=True, blank=True)
    default  = models.ImageField(upload_to='default/user/',null=True, blank=True)
    vehicle_default = VersatileImageField(upload_to='default/',null=True, blank=True)
    email_bg = models.ImageField(upload_to='mail/signature/',null=True, blank=True)

    company_log_hills = models.ImageField(upload_to='enviro/company/',null=True, blank=True)
    company_log_pumps = models.ImageField(upload_to='enviro/company/',null=True, blank=True)
    company_log_waste = models.ImageField(upload_to='enviro/company/',null=True, blank=True)
    company_log_destruction = models.ImageField(upload_to='enviro/company/',null=True, blank=True)
    
    created_date_time = models.DateTimeField(auto_now_add=True, blank=True)
    edited_date_time = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        ordering = ['-created_date_time', '-id']
class NotificationKeys(models.Model):
    key = models.CharField(max_length=200,null=True, blank=True)

class PushNotification(models.Model):
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE,null=True,blank=True)
    keys = models.ManyToManyField(NotificationKeys,related_name='notification_keys', blank=True)
    created_date_time = models.DateTimeField(auto_now_add=True, blank=True)
    edited_date_time = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        ordering = ['-created_date_time', '-id']  