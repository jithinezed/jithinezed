import os
import datetime
from pathlib import Path
from django.shortcuts import render, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from django.db.models import Q
from rest_framework import status
from django.conf import settings
from drive.models import DriveFolder
from drive.models import Files
from drive.serializers import DriveFolderSerializer

# Create your views here.
@api_view(['GET','DELETE','PATCH'])         
@permission_classes([IsAuthenticated])
def folder_segment_list(request,folder_id=0):
    if request.method == "GET":
        try:
            folders =[]
            for folder in DriveFolder.objects.filter(id =folder_id):
                
                file_list = []  
                for files in Files.objects.filter(folder=folder):
                    file_data= {
                        'id': files.id,
                        'name': os.path.basename(files.file.url),
                        'url': files.file.url
                    }
                    file_list.append(file_data)
                subfolder_list =[]    
                for subfolder in DriveFolder.objects.filter(parent_folder=folder_id,accounts_files=True):
                    subfolder_list.append({'id':subfolder.id,"name":subfolder.name,"type":"accounts"})


                subfolder_data = {
                    'files': file_list,
                    'folders':subfolder_list,
                    'type':"accounts"
                    }
                folders.append(subfolder_data)  
                return Response({"folders":folders})
        except Exception as E:
            return Response({"app_data": "Something went wrong", "dev_data":str(E)})
@api_view(['POST'])         
@permission_classes([IsAuthenticated])
def accounts_folder_update(request):
    if(request.method =='POST'):
        try:
            try:
                request.POST._mutable = True
            except:
                pass
            request.POST['accounts_files'] = True
            serializer = DriveFolderSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                try:
                    request.POST._mutable = False
                except:
                    pass
                return Response({"folders":"added"})
            else:
                return Response({'Error':serializer.errors,'app_data': 'folder creation failed'}, status=status.HTTP_400_BAD_REQUEST)    
            
        except Exception as E:
            return Response({"app_data": "Something went wrong", "dev_data":str(E)})               
