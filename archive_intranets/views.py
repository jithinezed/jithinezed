import os
import datetime
from django.shortcuts import render, HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework import status

from .models import (
    IntranetArchiveFiles,
    IntranetArchiveFolders,
    Inner_IntranetArchiveFiles,
    InnerFolder,
    Inside_Inner_IntranetArchiveFiles,
    Inside_InnerFolder
)
from accounts.models import Client,Employee

from .models import (
    IntranetFolders,
    IntranetSubFolders,
    IntranetFolderFiles,
    IntranetSubFolders2,
    IntranetSubFolderFiles,
    IntranetSubFolder2Files,
    IntranetBarAttachments

)

from .serializer import (
    InsideInnerIntranetSerializer,
    InsideInnerIntranetGetSerializer,
    InnerIntranetSerializer,
    InnerIntranetGetSerializer,
    IntranetGetSerializer,
    IntranetSerializer,
)

from drive.models import DriveFolder,Files
from django.db.models import Avg, Max, Min, Sum

#sales-intranet
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sales_archive(request,show_on):
    folders = DriveFolder.objects.all()
    data = []
    if show_on == 'sales_tab':
        try:
            for folder in folders:
                exist = IntranetArchiveFiles.objects.filter( intranet_archive_folder=folder)
                if folder.sales_tab == True and exist:
                    in_dict = {'id':folder.id,'folder_name':folder.name, 'files': IntranetArchiveFiles.objects.filter(intranet_archive_folder=folder).values('id', 'file_item','file_name')}
                    data.append(in_dict)
                    
            return Response(data)
        except Exception as E:
            return Response({'Error': str(E), 'app_data':'Something went wrong while fetching files'}, status=status.HTTP_400_BAD_REQUEST)

    if show_on == 'generate_qoute':
        try:
            for folder in folders:
                exist = IntranetArchiveFiles.objects.filter( intranet_archive_folder=folder)
                if folder.generate_qoute == True and exist:
                    in_dict = {'id':folder.id,'folder_name':folder.name, 'files': IntranetArchiveFiles.objects.filter( intranet_archive_folder=folder).values('id', 'file_item','file_name')}
                    data.append(in_dict)
                    
            return Response(data)
        except Exception as E:
            return Response({'Error': str(E), 'app_data':'Something went wrong while fetching files'}, status=status.HTTP_400_BAD_REQUEST)

    if show_on == 'attach_quote':
        try:
            for folder in folders:
                exist = IntranetArchiveFiles.objects.filter(intranet_archive_folder=folder)
                if folder.attach_quote == True and exist:
                    in_dict = {'id':folder.id,'folder_name':folder.name, 'files': IntranetArchiveFiles.objects.filter(intranet_archive_folder=folder).values('id', 'file_item','file_name')}
                    data.append(in_dict)
                    
            return Response(data)
        except Exception as E:
            return Response({'Error': str(E), 'app_data':'Something went wrong while fetching files'}, status=status.HTTP_400_BAD_REQUEST)

   
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def intranet_folderFiles(request,folder_id):
#     if request.method=="GET":
#         try:
#             data =[]
#             folder = IntranetArchiveFolders.objects.get(id=folder_id)
#             in_dict = {'id':folder.id,'folder_name':folder.name, 'files': IntranetArchiveFiles.objects.filter(intranet_archive_folder=folder).values('id', 'file_item','file_name')}
#             data.append(in_dict)

#             return Response(data)
#         except Exception as E:
#             return Response({'Error': str(E), 'app_data':'Something went wrong while fetching folder'}, status=status.HTTP_400_BAD_REQUEST)

                        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_intranet_folders(request):
    if request.method=="GET":
        try:
            app_data =[]
            folders = IntranetArchiveFolders.objects.all()

            for folder in folders:
                    in_dict = {'id':folder.id,'folder_name':folder.name}
                    app_data.append(in_dict)

            return Response(app_data)
        except Exception as E:
            return Response({'Error': str(E), 'app_data':'Something went wrong while fetching folder'}, status=status.HTTP_400_BAD_REQUEST)

# intranet folders and files                       
# Multiple file upload start here



#Intra

@api_view(['POST','GET'])
@permission_classes([IsAuthenticated])
def intranet_folder_list(request,folder_id):
    if request.method == 'POST':
        try:
            serializer = IntranetSerializer(data=request.data)
            if serializer.is_valid():
                new_serializer_object = serializer.save()
                try:
                    request.data._mutable = True
                except:
                    pass
                if 'attachments_list' in request.data:
                    uploaded_files = request.data.pop('attachments_list')   
                    
                    if not uploaded_files == ['']:
                        for attachment in uploaded_files:
                            
                            new_serializer_object.attachments.create(file=attachment)
                        try:
                            request.data._mutable = False
                        except:
                            pass
                         
                        return Response({'Success': 'files uploaded','app_data': 'file uploaded'}, status.HTTP_201_CREATED)   
                    
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'files uploaded  failed'}, status=status.HTTP_400_BAD_REQUEST)

    if request.method =='GET':
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
                for subfolder in DriveFolder.objects.filter(intranet=True,parent_folder=folder_id):
                    subfolder_list.append({'id':subfolder.id,"name":subfolder.name})


                subfolder_data = {
                    'files': file_list,
                    'folders':subfolder_list,
                    }
                folders.append(subfolder_data)  
                return Response({"folders":folders})
        except Exception as E:
            return Response({"app_data": "Something went wrong", "dev_data":str(E)})



@api_view(['GET','DELETE','PATCH'])         
@permission_classes([IsAuthenticated])
def get_intranet_folder_files(request,folder_id=0):
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
                for subfolder in DriveFolder.objects.filter(parent_folder=folder_id,intranet=True):
                    subfolder_list.append({'id':subfolder.id,"name":subfolder.name,"type":"intranet"})


                subfolder_data = {
                    'files': file_list,
                    'folders':subfolder_list,
                    'type':'intranet'
                    }
                folders.append(subfolder_data)  
                return Response({"folders":folders})
        except Exception as E:
            return Response({"app_data": "Something went wrong", "dev_data":str(E)})
 