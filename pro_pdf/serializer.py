
from rest_framework import serializers
from .models import Template,EditedForm


class TemplateGetSerializer(serializers.ModelSerializer):
    class Meta:
        model =Template
        fields = '__all__'


class TemplateGetSerializer(serializers.ModelSerializer):
    class Meta:
        model =Template
        fields = '__all__'

class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model =Template
        fields = ['id','html_content']        
class EditedFormSerializer(serializers.ModelSerializer):
    class Meta:
        model =EditedForm 
        fields= ['id','html_content','form_name']