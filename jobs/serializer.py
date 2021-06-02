from rest_framework import serializers
import datetime
import os
from .models import Job,JobCard
from .models import Job,JobcardInfo
from sales_quotes.models import Quote
from schedules.models import Schedule
from django.db.models import F

class JobGetSerializer(serializers.ModelSerializer):
    client_name = serializers.SerializerMethodField()
    dp = serializers.SerializerMethodField()
    code = serializers.SerializerMethodField()
    created_date_time = serializers.DateTimeField(format="%d-%b-%Y %I:%M %p")
    created_by = serializers.ReadOnlyField(source='created_by.name')
    amount = serializers.SerializerMethodField()
    paid_amount = serializers.SerializerMethodField()
    amount_paid_status = serializers.SerializerMethodField()
    amount_total_paid_status = serializers.SerializerMethodField()
    paid_status =serializers.ReadOnlyField(source='quote.paid_status')
    vehicle_image = serializers.SerializerMethodField()
    client_latitude = serializers.SerializerMethodField()
    client_longitude = serializers.SerializerMethodField()
    client_id = serializers.SerializerMethodField()
    quote_id = serializers.SerializerMethodField()
    quote_uuid = serializers.SerializerMethodField()
    tab_type = serializers.SerializerMethodField()
    quote_auto_create = serializers.SerializerMethodField()
    quote_invoice_amount = serializers.SerializerMethodField()
    attached_quote_files = serializers.SerializerMethodField()
    schedule = serializers.SerializerMethodField()
    tab_type = serializers.SerializerMethodField()

    def get_tab_type(self, instance):
        try:
            return instance.tab_type
        except:
            pass

    def get_schedule(self, instance):
        try:
            existing_schedule = Schedule.objects.get(job=instance)
            schedule_data = {
                'id':existing_schedule.id,
                'start_date':existing_schedule.start_date,
                'start_time':existing_schedule.start_time,
                'end_time':existing_schedule.end_time,
                'status':existing_schedule.status
            }
            return schedule_data
        except:
            pass

    def get_code(self, instance):
        try:
            return '000'+str(instance.id)
        except:
            pass
        
    def get_client_name(self, instance):
        try:
            return instance.client.client_name
        except:
            pass
    def get_dp(self, instance):
        try:
            return instance.client.dp.url
        except:
            pass    
    def get_amount(self, instance):
        try:
            return instance.amount
        except:
            pass
    
    def get_paid_amount(self, instance):
        try:
            return instance.paid_amount
        except:
            pass

    def get_amount_paid_status(self, instance):
        try:
            if (int(instance.paid_amount)>0):
                return True
            else:
                return False
        except:
            pass

    def get_amount_total_paid_status(self, instance):
        try:
            if(instance.amount==instance.paid_amount):
                return True
            else:
                return False
        except:
            pass
    def get_vehicle_image(self, instance):
        try:
            image_obj =Schedule.objects.get(job_id=instance.id).vehicle.image1.url
            
            return image_obj
        except:
            pass

    def get_client_latitude(self, instance):
        try:
            return instance.client.location_latitude
        except:
            pass       
    def get_client_longitude(self, instance):
        try:
            return instance.client.location_logitude
        except:
            pass    
    def get_client_id(self, instance):
        try:
            return instance.client.client_id
        except:
            pass     
    def get_quote_id(self, instance):
        try:
            return instance.quote.id
        except:
            pass    
    def get_quote_uuid(self, instance):
        try:
            return instance.quote.uuid
        except:
            pass   
    def get_tab_type(self, instance):
        try:
            return instance.quote.tab_type
        except:
            pass   
    def get_quote_auto_create(self, instance):
        try:
            return instance.quote.auto_create
        except:
            pass   
    def get_quote_invoice_amount(self, instance):
        try:
            return instance.quote.invoice_amt
        except:
            pass                    
    def get_attached_quote_files(self,instance):
        try:
            attached_quote_files = []
            for qoute_file in instance.quote.quote_attach_file.all():
                print(qoute_file.id)
                attached_quote_files.append(
                    {
                        'id': qoute_file.id,
                        'file': qoute_file.file.url,
                        'name': os.path.basename(qoute_file.file.url),
                        # 'folder':qoute_file.intranet_archive_folder.name
                    })  
            return attached_quote_files
        except:
            pass             

    class Meta:
        model= Job
        exclude = ['status', 'edited_date_time', 'client']

class CustomJobCardSerializer(serializers.ModelSerializer):
    class Meta:
        model= JobCard
        fields =['id','custom_client_email','custom_job','custom_location_logitude','custom_location_latitude','custom_place','custom_quote_auto_create',
        'custom_building','custom_device_capacity','custom_device_waste','custom_barcode','custom_site_address','custom_site_suburb','custom_post_code',
        'custom_bar_code_for_grease_trap_only','custom_access_restriction','custom_pit_location','custom_company_suburb','custom_company_mobile_number',
        'custom_company_contact_number','custom_company_email','custom_company_postcode','custom_information','custom_induction_type']

class CustomJobCardGetSerializer(serializers.ModelSerializer):                             
    class Meta:
        model= JobCard
        fields ='__all__'
        

class JobCardGetSerializer(serializers.ModelSerializer):
    customer_id = serializers.SerializerMethodField()
    customer_name = serializers.SerializerMethodField()
    site_location = serializers.SerializerMethodField()
    site_suburb = serializers.SerializerMethodField()
    quote_id = serializers.ReadOnlyField(source='quote.id')
    schedule_date = serializers.SerializerMethodField()
    # schedule =Schedule.objects.get(id=)
    truck_number = serializers.SerializerMethodField()
    technician_name =serializers.SerializerMethodField()
    duration =serializers.SerializerMethodField()
    site_contact_name = serializers.SerializerMethodField()
    mobile_number = serializers.SerializerMethodField()
    phone_number = serializers.SerializerMethodField()
    service_time = serializers.SerializerMethodField()
    security_key_required = serializers.SerializerMethodField()
    access_restriction  = serializers.SerializerMethodField()
    aditional_information = serializers.SerializerMethodField()
    pit_location = serializers.SerializerMethodField()
    date_service_complete = serializers.SerializerMethodField()
    payment_details = serializers.SerializerMethodField()
    capacity =  serializers.SerializerMethodField()
    code = serializers.SerializerMethodField()
    signature = serializers.SerializerMethodField()
    created_date_time = serializers.DateTimeField(format="%d-%b-%Y %I:%M %p")
    created_by = serializers.ReadOnlyField(source='created_by.name')
    induction_type = serializers.SerializerMethodField()
    # registration = serializers.SerializerMethodField()
    def get_code(self, instance):
        try:
            try:
                quote = self.context.get('quote',None)
                job_obj = Job.objects.get(quote__id=quote)
            except:
               return "Not Scheduled"  
            return '000'+str(job_obj.id)
        except:
            pass
        
    def get_customer_id(self, instance):
        try:
            return instance.client.client_id
        except:
            pass
    def get_customer_name(self, instance):
        try:
            return instance.client.client_name
        except:
            pass    
    def get_schedule_date(self,instance):
        quote = self.context.get('quote',None)
        try:
            job_obj = Job.objects.get(quote__id=quote)
        except:
               return "Not Scheduled" 
      
        schedule =Schedule.objects.filter(job=job_obj).exists()
        print(schedule)
        if schedule:
            schedule_obj =Schedule.objects.get(job=job_obj)
            schedule_date =schedule_obj.start_date

            return schedule_date
        else:
            return "Not Scheduled"
    def get_signature(self,instance):
        quote = self.context.get('quote',None)

        try:
            job_obj = Job.objects.get(quote__id=quote)
        except:
               return "Not Scheduled"
        
        schedule =Schedule.objects.filter(job=job_obj).exists()
        print(schedule)
        if schedule:
            try:
                schedule_obj =Schedule.objects.get(job=job_obj)
                signature =schedule_obj.image.url
            except:
                signature =None
            return signature
        else:
            return "Not Scheduled"        
    def get_truck_number(self,instance):
        quote = self.context.get('quote',None)
        try:
            job_obj = Job.objects.get(quote__id=quote)
        except:
               return "Not Scheduled" 
        schedule =Schedule.objects.filter(job=job_obj).exists()
        print(schedule)
        if schedule:
            schedule_obj =Schedule.objects.get(job=job_obj)
            registration =schedule_obj.vehicle.registration

            return str(registration)
        else:
            return "Not Scheduled"   
    def get_technician_name(self,instance):
        quote = self.context.get('quote',None)
        try:
            job_obj = Job.objects.get(quote__id=quote)
        except:
               return "Not Scheduled" 
        schedule =Schedule.objects.filter(job=job_obj).exists()
        if schedule:
            schedule_obj =Schedule.objects.get(job=job_obj)
            team =schedule_obj.team_employees.all()
            for employee in team:
                if employee.user_type =='technician':
                    return employee.name
                    

        else:
            return "Not Scheduled"

    def get_duration(self,instance):
        quote = self.context.get('quote',None)
        try:
            job_obj = Job.objects.get(quote__id=quote)
        except:
               return "Not Scheduled" 
        schedule =Schedule.objects.filter(job=job_obj).exists()
        if schedule:
            schedule_obj =Schedule.objects.get(job=job_obj)
            if schedule_obj.start_date !=" ":
                end = str(schedule_obj.end_time)[:-3]
                start = str(schedule_obj.start_time)[:-3]
                end_time = float(end.replace(':', '.'))
                start_time = float(start.replace(':', '.'))
                diff=end_time - start_time
                mean_time=str(diff)
                mean_time[0:5]
                hours =round(float(mean_time))
                if hours <1:
                    return str(1) + " hours"
                return str(hours) + " hours"
        else:
            return "Not Scheduled"   

    def get_site_contact_name(self, instance):
        try:
            return instance.client.site_address
        except:
            pass        
     
    def get_mobile_number(self, instance):
        try:
            return instance.client.company_mobile_number
        except:
            pass    
    def get_phone_number(self, instance):
        try:
            return instance.client.company_contact_number
        except:
            pass   
    def get_service_time(self,instance):
        quote = self.context.get('quote',None)
        try:
            job_obj = Job.objects.get(quote__id=quote)
        except:
               return "Not Scheduled" 
        schedule =Schedule.objects.filter(job=job_obj).exists()
        if schedule:
            schedule_obj =Schedule.objects.get(job=job_obj)
            end = str(schedule_obj.end_time)[:-3]
            start = str(schedule_obj.start_time)[:-3]
            end_time = float(end.replace(':', '.'))
            start_time = float(start.replace(':', '.'))
            diff=end_time - start_time
            mean_time=str(diff)
            mean_time[0:5]
            hours =round(float(mean_time))
            if hours <1:
                return str(1) + " hours"
            return str(hours) + " hours"
            

        else:
            return "Not Scheduled"        

    def get_security_key_required(self, instance):
        try:
            return instance.client.key_required_type
        except:
            pass
    def get_access_restriction(self, instance):
        try:
            quote = self.context.get('quote',None)
            if instance.client.access_restriction == None:
                job_card_obj = JobCard.objects.get(custom_quote__id=quote)
                return job_card_obj.custom_access_restriction
            return instance.client.access_restriction
        except:
            pass  
    def get_site_location(self, instance):
        try:
            quote = self.context.get('quote',None)
            if instance.client.site_address == None:
                job_card_obj = JobCard.objects.get(custom_quote__id=quote)
                return job_card_obj.custom_site_address
            return instance.client.site_address
        except:
            pass    
    def get_site_suburb(self, instance):
        try:
            quote = self.context.get('quote',None)
            if instance.client.site_suburb == None:
                job_card_obj = JobCard.objects.get(custom_quote__id=quote)
                return job_card_obj.custom_site_suburb
            return instance.client.site_address
        except:
            pass                    
    def get_aditional_information(self, instance):
        try:
            quote = self.context.get('quote',None)
            if instance.client.information == None:
                job_card_obj = JobCard.objects.get(custom_quote__id=quote)
                return job_card_obj.custom_information
            return instance.client.information
        except:
            pass          
    def get_pit_location(self, instance):
        try:
            quote = self.context.get('quote',None)
            if instance.client.pit_location == None:
                job_card_obj = JobCard.objects.get(custom_quote__id=quote)
                return job_card_obj.custom_pit_location
            return instance.client.pit_location 
        except:
            pass      
    def get_date_service_complete(self, instance):
        try:
            return instance.client.next_service_1 
        except:
            pass      
    def get_payment_details(self, instance):
        try:
            return instance.client.payment_type 
        except:
            pass         
    def get_capacity(self, instance):
        try:
            return instance.client.device_capacity 
        except:
            pass  
    def get_induction_type(self, instance):
        try:
            return instance.client.induction_type
        except:
            pass                                    
 

   
    class Meta:
        model= Quote
        exclude = ['status', 'edited_date_time', 'client']






class QuoteCardGetSerializer(serializers.ModelSerializer):
    customer_id = serializers.SerializerMethodField()
    customer_name = serializers.SerializerMethodField()
    site_location = serializers.ReadOnlyField(source='client.site_address')
    site_suburb = serializers.ReadOnlyField(source='client.site_suburb')
    quote_id = serializers.ReadOnlyField(source='quote.id')
    schedule_date = serializers.SerializerMethodField()
    # schedule =Schedule.objects.get(id=)
    truck_number = serializers.SerializerMethodField()
    technician_name =serializers.SerializerMethodField()
    duration =serializers.SerializerMethodField()
    site_contact_name = serializers.SerializerMethodField()
    mobile_number = serializers.SerializerMethodField()
    phone_number = serializers.SerializerMethodField()
    service_time = serializers.SerializerMethodField()
    security_key_required = serializers.SerializerMethodField()
    access_restriction  = serializers.SerializerMethodField()
    aditional_information = serializers.SerializerMethodField()
    pit_location = serializers.SerializerMethodField()
    date_service_complete = serializers.SerializerMethodField()
    payment_details = serializers.SerializerMethodField()
    capacity =  serializers.SerializerMethodField()
    code = serializers.SerializerMethodField()
    signature = serializers.SerializerMethodField()
    created_date_time = serializers.DateTimeField(format="%d-%b-%Y %I:%M %p")
    created_by = serializers.ReadOnlyField(source='created_by.name')
    induction_type = serializers.SerializerMethodField()
    
     
    def get_code(self, instance):
        try:
            job_obj = Job.objects.get(quote =instance.custom_quote.id)
            return '000'+str(job_obj.id)
        except:
            return " "
            pass
        
    def get_customer_id(self, instance):
        try:
            return instance.custom_quote.client.client_id
        except:
            return " "
    def get_customer_name(self, instance):
        try:
            return instance.custom_quote.client.client_name
        except:
            pass    
    def get_schedule_date(self,instance):
        quote = self.context.get('quote',None)

        job_obj = Job.objects.get(quote__id = quote)
      
        schedule =Schedule.objects.filter(job=job_obj).exists()
        print(schedule)
        if schedule:
            schedule_obj =Schedule.objects.get(job=job_obj)
            schedule_date =schedule_obj.start_date

            return schedule_date
        else:
            return "Not Scheduled"
    def get_signature(self,instance):
        quote = self.context.get('quote',None)

        job_obj = Job.objects.get(quote__id = quote)
        schedule =Schedule.objects.filter(job=job_obj).exists()
        print(schedule)
        if schedule:
            try:
                schedule_obj =Schedule.objects.get(job=job_obj)
                signature =schedule_obj.image.url
            except:
                signature =None
            return signature
        else:
            return "Not Scheduled"        
    def get_truck_number(self,instance):
        quote = self.context.get('quote',None)
        job_obj = Job.objects.get(quote__id = quote)

        schedule =Schedule.objects.filter(job=job_obj).exists()
        print(schedule)
        if schedule:
            schedule_obj =Schedule.objects.get(job=job_obj)
            registration =schedule_obj.vehicle.registration

            return registration
        else:
            return "Not Scheduled"   
    def get_technician_name(self,instance):
        quote = self.context.get('quote',None)
        job_obj = Job.objects.get(quote__id = quote)
        schedule =Schedule.objects.filter(job=job_obj).exists()
        if schedule:
            schedule_obj =Schedule.objects.get(job=job_obj)
            team =schedule_obj.team_employees.all()
            for employee in team:
                if employee.user_type =='technician':
                    return employee.name
                    

        else:
            return "Not Scheduled"

    def get_duration(self,instance):
        quote = self.context.get('quote',None)
        job_obj = Job.objects.get(quote__id = quote)
        schedule =Schedule.objects.filter(job=job_obj).exists()
        if schedule:
            schedule_obj =Schedule.objects.get(job=job_obj)
            if schedule_obj.start_date !=" ":
                end = str(schedule_obj.end_time)[:-3]
                start = str(schedule_obj.start_time)[:-3]
                end_time = float(end.replace(':', '.'))
                start_time = float(start.replace(':', '.'))
                diff=end_time - start_time
                mean_time=str(diff)
                mean_time[0:5]
                hours =round(float(mean_time))
                if hours <1:
                    return str(1) + " hours"
                return str(hours) + " hours"
        else:
            return "Not Scheduled"   

    def get_site_contact_name(self, instance):
        try:
            return instance.custom_quote.client.site_address
        except:
            pass        
     
    def get_mobile_number(self, instance):
        try:
            return instance.custom_quote.client.company_mobile_number
        except:
            pass    
    def get_phone_number(self, instance):
        try:
            return instance.custom_quote.client.company_contact_number
        except:
            pass   
    def get_service_time(self,instance):
        quote = self.context.get('quote',None)
        job_obj = Job.objects.get(quote__id = quote)
        schedule =Schedule.objects.filter(job=job_obj).exists()
        if schedule:
            schedule_obj =Schedule.objects.get(job=job_obj)
            end = str(schedule_obj.end_time)[:-3]
            start = str(schedule_obj.start_time)[:-3]
            end_time = float(end.replace(':', '.'))
            start_time = float(start.replace(':', '.'))
            diff=end_time - start_time
            mean_time=str(diff)
            mean_time[0:5]
            hours =round(float(mean_time))
            if hours <1:
                return str(1) + " hours"
            return str(hours) + " hours"
            

        else:
            return "Not Scheduled"        

    def get_security_key_required(self, instance):
        try:
            return instance.custom_quote.client.key_required_type
        except:
            pass
    def get_access_restriction(self, instance):
        try:
            return instance.custom_quote.client.access_restriction
        except:
            pass                
    def get_aditional_information(self, instance):
        try:
            return instance.custom_quote.client.information
        except:
            pass          
    def get_pit_location(self, instance):
        try:
            return instance.custom_quote.client.pit_location 
        except:
            pass      
    def get_date_service_complete(self, instance):
        try:
            return instance.custom_quote.client.next_service_1 
        except:
            pass      
    def get_payment_details(self, instance):
        try:
            return instance.custom_quote.client.payment_type 
        except:
            pass         
    def get_capacity(self, instance):
        try:
            return instance.custom_quote.client.device_capacity 
        except:
            pass  
    def get_induction_type(self, instance):
        try:
            return instance.custom_quote.client.induction_type
        except:
            pass                                    
 

   
    class Meta:
        model= JobCard
        exclude = ['edited_date_time']

class JobCardInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model= JobcardInfo
        fields =['id','tab_type','quote','client','payment_details','company_name','company_address',
        'suburb','postal_code','job_site_address','building_name','contact_email_address','contact_number','job_site_contact_name','access_restriction',
        'tc_required','waste_data_form','access_height','key_required','security_required','induction_required','contact_name',
        'phone_number','type_of_induction','pit_distacnce_from_truck_location','water_tap_location','gumy_required','confined_space',
        'number_of_trucks_required','specific_ppe_reqired','service_time','if_yes_specify','completed_by','date','services']

class JobCardInfoGetSerializer(serializers.ModelSerializer):  
    connected =   serializers.SerializerMethodField() 
    service_list = serializers.SerializerMethodField() 
    def get_connected(self, instance):
            connected_status = instance.quote
            if connected_status ==None:
                return False
            else:
                return True
    def get_service_list(self, instance):   
        service_list = []       
        each_service_list = instance.services.get_queryset()            
        for i in each_service_list:
                try:
                    service_list.append(
                        {
                            'id': i.id,
                            'no':i.no,
                            'capacity': i.capacity,
                            'waste_type': i.waste_type,
                            'pit_location':i.pit_location,
                            'frequency': i.frequency
        
                        }
                    )
                except:
                    pass      
        return service_list              
                              
    class Meta:

        model= JobcardInfo
        extra_fields =['service_list','connected']
        exclude =['services']
                