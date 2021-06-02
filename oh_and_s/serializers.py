from rest_framework import serializers
import datetime
import os
from .models import Notification,News,SafetyData
from archive_intranets.models import(
    IntranetFolders,
    IntranetFolderFiles,
    IntranetSubFolders,
    IntranetSubFolderFiles,
    IntranetSubFolders2,
    IntranetSubFolder2Files,


) 
from accounts.models import Employee

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        exclude =['members']

     
class NotificationGetSerializer(serializers.ModelSerializer):

    members_list = serializers.SerializerMethodField()
    user_read_status = serializers.SerializerMethodField()
    edit_status = serializers.SerializerMethodField()
    dp = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField()

    # Use this method for the custom field
    def get_user_read_status(self,instance):
        member = self.context.get('member',None)
        each_members = instance.members.get_queryset()
        for user in each_members:
            
            if (user.member_id.id ==member):
              
                read_status = user.read_status
                return read_status
    def get_user_id(self,instance):
        member = self.context.get('member',None)
        return member           


    def get_members_list(self, instance):
        members_list =[]
        each_members = instance.members.get_queryset()
        for i in each_members:
            try:
     
                members_list.append({
                   
                        'id': i.id,
                        'name': i.member_id.name,
                        'related':'job completed',
                        'read_status':i.read_status,
                        'dp':i.member_id.dp.url
                    
                    })
            
            except:
                pass

        return members_list
    def get_edit_status(self,instance):
        member = self.context.get('member',None)
        employee = Employee.objects.get(id=member)
        if instance.created_by  ==employee:

            return  True
        else:
            return False
    def get_dp(self,instance):
        member = self.context.get('member',None)
        employee = Employee.objects.get(id=member)
        file_dp =employee.dp.url
        return  file_dp      
        
    def get_created_by(self,instance):
        if instance.created_by != None:
            employee = instance.created_by.name
            created_by =str(employee)
            return  created_by
        else:
            return "Not assigned"    
             
   
    class Meta:
      model= Notification
      exclude = ['members']
      extra_fields = ['members_list']     

#News


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        exclude =['news_member']

     
class NewsGetSerializer(serializers.ModelSerializer):
    members_list = serializers.SerializerMethodField()
    user_read_status = serializers.SerializerMethodField()
    edit_status =  serializers.SerializerMethodField()
    dp =  serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField()

    def get_user_read_status(self,instance):
            member = self.context.get('member',None)
            each_members = instance.news_member.get_queryset()
            for user in each_members:
                
                if (user.member_id.id ==member):
                
                    read_status = user.read_status
                    return read_status
    
    def get_members_list(self, instance):
            members_list =[]
            each_members = instance.news_member.get_queryset()
            for i in each_members:
                try:
                    members_list.append({
                    
                            'id': i.id,
                            'name': i.member_id.name,
                            'related':'job completed',
                            'read_status':i.read_status,
                            'dp':i.member_id.dp.url
                        
                        })
                
                except:
                    pass

            return members_list
    def get_edit_status(self,instance):
        member = self.context.get('member',None)
        employee = Employee.objects.get(id=member)
        if instance.created_by  ==employee:

            return  True
        else:
            return False
    def get_dp(self,instance):
        member = self.context.get('member',None)
        employee = Employee.objects.get(id=member)
        file_dp =employee.dp.url
        return  file_dp
       
    def get_created_by(self,instance):
        if instance.created_by != None:
            employee = instance.created_by.name
            created_by =str(employee)
            return  created_by
        else:
            return "Not assigned"    
   

    class Meta:
      model= News
      exclude = ['news_member'  ]
      extra_fields = ['members_list']   


# folders ohs

class IntranetFoldersSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntranetFolders
        fields =['id','name','sales_tab','generate_quote','attach_quote','intranet','parent_folder']
class IntranetFoldersGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntranetFolders
        fields ='__all__'    

class IntranetFolderFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntranetFolderFiles
        fields =['id','folder','attachment'] 

class IntranetSubFoldersSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntranetSubFolders
        fields =['id','name','folder']
class IntranetSubFoldersGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntranetSubFolders
        fields ='__all__'    

class IntranetSubFolderFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntranetSubFolderFiles
        fields =['id','folder','attachment'] 

class IntranetSub1FoldersSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntranetSubFolders2
        fields =['id','name','folder']
class IntranetSub1FoldersGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntranetSubFolders2
        fields ='__all__'    

class IntranetSub1FolderFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntranetSubFolder2Files
        fields =['id','folder','attachment']


class SafetyDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SafetyData
        fields =['id']

class SafetyDataGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = SafetyData
        fields ='__all__'      