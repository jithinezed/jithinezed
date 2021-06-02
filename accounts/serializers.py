from rest_framework import serializers
import datetime
import os
from django.contrib.auth.models import User
from .models import PushNotification

class ProfileGetSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        exclude = ['password']
class PushNotificationSerializer(serializers.ModelSerializer):  
    class Meta:
        model= PushNotification
        exclude = ['keys'] 
        