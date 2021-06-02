from rest_framework import serializers
import datetime
import os
from .models import DriveFolder,Files

class DriveFolderSerializer(serializers.ModelSerializer):
    class Meta:
        model =  DriveFolder
        fields = ['id','name','parent_folder','tab_type','intranet','generate_quote','job_images','Intranet_top_bar_attachments','tender','pricing','power_point','description_of_waste','marketing','type','employee','vehicle','accounts_files','vehicle_id','site','vehicle_type']   
        

class DriveFolderGetSerializer(serializers.ModelSerializer):
    class Meta:
        model =  DriveFolder
        fields = ['id','name','parent_folder']
        order_by = (
        ('name',)
        )
        
class FilesGetSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Files
        fields = '__all__'        
        