from rest_framework import serializers
import os
from .models import (Vehicle,Fleet,TruckMaintananceReport,CarMaintananceReport,
FuelExpense,ForkliftMaintananceReport,PreInspectionCheck,VehicleFile,VehicleFolder,VehicleImages)

class VehicleSerializer(serializers.ModelSerializer):
     class Meta:
        model = Vehicle
        fields = ['id','vehicle_type','previous_rego','registration',
        'types','year','transmission','height','width','length',
        'litres','vin_number','axies','due_rego','engine_numbers',
         'image1','image2','image3','fbt','e_tag','fuel_card','insurance','fuel']
class VehicleGetSerializer(serializers.ModelSerializer):
     image_thumbnail = serializers.SerializerMethodField()
     image1 = serializers.SerializerMethodField()
     multiple_images = serializers.SerializerMethodField()
     def get_image_thumbnail(self, instance):
          try:
               return instance.image1.thumbnail['200x200'].url
       
          except:
                pass
     def get_multiple_images(self, instance):
          attachments_list = []
          try:
               images =  instance.images.get_queryset()
               if not images:
                    return attachments_list
               try:
                    for i in images:
                         attachments_list.append({
                         'id': i.id,
                         'file': i.image_file.url,
                         'name': os.path.basename(i.image_file.url),
                         })
                    return   attachments_list   
               
               except:
                    pass 
          
          except:
               return  attachments_list
     def get_image1(self, instance):
          try:
               images =  instance.images.get_queryset()
               try:
                    data =images[0]

                    return data.image_file.url 
               except:
                    return instance.image1.url
                    pass 
          except:
              return None
     
     class Meta:
        model = Vehicle
        exclude = ['images']
        extra_fields = ['multiple_images','image1']
class FleetSerializer(serializers.ModelSerializer):
     class Meta:
        model = Fleet
        fields = ['id','make',
        'rego_due','contact','location','rms_booking_by','booked_date','completed','next_due']      

class FleetGetSerializer(serializers.ModelSerializer):
     registration = serializers.ReadOnlyField(source='vehicle.registration')
     class Meta:
        model = Fleet
        fields = '__all__'

class TruckMaintananceReportSerializer(serializers.ModelSerializer):

     class Meta:
        
         model = TruckMaintananceReport
         fields = ['id','vehicle','description','invoice_date','service_date','ometer','invoice_number','service_provided','hours','l_cost','s_part','gst','total_cost']
                  
class TruckMaintananceReportGetSerializer(serializers.ModelSerializer):
     vehicle = serializers.ReadOnlyField(source='vehicle.id')
     registration = serializers.ReadOnlyField(source='vehicle.registration')
     class Meta:
        model =TruckMaintananceReport
        fields = '__all__'

        
class ForkliftMaintananceReportSerializer(serializers.ModelSerializer):
     registration = serializers.ReadOnlyField(source='vehicle.registration')
     class Meta:
         model = ForkliftMaintananceReport
         exclude = ['active_status']
class ForkliftMaintananceReportGetSerializer(serializers.ModelSerializer):
     vehicle = serializers.ReadOnlyField(source='vehicle.id')
     registration = serializers.ReadOnlyField(source='vehicle.registration')
     class Meta:
        model = ForkliftMaintananceReport
        fields = '__all__'

class FuelExpenseSerializer(serializers.ModelSerializer):
     class Meta:
        model = FuelExpense
        fields = ['id','vehicle','date','time',
        'truck_rego','current_reading_before','reading_after_filling','filled_by','volume_usedIn_liter','tab_type','vehicle_type']             
class FuelExpenseGetSerializer(serializers.ModelSerializer):
     registration = serializers.ReadOnlyField(source='vehicle.registration')
     class Meta:
        model = FuelExpense
        fields = '__all__'
class VehicleIdGetSerializer(serializers.ModelSerializer):
     class Meta:
        model = Vehicle
        fields = 'id','registration'


class PreInspectionCheckSerializer(serializers.ModelSerializer):
     class Meta:
          model = PreInspectionCheck
          fields = ['id','vehicle','odometer','driver_name','odometdriver_signature','hour_meter_start','fit_for_work',
          'Valid_driving_license','appropriate_ppe','engine_oil_level','warning_system','steering','safety_emerg_stop',
          'handbreak_alarm','pto_vacpump','horn','rev_alarm_camera','lights_head','lights_tail','light_beacons',
          'hazard_light','rims_wheelnut','coolant','wheels','mirror_windowscreen','structure_bodywork','wipers',
          'fuel_levelpump','fuel_leveltruck','seat_seatbelt','parkbrake_trailer','foot_brake','electrical',
          'pin_retainers','hoses','fittings','first_aid_kit','ppe','fire_extinguisher_date','garden_hose',
          'gatic_lifters','bucket_rags','spill_kit','action_taken','authorized_by','safe_ready_to_operate',
          'reported_faults','reviewed_form','corrected','scheduled_for_repair','no_action',
          'do_not_affect_safe_operation','name','signature','tab_type','vehicle_type','date_now','fire_extinguisher','house_keeping']                   


class PreInspectionCheckGetSerializer(serializers.ModelSerializer):
     registration = serializers.ReadOnlyField(source='vehicle.registration')
     class Meta:
          model = PreInspectionCheck
          fields = '__all__'



class VehicleFileSerializer(serializers.ModelSerializer):
     class Meta:
          model = VehicleFile
          fields = ['id','file_item','vehicle','expiring_date','notification_alert_before','vehicle_folder']     
          
class VehicleFileGetSerializer(serializers.ModelSerializer):
     class Meta:
          model = VehicleFile
          fields = '__all__'  
          
class VehicleFolderSerializer(serializers.ModelSerializer):
     class Meta:
          model = VehicleFolder
          fields = ['id','name']  

class VehicleFolderGetSerializer(serializers.ModelSerializer):
     class Meta:
          model = VehicleFolder
          fields = '__all__'          

class VehicleImagesSerializer(serializers.ModelSerializer):
     class Meta:
        model = VehicleImages
        exclude = ['attachments']
class VehicleImagesGetSerializer(serializers.ModelSerializer):
   attachments_list = serializers.SerializerMethodField()

   def get_attachments_list(self, instance):
        attachments_list =[]
        each_attachments = instance.attachments.get_queryset()
        for i in each_attachments:
          try:
                attachments_list.append({
                        'id': i.id,
                        'file': i.file.url,
                    #     'type': (i.file.url).split('.')[-1],
                        'name': os.path.basename(i.file.url)
                    })
            
          except:
                pass
          

          return attachments_list
   class Meta:
      model= VehicleImages
      exclude = ['attachments','vehicle','folder']
      extra_fields = ['attachments_list','id']  

class CarMaintananceReportSerializer(serializers.ModelSerializer):
     registration = serializers.ReadOnlyField(source='vehicle.registration')
     class Meta:
         model = CarMaintananceReport
         exclude = ['active_status']