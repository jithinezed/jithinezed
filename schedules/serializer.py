from rest_framework import serializers
import datetime
from datetime import datetime
import os

from .models import Schedule,Schedule_comment,AdditionalVehicles
from vehicles.models import Vehicle, PreInspectionCheck
from accounts.models import Employee,Client
from jobs.models import Job

class ScheduleGetSerializer(serializers.ModelSerializer):
    client = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    job_type = serializers.SerializerMethodField()
    amount = serializers.SerializerMethodField()
    paid_amount = serializers.SerializerMethodField()
    amount_paid_status = serializers.SerializerMethodField()
    amount_total_paid_status = serializers.SerializerMethodField()
    pending_amount = serializers.SerializerMethodField()
    vehicle = serializers.SerializerMethodField()
    team_employees = serializers.SerializerMethodField()
    shift = serializers.SerializerMethodField()
    gallery = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    tab_type = serializers.SerializerMethodField()
    quote_id = serializers.SerializerMethodField()

    def get_quote_id(self, instance):
        try:
            return instance.job.quote.id
        except:
            pass

    def get_tab_type(self, instance):
        try:
            return instance.tab_type
        except:
            pass

    def get_status(self, instance):
        try:
            return instance.status
        except:
            pass
    # def get_signature(self, instance):
    #     try:
    #         return instance.image.url
    #     except:
    #         pass     
        
    def get_client(self, instance):
        try:
            return instance.job.client.client_name
        except:
            pass
    
    def get_shift(self, instance):
        try:
            if instance.start_time >= datetime.strptime('16:00:00', '%H:%M:%S').time() :
                return '3'
            elif instance.start_time >= datetime.strptime('11:00:00', '%H:%M:%S').time() :
                return '2'
            else:
                return '1'
        except Exception as E:
            print(E)
            pass

    def get_address(self, instance):
        try:
            return instance.job.client.site_address
        except:
            pass

    def get_job_type(self, instance):
        try:
            return instance.job.job_type
        except:
            pass

    def get_amount(self, instance):
        try:
            return instance.job.amount
        except:
            pass
    
    def get_paid_amount(self, instance):
        try:
            return instance.job.paid_amount
        except:
            pass

    def get_pending_amount(self, instance):
        try:
            return str(float(instance.job.amount) - float(instance.job.paid_amount))
        except:
            pass

    def get_amount_paid_status(self, instance):
        try:
            if (int(instance.job.paid_amount)>0):
                return True
            else:
                return False
        except:
            pass

    def get_vehicle(self, instance):
        try:
            return instance.vehicle.registration
        except:
            pass

    def get_amount_total_paid_status(self, instance):
        try:
            if(instance.job.amount==instance.job.paid_amount):
                return True
            else:
                return False
        except:
            pass
    
    def get_team_employees(self, instance):
        try:
            team = []
            for member in instance.team_employees.all():
                team.append({'id':member.id, 'name':member.name, 'dp':member.dp.url})
            return team
        except:
            pass
    def get_gallery(self, instance):
        try:
            gallery = []
            for image in instance.gallery.all():
                gallery.append({'id':image.id,  'file':image.file.url})
            return gallery
        except:
            pass   
    def get_comments(self, instance):
        try:
            comments = []
            employee = self.context.get('member',None)
            employee_obj = Employee.objects.get(id=employee)
            for comment in instance.comments.all():
                if comment.employee == employee_obj:
                    comments.append({'id':comment.id,'comment':comment.comment,'created_by':comment.employee.name,'author':True})
                    
                else:
                    comments.append({'id':comment.id,'comment':comment.comment,'created_by':comment.employee.name,'author':False})
            return comments
        except:
            pass        

    class Meta:
        model= Schedule
        exclude = ['edited_date_time']

class ScheduleMobileGetSerializer(serializers.ModelSerializer):
    client = serializers.SerializerMethodField()
    quote_id = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField()
    job_type = serializers.SerializerMethodField()
    amount = serializers.SerializerMethodField()
    paid_amount = serializers.SerializerMethodField()
    amount_paid_status = serializers.SerializerMethodField()
    amount_total_paid_status = serializers.SerializerMethodField()
    pending_amount = serializers.SerializerMethodField()
    vehicle = serializers.SerializerMethodField()
    team_employees = serializers.SerializerMethodField()
    shift = serializers.SerializerMethodField()
    gallery = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    def get_quote_id(self, instance):
        return '000'+str(instance.job.quote_id)
        
    def get_created_by(self, instance):
        return instance.job.created_by.name
        


    def get_client(self, instance):
        try:
            data = {
                'client_id': instance.job.client.client_name,
                'client_type': instance.job.client.client_name,
                'client_name': instance.job.client.client_name,
                'client_email': instance.job.client.client_name,
                'location_logitude': instance.job.client.client_name,
                'location_latitude': instance.job.client.client_name,
                'place': instance.job.client.client_name,
                'building': instance.job.client.client_name,
                'dp': instance.job.client.client_name,
                'device_capacity': instance.job.client.client_name,
                'device_waste': instance.job.client.client_name,
                'barcode': instance.job.client.client_name,
                'site_address': instance.job.client.client_name,
                'site_suburb': instance.job.client.client_name,
                'post_code': instance.job.client.client_name,
                'bar_code_for_grease_trap_only': instance.job.client.client_name,
                'account_type': instance.job.client.client_name,
                'pit_location': instance.job.client.client_name,
                'access_registration': instance.job.client.client_name,
                'company_suburb': instance.job.client.client_name,
                'company_contact_number': instance.job.client.client_name,
                'company_mobile_number': instance.job.client.client_name,
                'company_landline_number': instance.job.client.client_name,
                'company_email': instance.job.client.client_name,
                'company_postcode': instance.job.client.client_name,
                'information': instance.job.client.client_name,
            }
            return data
        except:
            pass
    
    def get_shift(self, instance):
        try:
            if instance.start_time >= datetime.strptime('16:00:00', '%H:%M:%S').time() :
                return '3'
            elif instance.start_time >= datetime.strptime('11:00:00', '%H:%M:%S').time() :
                return '2'
            else:
                return '1'
        except Exception as E:
            print(E)
            pass

    def get_address(self, instance):
        try:
            return instance.job.client.site_address
        except:
            pass

    def get_job_type(self, instance):
        try:
            return instance.job.job_type
        except:
            pass

    def get_amount(self, instance):
        try:
            return instance.job.amount
        except:
            pass
    
    def get_paid_amount(self, instance):
        try:
            return instance.job.paid_amount
        except:
            pass

    def get_pending_amount(self, instance):
        try:
            return str(float(instance.job.amount) - float(instance.job.paid_amount))
        except:
            pass

    def get_amount_paid_status(self, instance):
        try:
            if (int(instance.job.paid_amount)>0):
                return True
            else:
                return False
        except:
            pass

    def get_vehicle(self, instance):
        try:
            return instance.vehicle.registration
        except:
            pass

    def get_amount_total_paid_status(self, instance):
        try:
            if(instance.job.amount==instance.job.paid_amount):
                return True
            else:
                return False
        except:
            pass
    
    def get_team_employees(self, instance):
        try:
            team_employees = []
            if instance.team_employees.all() ==None:
                return team_employees
            for member in instance.team_employees.all():
                print(member)
               
                try: 
                    team_employees.append({'id':member.id, 'name':member.name, 'dp':member.dp.url})
                except:
                    pass
        except:
            pass
        return team_employees 
    def get_gallery(self, instance):
        try:
            gallery = []
            for image in instance.gallery.all():
                gallery.append({'id':image.id,  'file':image.file.url})
            return gallery
        except:
            pass
    def get_comments(self, instance):
        try:
            comments = []
            employee = self.context.get('member',None)
            employee_obj = Employee.objects.get(id=employee)
            for comment in instance.comments.all():
                if comment.employee == employee_obj:
                    comments.append({'id':comment.id,'comment':comment.comment,'created_by':comment.employee.name,'editable':True})
                    return comments
                else:
                    comments.append({'id':comment.id,'comment':comment.comment,'created_by':comment.employee.name,'editable':False})
                    return comments

        except:
            pass            
    

    class Meta:
        model= Schedule
        exclude = ['edited_date_time']


class VehicleSerializer(serializers.ModelSerializer):
    is_available = serializers.SerializerMethodField()
    pre_inspection_check = serializers.SerializerMethodField()

    def get_pre_inspection_check(self, instance):
        try:
            today = datetime.now()
            pre_inspection_check_status = PreInspectionCheck.objects.get(vehicle=instance, date_time=today.strftime('%Y-%m-%d'))
            return True
        except:
            return False
    
    def get_is_available(self, instance):
        try:
            start = self.context.get('start',None)

            end = self.context.get('end',None)
            start_date = start[:-9]
            print(start_date)
            end_date = end[:-9]
            print(end_date)
            start_time = start[-8:]
            print(start_time)
            end_time = end[-8:]
            all_schedule = Schedule.objects.filter(vehicle=instance).filter(start_date__lte=end_date,end_date__gte=start_date).filter(end_time__gte=start_time, start_time__lte=end_time).exclude(status='completed')
            print(all_schedule.count())
            if all_schedule.count()==0:
                return True
            else:
                return False
        except:
            print("exception")
            return False

    class Meta:
        model = Vehicle
        fields = ['id','vehicle_type','registration','is_available', 'pre_inspection_check']
        # extra_fields = []

class EmployeeSerializer(serializers.ModelSerializer):
    is_available = serializers.SerializerMethodField()
    terminated_status = serializers.SerializerMethodField()

    def get_is_available(self, instance):
        try:
            start = self.context.get('start',None)
           
            end = self.context.get('end',None)
            start_date = start[:-9]
            end_date = end[:-9]

            start_time = start[-8:]
            end_time = end[-8:]
            all_schedule = Schedule.objects.filter(team_employees=instance).filter(start_date__lte=end_date,end_date__gte=start_date).filter(end_time__gte=start_time, start_time__lte=end_time).exclude(status='completed')
            if all_schedule.count()==0:
                return True
            else:
                return False
        except:
            return False
    def get_terminated_status(self, instance):
        try:
            print ("termination_date__isnull")
            if instance.termination_date !=None or instance.active_status ==False:
                return True
            else:
                print("dfhg")
                return False 
        except Exception as E:
            print(str(E))     

               
    class Meta:
        model = Employee
        fields = ['id', 'employee_id', 'name', 'dp', 'user_type', 'is_available','terminated_status']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule_comment
        fields = ['comment','employee']


class CommentGetSerializer(serializers.ModelSerializer):
    comments =serializers.SerializerMethodField()
    def get_comments(self,instance):
        comments =[]
        employee = self.context.get('member',None)
        employee_obj = Employee.objects.get(id=employee)
        print(instance.comment)
        if instance.employee == employee_obj:
            comments.append({'id':instance.id,'comment':instance.comment,'created_by':instance.employee.name,'author':True}) 
        else:
            comments.append({'id':instance.id,'comment':instance.comment,'created_by':instance.employee.name,'author':False})
        return comments
    class Meta:
        model= Schedule_comment
        exclude = ['edited_date_time','comment','employee','created_date_time']
        extra_fields =['comments']

class JobSingleGetSerializer(serializers.ModelSerializer):  

    client_name = serializers.SerializerMethodField()
    client_id = serializers.SerializerMethodField()
    dp = serializers.SerializerMethodField()
    company_name =serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    job_type = serializers.SerializerMethodField()
    code = serializers.SerializerMethodField()
    amount = serializers.SerializerMethodField()
    paid_amount = serializers.SerializerMethodField()
    amount_paid_status = serializers.SerializerMethodField()
    amount_total_paid_status = serializers.SerializerMethodField()
    pending_amount = serializers.SerializerMethodField()
    client_latitude = serializers.SerializerMethodField()
    client_longitude = serializers.SerializerMethodField()
    vehicle = serializers.SerializerMethodField()
    # shift = serializers.SerializerMethodField()
    schedule = serializers.SerializerMethodField()
    quote = serializers.SerializerMethodField()
    # comments = serializers.SerializerMethodField()
    

    def get_client_name(self, instance):
        try:
            return instance.client.client_name
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
    def get_dp(self, instance):
        try:
            return instance.client.dp.url
        except:
            pass
    def get_company_name(self, instance):
        try:
            return instance.quote.company_name
        except:
            pass   
    def get_code(self, instance):
        try:
            return '000'+str(instance.id)
        except:
            pass 
    def get_address(self, instance):
        try:
            return instance.client.site_address
        except:
            pass

    def get_job_type(self, instance):
        try:
            return instance.job_type
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

    def get_pending_amount(self, instance):
        try:
            return str(float(instance.amount) - float(instance.paid_amount))
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
    
    
    def get_quote(self,instance):
        try:
            quote_data ={}
            try:
                attached_quote_files = []
                for qoute_file in instance.quote.quote_attach_file.all():
                    attached_quote_files.append(
                        {
                            'id': qoute_file.id,
                            'file': qoute_file.file.url,
                            'name': os.path.basename(qoute_file.file.url),
                            # 'folder':qoute_file.intranet_archive_folder.name
                        })
               
            
            except:
                pass
            quote_data = {
                'quote_id':instance.quote.id,
                'quote_uuid':instance.quote.uuid,
                'quote_template':instance.quote.template.url,
                'tab_type':instance.quote.tab_type,
                'quote_auto_create':instance.quote.auto_create,
                'quote_invoice_amount':instance.quote.invoice_amt,
                'attached_quote_files':attached_quote_files,
                'reoccurring':instance.quote.reoccurring,
                'auto_create':instance.quote.auto_create,
                'status':instance.quote.status,
                'won_reject_date':instance.quote.won_reject_date,
                'date':instance.quote.date,
                'client':instance.quote.client.client_name,
                'paid_status':instance.quote.paid_status,
                'invoice_amt':instance.quote.invoice_amt,
                'company_name':instance.quote.company_name,
                'amount':instance.quote.amount
                
                }

            return quote_data

        except:
            pass    

    def get_schedule(self, instance):
        try:
            schedule_data ={}
            if Schedule.objects.filter(job=instance).exists():
                existing_schedule = Schedule.objects.get(job=instance)
                try:
                    team = []
                    for member in existing_schedule.team_employees.all():
                        team.append({'id':member.id, 'name':member.name, 'dp':member.dp.url})
                except:
                    pass
                try:
                    gallery = []
                    for image in existing_schedule.gallery.all()[:3]:
                        gallery.append({'id':image.id,  'file':image.file.url})
                
                except:
                    pass  
                try:
                    comments = []
                    employee = self.context.get('member',None)
                    employee_obj = Employee.objects.get(id=employee)
                    for comment in instance.comments.all():
                        if comment.employee == employee_obj:
                            comments.append({'id':comment.id,'comment':comment.comment,'created_by':comment.employee.name,'editable':True})
                            return comments
                        else:
                            comments.append({'id':comment.id,'comment':comment.comment,'created_by':comment.employee.name,'editable':False})
                            

                except:
                    pass
                existing_schedule = Schedule.objects.get(job=instance)
                try:
                    signature = existing_schedule.image.url
                except:
                    signature = None    

                schedule_data = {
                    'id':existing_schedule.id,
                    'start_date':existing_schedule.start_date,
                    'start_time':existing_schedule.start_time,
                    'end_time':existing_schedule.end_time,
                    'status':existing_schedule.status,
                    'get_team_employees':team,
                    'gallery':gallery,
                    'signature':signature,
                    'comments':comments

                }
                return schedule_data
            else:
                return schedule_data

        except:
            pass   
    def get_vehicle(self, instance):
        try:
            vehicle_data ={}
            if Schedule.objects.filter(job=instance).exists():
                existing_schedule = Schedule.objects.get(job=instance)
                try:
                    gallery = []
                    for image in existing_schedule.gallery.all()[:3]:
                        gallery.append({'id':image.id,  'file':image.file.url})
                
                except:
                    pass  
                existing_schedule = Schedule.objects.get(job=instance)
                vehicle_data = {
                    'id':existing_schedule.vehicle.id,
                    'engine_numbers':existing_schedule.vehicle.engine_numbers,
                    'image1':existing_schedule.vehicle.image1.url,
                    'due_rego':existing_schedule.vehicle.due_rego,
                    'fuel':existing_schedule.vehicle.fuel,
                    'width':existing_schedule.vehicle.width,
                    'length':existing_schedule.vehicle.length,
                    'transmission':existing_schedule.vehicle.transmission,
                    'year':existing_schedule.vehicle.year,
                    'types':existing_schedule.vehicle.types,
                    'registration':existing_schedule.vehicle.registration,
                    'previous_rego':existing_schedule.vehicle.previous_rego,
                    
                }
                return vehicle_data
            else:
                return vehicle_data

        except:
            pass
     

    
    # def get_vehicle(self, instance):
    #     try:
    #         return instance.vehicle.registration
    #     except:
    #         pass    
    # def get_comments(self, instance):
    #     try:
    #         comments = []
    #         employee = self.context.get('member',None)
    #         employee_obj = Employee.objects.get(id=employee)
    #         for comment in instance.comments.all():
    #             print(comment.employee)
    #             if comment.employee == employee_obj:
    #                 comments.append({'id':comment.id,'comment':comment.comment,'created_by':comment.employee.name,'author':True})
                    
    #             else:
    #                 print(comment)
    #                 comments.append({'id':comment.id,'comment':comment.comment,'created_by':comment.employee.name,'author':False})
    #         return comments
    #     except:
    #         pass        

    class Meta:
        model= Job
        exclude = ['edited_date_time']    
        # extra_fields =['comments']   

class AdditionalVehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalVehicles
        fields =['id','schedule']

class AdditionalVehicleGetSerializer(serializers.ModelSerializer):
    additional_vehicles = serializers.SerializerMethodField()

    def get_additional_vehicles(self, instance):
        additional_vehicle = []
        each_vehicle = instance.vehicles.get_queryset()
        for i in each_vehicle:
            try:
                additional_vehicle.append({
                    
                        'id': i.id,
                        'vehicle_type':i.vehicle_type,
                        'active_status':i.active_status,
                        'previous_rego':i.previous_rego,

                        'registration':i.registration,
                        'types':i.types,
                        'year':i.year,
                        'transmission':i.transmission,
                        'fuel':i.fuel,
                        'height':i.height,
                        'width':i.width,
                        'length':i.length,
                        'litres':i.litres,
                        'vin_number':i.vin_number,
                        'axies':i.axies,
                        'engine_numbers':i.engine_numbers,
                        'due_rego':i.due_rego,
                        'action':i.action,
                        'image1':i.image1.url
      
                    })
            
            except:
                pass 
       
        return additional_vehicle    
    class Meta:
        model = AdditionalVehicles
        extra_fields = ['additional_vehicles']
        exclude =['edited_date_time','vehicles','id','created_date_time','schedule']
