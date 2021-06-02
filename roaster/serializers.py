from .models import Roaster 
from accounts.models import Employee
from rest_framework import serializers
class RoasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roaster
        fields = ['id','technician','day','scheduled_time','type_of_service',
        'company_name','contact_name','site_adddress','comments_info',
        'end_time','slot','amount']

class RoasterGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roaster
        fields = '__all__'


class RoasterGetReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roaster
        fields = [ 'id','day','slot']