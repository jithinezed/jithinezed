from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime,date
from accounts.models import Employee
import datetime as dd
from versatileimagefield.fields import VersatileImageField

tab_choice = (
    ("waste", "waste"),
    ("hills", "hills"),
    ("pumps", "pumps"),
    ("destruction", "destruction"),
    ("all","all"))

    
class VehicleImage(models.Model):
    image_file = VersatileImageField(upload_to='uploads/vehicle/' ,default= '/default/vehi.jpg', blank=True)
    created_date_time = models.DateTimeField(auto_now_add=True, blank=True)
    edited_date_time = models.DateTimeField(auto_now=True, blank=True)
    visibility = models.BooleanField(default=True,null=True,blank=True)

    class Meta:
        ordering = ['-created_date_time', '-id']    
   

class Vehicle(models.Model):
    vehicle_type = models.CharField(max_length = 200,null=True,default="truck",blank=True)
    active_status = models.BooleanField(default=True)
    previous_rego=models.DateField(null=True, blank=True)
    registration = models.CharField(max_length = 100,unique=True)
    types = models.CharField(max_length = 200,null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    transmission = models.CharField(max_length = 200,null=True, blank=True)
    fuel = models.CharField(max_length = 150,null=True, blank=True)
    height = models.CharField(max_length = 150,null=True, blank=True)
    width = models.CharField(max_length = 150,null=True, blank=True)
    length = models.CharField(max_length = 150,null=True, blank=True)
    litres = models.CharField(max_length = 150,null=True, blank=True)
    vin_number=models.CharField(max_length = 250,null=True, blank=True)
    axies = models.CharField(max_length = 150,null=True, blank=True)
    due_rego= models.DateField(null=True, blank=True)
    engine_numbers = models.CharField(max_length = 150,null=True, blank=True)
    e_tag = models.CharField(max_length = 150,null=True, blank=True)
    insurance = models.CharField(max_length = 150,null=True, blank=True)
    fuel_card = models.CharField(max_length = 200,null=True, blank=True)
    fbt = models.CharField(max_length = 200,null=True, blank=True)
    action =models.BooleanField(default=False)
    image1 = VersatileImageField(upload_to='uploads/vehicle/' ,default= '/default/vehi.jpg', blank=True)
    images = models.ManyToManyField(VehicleImage,blank=True,related_name='images')


    image2 = models.ImageField(upload_to='media/uploads/vehicle/' ,default= '/default/vehi.jpg', blank=True)
    image3 = models.ImageField(upload_to='media/uploads/vehicle/' ,default= '/default/vehi.jpg', blank=True)

    created_date_time = models.DateTimeField(auto_now_add=True, blank=True)
    edited_date_time = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        ordering = ['-created_date_time', '-id']   


class Fleet(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    make = models.CharField(max_length = 100,null=True, blank=True)
    rego_due = models.DateField(null=True, blank=True)
    location = models.CharField(max_length = 100,null=True, blank=True)
    contact = models.CharField(max_length = 100,null=True, blank=True)
    rms_booking_by = models.DateField(null=True, blank=True)
    booked_date = models.DateField(null=True, blank=True)
    completed = models.CharField(max_length = 100,null=True, blank=True)
    next_due = models.DateField(null=True, blank=True)
    active_status = models.BooleanField(default=True)

class TruckMaintananceReport(models.Model):
    vehicle_type = models.CharField(max_length = 200,null=True,default="truck",blank=True)

    tab_type = models.CharField(max_length=50,choices=tab_choice,default="waste")
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    active_status = models.BooleanField(default=True)
    description = models.CharField(max_length = 100,null=True, blank=True)
    invoice_date = models.DateField(null=True, blank=True)
    service_date = models.DateField(null=True, blank=True)
    ometer = models.CharField(max_length = 100,null=True, blank=True)
    invoice_number = models.IntegerField(null=True, blank=True)
    service_provided = models.CharField(max_length = 100,null=True, blank=True)
    hours = models.CharField(max_length = 100,null=True, blank=True)
    l_cost = models.CharField(max_length = 100,null=True, blank=True)
    s_part = models.CharField(max_length = 100,null=True, blank=True)
    gst = models.CharField(max_length = 100,null=True, blank=True)
    total_cost = models.CharField(max_length = 100,null=True, blank=True)

    created_date_time = models.DateTimeField(auto_now_add=True, blank=True)
    edited_date_time = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        ordering = ['-created_date_time', '-id']   
class CarMaintananceReport(models.Model):
    vehicle_type = models.CharField(max_length = 200,null=True,default="car",blank=True)

    tab_type = models.CharField(max_length=50,choices=tab_choice,default="waste")
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    active_status = models.BooleanField(default=True)
    description = models.CharField(max_length = 100,null=True, blank=True)
    invoice_date = models.DateField(null=True, blank=True)
    service_date = models.DateField(null=True, blank=True)
    ometer = models.CharField(max_length = 100,null=True, blank=True)
    invoice_number = models.IntegerField(null=True, blank=True)
    service_provided = models.CharField(max_length = 100,null=True, blank=True)
    hours = models.CharField(max_length = 100,null=True, blank=True)
    l_cost = models.CharField(max_length = 100,null=True, blank=True)
    s_part = models.CharField(max_length = 100,null=True, blank=True)
    gst = models.CharField(max_length = 100,null=True, blank=True)
    total_cost = models.CharField(max_length = 100,null=True, blank=True)

    created_date_time = models.DateTimeField(auto_now_add=True, blank=True)
    edited_date_time = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        ordering = ['-created_date_time', '-id']           


class ForkliftMaintananceReport(models.Model):
    vehicle_type = models.CharField(max_length = 200,null=True,default="fork-lift",blank=True)
    tab_type = models.CharField(max_length=50,choices=tab_choice,default="waste")
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    active_status = models.BooleanField(default=True)
    description = models.CharField(max_length = 100,null=True, blank=True)
    service_completed= models.DateField(null=True, blank=True)
    hour_mr = models.CharField(max_length = 100,null=True, blank=True)
    next_service = models.DateField(null=True, blank=True)
    frequency = models.CharField(max_length = 100,null=True, blank=True)
    rego_expiry_date = models.DateField(null=True, blank=True)
    active_perfomed_report = models.CharField(max_length = 100,null=True, blank=True)
    invoice_number = models.CharField(max_length = 100,null=True, blank=True)

    total_cost = models.CharField(max_length = 100,null=True, blank=True)  

    created_date_time = models.DateTimeField(auto_now_add=True, blank=True)
    edited_date_time = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        ordering = ['-created_date_time', '-id']      


class FuelExpense(models.Model):
    vehicle_type = models.CharField(max_length = 200,null=True, blank=True,default='truck')
    tab_type = models.CharField(max_length=50,choices=tab_choice,default="waste")
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    active_status = models.BooleanField(default=True)
    date = models.DateField(null=True, blank=True)
    time = models.CharField(max_length = 100,null=True, blank=True)
    truck_rego = models.CharField(max_length = 200,null=True, blank=True)
    current_reading_before = models.CharField(max_length = 100,null=True, blank=True)
    reading_after_filling = models.CharField(max_length = 100,null=True, blank=True)
    filled_by = models.CharField(max_length = 200,null=True, blank=True)
    volume_usedIn_liter = models.CharField(max_length = 100,null=True, blank=True)

    created_date_time = models.DateTimeField(auto_now_add=True, blank=True)
    edited_date_time = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        ordering = ['-created_date_time', '-id']       
    

class PreInspectionCheck(models.Model):
    vehicle_type = models.CharField(max_length = 200,null=True,default="truck",blank=True)
    tab_type = models.CharField(max_length=50,
    choices=tab_choice,
    default="waste")
    active_status = models.BooleanField(default=True)
    date_time = models.DateTimeField(auto_now_add=True, blank=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    odometer = models.IntegerField(null=True, blank=True)
    driver_name = models.ForeignKey(Employee, on_delete=models.CASCADE)
    odometdriver_signature = models.CharField(max_length = 100,null=True, blank=True)
    hour_meter_start =  models.CharField(max_length = 100,null=True, blank=True)
    fit_for_work = models.BooleanField(default = False)
    Valid_driving_license = models.BooleanField(default = False)
    appropriate_ppe = models.BooleanField(default = False)
    engine_oil_level = models.BooleanField(default = False)
    warning_system = models.BooleanField(default = False)
    steering = models.BooleanField(default = False)   
    safety_emerg_stop = models.BooleanField(default = False)
    handbreak_alarm = models.BooleanField(default = False)
    pto_vacpump = models.BooleanField(default = False)
    horn = models.BooleanField(default = False)
    rev_alarm_camera = models.BooleanField(default = False)
    lights_head = models.BooleanField(default = False)
    lights_tail = models.BooleanField(default = False)
    light_beacons = models.BooleanField(default = False)
    hazard_light = models.BooleanField(default = False)
    rims_wheelnut = models.BooleanField(default = False)
    coolant = models.BooleanField(default = False)
    wheels = models.BooleanField(default = False)
    mirror_windowscreen = models.BooleanField(default = False)
    structure_bodywork = models.BooleanField(default = False)
    wipers = models.BooleanField(default = False)
    fuel_levelpump = models.BooleanField(default = False)
    fuel_leveltruck = models.BooleanField(default = False)
    seat_seatbelt = models.BooleanField(default = False)
    parkbrake_trailer = models.BooleanField(default = False)
    foot_brake = models.BooleanField(default = False)
    electrical = models.BooleanField(default = False)
    pin_retainers = models.BooleanField(default = False)
    hoses = models.BooleanField(default = False)
    fittings = models.BooleanField(default = False)
    first_aid_kit = models.BooleanField(default = False)
    ppe = models.BooleanField(default = False)
    fire_extinguisher_date =models.DateField(null= True,blank=True)
    fire_extinguisher =  models.BooleanField(default = False)
    house_keeping =  models.BooleanField(default = False)
    garden_hose = models.BooleanField(default = False)
    gatic_lifters = models.BooleanField(default = False)
    bucket_rags = models.BooleanField(default = False)
    spill_kit = models.BooleanField(default = False)
    action_taken = models.CharField(max_length = 100,null=True, blank=True)
    authorized_by = models.CharField(max_length = 100,null=True, blank=True)
    safe_ready_to_operate = models.BooleanField(default = False)
    reported_faults = models.BooleanField(default = False)
    reviewed_form = models.BooleanField(default = False)
    corrected  = models.BooleanField(default = False)
    scheduled_for_repair = models.BooleanField(default = False)
    no_action = models.BooleanField(default = False)
    do_not_affect_safe_operation = models.BooleanField(default = False)
    name = models.CharField(max_length = 100,null=True, blank=True)
    signature = models.CharField(max_length = 100,null=True, blank=True)
    date_now= models.DateField(null=True,blank=True)

    created_date_time = models.DateTimeField(auto_now_add=True, blank=True)
    edited_date_time = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        ordering = ['-created_date_time', '-id']   

class VehicleFolder(models.Model):
    name = models.CharField(max_length=300)
    visibility = models.BooleanField(default=True,null=True,blank=True)
    accessibility = models.BooleanField(default=True,null=True,blank=True)
    created_by =models.ForeignKey(Employee,on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self): 
         return self.name
    created_date_time = models.DateTimeField(auto_now_add=True, blank=True)
    edited_date_time = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        ordering = ['-created_date_time', '-id']       
         

class VehicleFile(models.Model):
        active_status = models.BooleanField(default=True)
        vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
        vehicle_folder = models.ForeignKey(VehicleFolder, on_delete=models.CASCADE)
        file_item = models.FileField(upload_to='uploads/vehicle/',null=True, blank=True) 
        notification_alert_before = models.DateField(null=True,blank=True)
        expiring_date = models.DateField(null=True,blank=True)



class PostImage(models.Model):
   file = models.FileField(upload_to='uploads/vehicle/images/', max_length=254)

class VehicleImages(models.Model):
        attachments = models.ManyToManyField(PostImage, related_name="post_image", blank=True)
        vehicle = models.ForeignKey(Vehicle,on_delete=models.CASCADE)
        folder = models.ForeignKey(VehicleFolder,on_delete=models.CASCADE)    


    

    




