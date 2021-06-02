
from django.db.models import fields
from rest_framework import serializers
from accounts.models import Client,SiteDetails
from .models import PostImage,ClientImages,ClientFolder
import os

class ClientSerializer(serializers.ModelSerializer):
    
     class Meta:
        model = Client
        fields =['tab_type','client_id','client_type','client_name','client_email','date_joined','location_logitude','location_latitude','place',
        'building','dp','device_waste','site_address','site_suburb','site_post_code','site_phone_no','site_contact_person','site_contact_mob','induction_type',
        'bar_code_for_grease_trap_only','call_type','account_type','pit_location','access_restriction','company_name','company_address','company_suburb',
        'company_contact_number','company_mobile_number','company_landline_number','company_email','company_postcode','sales_person','information',
        'invoice_name','invoice_address','invoice_phone','invoice_email','invoice_account_status','invoice_terms_of_account','invoice_reason_for_cancelling',
        'payment_type_str','invoice_purchase_no','waste_service_type','device_capacity','frequency','barcode','price','next_service','last_service',
        'job_duration','key_required_type_str','job_status','alarm_code','weigh_bridge_required','pellets_to_be_exchanged_str','quantity','next_service_1',
        'next_service_2','frequency_weeks','frequency_days','account_status','access_status_choice','access_status','next_service_due',
        'Reason_for_cancelling','waste_type_str','induction_required_str','company_contact_name']

class ClientGetSerializer(serializers.ModelSerializer):
     dp_thumbnail = serializers.SerializerMethodField()
     def get_dp_thumbnail(self, instance):
          try:
               return instance.dp.thumbnail['200x200'].url
          except:
                pass
     class Meta:
        model = Client
        fields = '__all__'
class ClientImagesSerializer(serializers.ModelSerializer):
     class Meta:
        model = ClientImages
        exclude = ['attachments']
class ClientImagesGetSerializer(serializers.ModelSerializer):
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
      model= ClientImages
      exclude = ['attachments','client','folder','id']
      extra_fields = ['attachments_list'] 

class ClientFolderSerializer(serializers.ModelSerializer):
     class Meta:
          model = ClientFolder
          fields = ['id','name']  

class ClientFolderGetSerializer(serializers.ModelSerializer):
     class Meta:
          model = ClientFolder
          fields = '__all__'      

class SiteDetailSerializer(serializers.ModelSerializer):
     class Meta:
        model = SiteDetails
        exclude =['active_status']

