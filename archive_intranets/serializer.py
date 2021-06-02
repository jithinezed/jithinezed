from rest_framework import serializers
from .models import Inside_Inner_IntranetArchiveFiles,Inner_IntranetArchiveFiles,IntranetArchiveFiles,IntranetBarAttachments
import os

#inside
class InsideInnerIntranetSerializer(serializers.ModelSerializer):
     class Meta:
        model = Inside_Inner_IntranetArchiveFiles
        exclude = ['attachments']
class InsideInnerIntranetGetSerializer(serializers.ModelSerializer):
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
      model= Inside_Inner_IntranetArchiveFiles
      exclude = ['attachments']
      extra_fields = ['attachments_list','id']   

#inner

class InnerIntranetSerializer(serializers.ModelSerializer):
     class Meta:
        model = Inner_IntranetArchiveFiles
        exclude = ['attachments']
class InnerIntranetGetSerializer(serializers.ModelSerializer):
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
      model= Inner_IntranetArchiveFiles
      exclude = ['attachments']
      extra_fields = ['attachments_list','id']   

#intra

class IntranetSerializer(serializers.ModelSerializer):
     class Meta:
        model = IntranetArchiveFiles
        exclude = ['attachments']
class IntranetGetSerializer(serializers.ModelSerializer):
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
      model= IntranetArchiveFiles
      exclude = ['attachments']
      extra_fields = ['attachments_list','id']   
