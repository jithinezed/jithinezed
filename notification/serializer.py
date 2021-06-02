from .models import Notification_hub
from rest_framework import serializers
import os

class Notification_hubSerializer(serializers.ModelSerializer):
    class Meta:
        model =Notification_hub
        field =['id','type','model','reference_id']

class NotificationGetSerializer(serializers.ModelSerializer):
    model_type = serializers.SerializerMethodField()
    action_type = serializers.SerializerMethodField()
    reference_id = serializers.SerializerMethodField()
    team_list  = serializers.SerializerMethodField()
    def get_model_type(self, instance):
        try:
            return instance.model_type
        except:
            pass        
    def get_action_type(self, instance):
        try:
            return instance.type
        except:
            pass        
    def get_reference_id(self, instance):
        try:
            return instance.reference_id
        except:
            pass   
    def get_team_list(self,instance):
        team_list =[]
        employee = instance.send_to_team.get_queryset()
        for i in employee:
              
                    team_list.append({
                            'id': i.id,
                            'name': i.name,
                        })
        print(team_list)           
        return team_list
        
        
   
    class Meta:
        model= Notification_hub
        exclude = [ 'edited_date_time','send_to_team']        