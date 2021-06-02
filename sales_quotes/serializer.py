from rest_framework import serializers
from accounts.models import Client
from .models import(JobImages,
DummyTemplate,Products,UserQuoteTemplate,TemplateDraft,UserSafetyData,QuoteAttachTemplates,TypeOfWaste)
from clients.serializers import ClientImagesGetSerializer
import datetime
from .models import Quote,LoggingInfo,ClientQuoteAttachmentResponses
from jobs.models import Job
import os
from drive.models import Files

  


class QuoteGetSerializer(serializers.ModelSerializer):
    file_list = serializers.SerializerMethodField()
    sale_person = serializers.ReadOnlyField(source='employee.name') 
    contact_number = serializers.ReadOnlyField(source='employee.contact_number')
    customer = serializers.ReadOnlyField(source='client.client_name')
    date = serializers.SerializerMethodField()
    won_reject_date = serializers.SerializerMethodField()

    def get_date(self, instance):
        string_date = str(instance.date)
        date = string_date[:10]
        return date
    def get_won_reject_date(self, instance):
        string_date = str(instance.won_reject_date)
        won_reject_date = string_date[:10]
        return won_reject_date

    def get_file_list(self, instance):
        file_list = []
        each_attachments = instance.quote_attach_files_in.get_queryset()
        for i in each_attachments:
            try:
                file_list.append(
                    {
                        'id': i.id,
                        'file': i.file_item.url,
                        'type': (i.file_item.url).split('.')[-1],
                        'name': os.path.basename(i.file_item.url),
                        'folder':i.intranet_archive_folder.name
                    }
            )
            except:
                pass
        return file_list
    class Meta:
        model= Quote
        exclude = ['quote_attach_files_in']
        extra_fields = ['id','file_list','uuid','status','dates']       

class JobGetSerializer(serializers.ModelSerializer):
    job_code = serializers.SerializerMethodField()
    quoted_by = serializers.ReadOnlyField(source='created_by.name')
    contact_number = serializers.ReadOnlyField(source='employee.contact_number')
    client_id = serializers.ReadOnlyField(source='client.client_id') 
    client_name = serializers.ReadOnlyField(source='client.client_name')
    client_type = serializers.ReadOnlyField(source='client.client_type') 
    paid_status = serializers.ReadOnlyField(source='quote.paid_status')   
    date = serializers.SerializerMethodField()
    # won_reject_date = serializers.SerializerMethodField()

    def get_date(self, instance):
        string_date = str(instance.created_date_time)
        date = string_date[:10]
        return date
    # def get_won_reject_date(self, instance):
    #     string_date = str(instance.won_reject_date)
    #     won_reject_date = string_date[:10]
    #     return won_reject_date 
    def get_job_code(self, instance):
        try:
            return '000'+str(instance.id)
        except:
            pass   
    class Meta:
        model= Job
        exclude = []
        extra_fields = ['id']   

class JobDetailsGetSerializer(serializers.ModelSerializer):
  
   client_id = serializers.ReadOnlyField(source='client.client_id') 
   client_name = serializers.ReadOnlyField(source='client.client_name') 
   location_latitude = serializers.ReadOnlyField(source='client.location_latitude')  
   location_logitude = serializers.ReadOnlyField(source='client.location_logitude')  
   building = serializers.ReadOnlyField(source='client.building') 
   class Meta:
      model= Quote
      exclude = ['uuid','status','employee','won_reject_date','date',
      'quote_attach_file','template','reoccurring','auto_create','url','job_type','invoice_amt','company_name']
      extra_fields = ['id']   

class JobImagesSerializer(serializers.ModelSerializer):
     class Meta:
        model = JobImages
        exclude = ['attachments']
class JobImagesGetSerializer(serializers.ModelSerializer):
   attachments_list = serializers.SerializerMethodField()

   def get_attachments_list(self, instance):
        attachments_list = []
        each_attachments = instance.attachments.get_queryset()
        for i in each_attachments:
            try:
                attachments_list.append(
                    {
                        'id': i.id,
                        'file': i.file.url,
                        'type': (i.file.url).split('.')[-1],
                        'name': os.path.basename(i.file.url)

      
                    }
            )
            except:
                pass

        return attachments_list
   class Meta:
      model= JobImages
      exclude = ['attachments']
      extra_fields = ['attachments_list','id']     


class DummyTemplateGetSerializer(serializers.ModelSerializer):
    class Meta:
        model =DummyTemplate
        field = '__all__'

class ProductsSerializer(serializers.ModelSerializer):
     class Meta:
        model = Products
        fields =['name']
class ProductsGetSerializer(serializers.ModelSerializer):
     class Meta:
        model = Products
        fields = '__all__'
   
class UserQuoteTemplateGetSerializer(serializers.ModelSerializer):
     class Meta:
        model = UserQuoteTemplate
        exclude = ['template']
        extra_fields = ['id']    
class SingleUserQuoteTemplateGetSerializer(serializers.ModelSerializer):
     class Meta:
        model = UserQuoteTemplate
        fields = '__all__'        

class TemplateDraftSerializer(serializers.ModelSerializer):
     class Meta:
        model = TemplateDraft
        fields = ['created_by','client','template','tab_type']  
class TemplateDraftGetSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()

    client_name = serializers.SerializerMethodField()
    def get_client_name(self, instance):
        client_name = str(instance.client.client_name)
        return client_name
    def get_employee_name(self, instance):
        employee_name = str(instance.created_by.name)
        return employee_name     
    class Meta:
        model = TemplateDraft
        exclude = ['template']
        extra_fields = ['id','client_name','employee_name']
class TemplateDraftGetAllSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()

    client_name = serializers.SerializerMethodField()
    def get_client_name(self, instance):
        client_name = str(instance.client.client_name)
        return client_name
    def get_employee_name(self, instance):
        employee_name = str(instance.created_by.name)
        return employee_name     
    class Meta:
        model = TemplateDraft
        exclude = []
        extra_fields = ['id','client_name','employee_name'] 


                     
class SingleTemplateDraftSerializer(serializers.ModelSerializer):
     class Meta:
        model = TemplateDraft
        fields = '__all__'
        
class UserSafetyDataGetSerializer(serializers.ModelSerializer):
     class Meta:
        model = UserSafetyData
        exclude = ['safety_data']
        extra_fields = ['id']    
class SingleUserSafetyDataGetSerializer(serializers.ModelSerializer):
     class Meta:
        model = UserSafetyData
        fields = '__all__'        

class QuoteAttachTemplatesSerializer(serializers.ModelSerializer):
     class Meta:
        model = QuoteAttachTemplates
        fields = ['id','quote_attach_template','template_name']

class QuoteAttachTemplatesGetSerializer(serializers.ModelSerializer):

   
    class Meta:
       
       
        model = QuoteAttachTemplates
        exclude = ['template']
        extra_fields = ['id'] 
        





class TypeOfWasteSerializer(serializers.ModelSerializer):
     class Meta:
        model = TypeOfWaste
        fields = ['id','w_type']

class TypeOfWasteGetSerializer(serializers.ModelSerializer):
     class Meta:
        model = TypeOfWaste
        fields = '__all__' 

class LoggingInfoSerializer(serializers.ModelSerializer):
     class Meta:
        model = LoggingInfo
        fields = ['id','tab_type','message','employee']

class LoggingInfoGetSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()

    def get_date(self, instance):
        from datetime import datetime as dt
        t = str(instance.created_date_time)
        date = t[:-22]
        # time = datetime.datetime.strptime(t,%H:%M")
        
        
        
            
        return date
    def get_time(self, instance):
        
        t = instance.created_date_time
       
        
        time = t.strftime("%X")
        
            
        return time    
    class Meta:
        model = LoggingInfo
        extra_fields = ['time']
        exclude = ['created_date_time','edited_date_time']
class ClientQuoteAttachmentResponsesGetSerializer(serializers.ModelSerializer):
     class Meta:
        model = ClientQuoteAttachmentResponses
        fields = '__all__'         