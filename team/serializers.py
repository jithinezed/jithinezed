from rest_framework import serializers
from drive.models import DriveFolder,Files
from accounts.models import Employee,EmployeeCertification
from .models import EmployeeFile,EmployeeFolder,EmployeeImages,PostImage,SafteyInfo
import os
from team.models import EmployeeFile

class EmployeeSerializer(serializers.ModelSerializer):
     class Meta:
        model = Employee
        fields = ['id', 'employee_id', 'name', 'contact_number',
            'date_of_birth','dp', 'bio', 'cover_image','date_joined','user_type','facebook_link','instagram_link','linkedin_link','termination_date',
            'emergency_contact','emergency_contact_name','personal_email','employement_status','email','address']

class EmployeeGetSerializer(serializers.ModelSerializer):
   termination_date =serializers.SerializerMethodField()
   username = serializers.ReadOnlyField(source='user.username')
   dp_thumbnail = serializers.SerializerMethodField()
   cover_image = serializers.SerializerMethodField()
   expiry_date = serializers.SerializerMethodField() 
   alert_before = serializers.SerializerMethodField()
   driving_license = serializers.SerializerMethodField()
   def get_cover_image(self, instance):
      try:  
         return instance.cover_image.thumbnail['200x200'].url
      except:
            pass  
   def get_dp_thumbnail(self, instance):
      try:   
         return instance.dp.thumbnail['200x200'].url
      except:
            pass
   def get_expiry_date(self, instance):
      try:   
         
         license_file = DriveFolder.objects.get(name="Drivers License")
         try:
            driving_licence_file = Files.objects.get(created_by=instance,folder=license_file)
         except:
            return "No license file exists under this employe"   
         
         date = driving_licence_file.expiry_date
         return str(date)
      except:
            pass      
   def get_driving_license(self, instance):
      try:
         dr_license = EmployeeImages.objects.get(employee=instance,folder=1)  
         # driving_license =[]
         each_attachments = dr_license.attachments.get_queryset()
         for i in each_attachments:
            try:
               driving_license= i.file.url
            except:
                pass        
     
         return str(driving_license)
      except:
            pass 
   def get_termination_date(self, instance):
      try:   
         return instance.termination_date
      except:
            pass                 
   def get_alert_before(self, instance):
      try:   
         
         license_file = DriveFolder.objects.get(name="Drivers License")
         try:
            driving_licence_file = Files.objects.get(created_by=instance,folder=license_file)
         except:
            return "No file exists"   
         
         date = driving_licence_file.alert_before
         return str(date)
      except:
            pass             
      
   class Meta:
      model = Employee
      extra_fields =['username']
      exclude =['created_date_time']

class EmployeeCertificationSerializer(serializers.ModelSerializer):
   
   class Meta:
      model = EmployeeCertification
      fields = '__all__'


class EmployeeFileGetSerializer(serializers.ModelSerializer):
     name = serializers.ReadOnlyField(source='employee.name')
     designation = serializers.ReadOnlyField(source='employee.user_type')
     dp = serializers.ImageField(source='employee.dp')
     
     class Meta:
        model = EmployeeFile
        fields = '__all__'        


class EmployeeFileSerializer(serializers.ModelSerializer):
     class Meta:
        model = EmployeeFile
        fields =['id','employee','employee_folder','file_item','expiry_date','alert_before'] 


class EmployeeFolderSerializer(serializers.ModelSerializer):
   class Meta:
      model = EmployeeFolder
      fields = ['id','name']   

class EmployeeFolderGetSerializer(serializers.ModelSerializer):
   class Meta:
      model = EmployeeFolder
      fields = '__all__'                      



class EmployeeImagesSerializer(serializers.ModelSerializer):
     class Meta:
        model = EmployeeImages
        exclude = ['attachments']
class EmployeeImagesGetSerializer(serializers.ModelSerializer):
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
                        'name': os.path.basename(i.file.url),
                    })
            
            except:
                pass
   
         return attachments_list
   class Meta:
      model= EmployeeImages
      exclude = ['attachments','employee','folder']
      extra_fields = ['attachments_list','id']   


class SafteyInfoSerializer(serializers.ModelSerializer):
   data = serializers.JSONField()

   class Meta:
      model = SafteyInfo
      fields = ['id', 'name', 'data'] 
class SafteyInfoGetSerializer(serializers.ModelSerializer):
     class Meta:
         model = SafteyInfo
         fields = '__all__'           
