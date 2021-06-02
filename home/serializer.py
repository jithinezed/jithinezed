from rest_framework import serializers
import datetime
import os
from jobs.models import Job
from schedules.models import Schedule

class JobGetSerializer(serializers.ModelSerializer):
    client_name = serializers.SerializerMethodField()
    code = serializers.SerializerMethodField()
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
        
    class Meta:
        model= Job
        exclude = ['uuid','created_by','client','quote','amount','paid_amount','reoccurring','schedule_status','tab_type','created_date_time','edited_date_time']


class ScheduleGetSerializer(serializers.ModelSerializer):
    client = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    job_type = serializers.SerializerMethodField()
    amount = serializers.SerializerMethodField()
    paid_amount = serializers.SerializerMethodField()
    amount_paid_status = serializers.SerializerMethodField()
    amount_total_paid_status = serializers.SerializerMethodField()
    vehicle = serializers.SerializerMethodField()
    team_employees = serializers.SerializerMethodField()
    shift = serializers.SerializerMethodField()

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

    class Meta:
        model= Schedule
        exclude = ['edited_date_time']