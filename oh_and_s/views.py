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
from accounts.models import Employee
from datetime import datetime
from vehicles.general import paginate
from rest_framework.response import Response
from jobs.models import Job
from .serializers import (
NotificationSerializer,NotificationGetSerializer,
NewsGetSerializer,NewsSerializer,

IntranetFoldersSerializer,
IntranetFolderFilesSerializer,
IntranetFoldersGetSerializer,

IntranetSubFoldersGetSerializer,
IntranetSubFoldersSerializer,
IntranetSubFolderFilesSerializer,

IntranetSub1FoldersSerializer,
IntranetSub1FolderFilesSerializer,
IntranetSub1FoldersGetSerializer,
SafetyDataGetSerializer,
SafetyDataSerializer
)
from .models import Notification,News,SafetyData
from  archive_intranets.models import (
    IntranetFolderFiles,
    IntranetFolders,
    IntranetSubFolderFiles,
    IntranetSubFolders,
    IntranetSubFolders2,
    IntranetSubFolder2Files
)
from drive.models import DriveFolder,Files
from django.db.models import Avg, Max, Min, Sum
from django.contrib.auth.models import User

@api_view(['POST','GET','DELETE'])         
@permission_classes([IsAuthenticated])
def notification(request,notification_id=0,page_number=1):
    user = Employee.objects.get(user=request.user)
    if request.method =='POST':
        try:
            try:
                request.data._mutable = True
                request.data['created_by']=user.id
            except:
                pass
            serializer = NotificationSerializer(data=request.data)
            if serializer.is_valid():
                new_serializer_object = serializer.save()
            else:
                return Response({'Error':serializer.errors,'app_data': 'Notification adding failed'}, status=status.HTTP_400_BAD_REQUEST)   
            if 'members' in request.data:
                try:     
                    uploaded_member = request.data.pop('members')
                    if not uploaded_member == ['']:
                        for attachment in uploaded_member:  
                            employee_obj = Employee.objects.get(id=attachment)
                            
                            new_serializer_object.members.create(member_id=employee_obj)
                        try:
                            request.data._mutable = False
                        except:
                            pass
                        
                        obj = Notification.objects.get(id=new_serializer_object.id) 
                        serializer_ = NotificationGetSerializer(obj,context={'member':user.id})   
                        return Response({'Success': 'Notification added','app_data':  serializer_.data}, status.HTTP_201_CREATED)
                except Exception as E:
                        return Response({'Error': str(E), 'app_data': 'Attachments upload was not successful'},status=status.HTTP_400_BAD_REQUEST)
            else:
                employees = Employee.objects.all()
                if not employees == ['']:
                    for employee in employees:  
                        
                        
                        new_serializer_object.members.create(member_id=employee.id)
                    try:
                        request.data._mutable = False
                    except:
                        pass
                    
                    obj = Notification.objects.get(id=new_serializer_object.id) 
                    serializer_ = NotificationGetSerializer(obj,context={'member':user.id},)            
                    return Response({'Success': 'Notification added','app_data': serializer_.data}, status.HTTP_201_CREATED)    

        except Exception as E:
                        return Response({'Error': str(E), 'app_data': 'Attachments upload wass not successful'},status=status.HTTP_400_BAD_REQUEST)

            
        
    if request.method =='GET':
        try:
            limit = request.GET['limit']
            obj = Notification.objects.filter(members__member_id = user)
            serializer = NotificationGetSerializer(obj,many=True,context={'member':user.id})  
            paginate_data = paginate(serializer.data,page_number,int(limit))
            return Response(paginate_data)
        except Exception as E:
            return Response ({'Error':str(E),'app_data': 'No Notification exist'}, status=status.HTTP_400_BAD_REQUEST)          

    if request.method =='DELETE':
        try:
            obj = Notification.objects.get(id=notification_id)
            obj.delete()
            return Response({'Success': 'Notification Deleted', 'app_data': 'Notification deleted'})
        except Exception as E:
            return Response ({'Error':str(E),'app_data': 'No Notification exist'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','DELETE'])         
@permission_classes([IsAuthenticated])
def notification_read_status(request,notification_id):
    if request.method =='GET':
        try:
            user = Employee.objects.get(user=request.user)
            notification = Notification.objects.get(id=notification_id)
            notification_obj = Notification.objects.filter(id = notification_id)[0].members.all()
            for notification_member in notification_obj:
                print(notification_member)
                if(notification_member.member_id == user):
                    if notification_member.read_status ==True:
                        notification_member.read_status =False
                        notification_member.save()
                    else:
                        notification_member.read_status =True
                        notification_member.save()

            return Response ({'Success': 'Notification status changed','app_data': 'Notification status changed'}, status.HTTP_200_OK) 
   
        except Exception as E:
            return Response ({'Error':str(E),'app_data': 'No Notification exist'}, status=status.HTTP_400_BAD_REQUEST)

#News

@api_view(['POST','GET','DELETE','PATCH'])
@permission_classes([IsAuthenticated])
def Team_news(request,news_id=0,page_number=1):
    user = Employee.objects.get(user=request.user)
    if request.method =='POST':
        try:
            request.data._mutable = True
            request.data['created_by']=user.id  
        except:
            pass
        
        try:
            serializer = NewsSerializer(data=request.data)
            if serializer.is_valid():
                new_serializer_object = serializer.save()  
            else:
                return Response({'Error':serializer.errors,'app_data': 'Creating news failed'}, status=status.HTTP_400_BAD_REQUEST)   
            if 'members' in request.data:
                    try:      
                        uploaded_member = request.data.pop('members')
                        if not uploaded_member == ['']:
                            for attachment in uploaded_member:  
                                employee_obj = Employee.objects.get(id=attachment)
                                
                                new_serializer_object.news_member.create(member_id=employee_obj)
                            try:
                                request.data._mutable = False
                            except:
                                pass
                            obj = News.objects.get(id=new_serializer_object.id) 
                            serializer_= NewsGetSerializer(obj,context={'member':user.id})   
                            return Response({'Success': 'News added','app_data': serializer_.data}, status.HTTP_201_CREATED)    

                    except Exception as E:

                        return Response({"Error":str(E),'app_data': 'Somthing went wrong'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                try:
                    uploaded_member = Employee.objects.all()
                    if not uploaded_member == ['']:
                        for attachment in uploaded_member:  
                            employee_obj = Employee.objects.get(id=attachment.id)
                            
                            new_serializer_object.news_member.create(member_id=employee_obj)
                        try:
                            request.data._mutable = False
                        except:
                            pass
                        obj = News.objects.get(id=new_serializer_object.id) 
                        serializer_ = NewsGetSerializer(obj,context={'member':user.id})   
                        return Response({'Success': 'News to all employees','app_data': serializer_.data}, status.HTTP_201_CREATED)    

                except Exception as E:

                    return Response({"Error":str(E),'app_data': 'Somthing went wrong'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                request.data._mutable = False
            except:
                pass
            
        except Exception as E:
            return Response({'Error':str(E), 'app_data': 'Somthing went wrong'}, status=status.HTTP_400_BAD_REQUEST)
    if request.method =='GET':
        try:
       
            limit = request.GET['limit']
            obj = News.objects.filter(news_member__member_id = user)
            serializer = NewsGetSerializer(obj,many=True,context={'member':user.id})  
            paginate_data = paginate(serializer.data,page_number,int(limit))
            return Response(paginate_data)
        except Exception as E:
            return Response ({'Error':str(E),'app_data': 'No News found'}, status=status.HTTP_400_BAD_REQUEST)          

    if request.method =='DELETE':
        try:
            obj = News.objects.get(id=news_id)
            obj.delete()
            return Response({'Success': 'News Deleted', 'app_data': 'News deleted'})
        except Exception as E:
            return Response ({'Error':str(E),'app_data': 'No News found'}, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'PATCH':
        try:  
            news = News.objects.get(id=news_id)
            serializer = NewsGetSerializer(news, data=request.data, partial=True,context={'member':user.id})   
            if serializer.is_valid():
                serializer.save()                
            return Response(serializer.data)            
        except:
            return Response({'Error': 'No News found', 'app_data': 'No news found '}, status=status.HTTP_400_BAD_REQUEST) 


@api_view(['GET','DELETE'])         
@permission_classes([IsAuthenticated])
def news_read_status(request,news_id):
    if request.method =='GET':
        try:
            user = Employee.objects.get(user=request.user)
            news = News.objects.get(id=news_id)
            news_obj = News.objects.filter(id = news_id)[0].news_member.all()
            for news_member in news_obj:
                if(news_member.member_id == user):
                    if news_member.read_status:
                        news_member.read_status =False
                        news_member.save()
                    else:
                        news_member.read_status =True
                        news_member.save()

            return Response ({'Success': 'news status changed','app_data': 'News status changed'}, status.HTTP_200_OK) 
   
        except Exception as E:
            return Response ({'Error':str(E),'app_data': 'No news exist'}, status=status.HTTP_400_BAD_REQUEST)            

#Folders in ohs


@api_view(['POST','GET','DELETE','PATCH'])         
@permission_classes([IsAuthenticated])
def folder_list(request,folder_id=0):
    if request.method == "GET":
        try:
         
           
            folders =[]
            for folder in DriveFolder.objects.filter(parent_folder = 0):
                file_list = []  
                for files in Files.objects.filter(folder=folder):
                    file_data= {
                        'id': files.id,
                        'name': os.path.basename(files.file.url),
                        'url': files.file.url
                    }
                    files_list.append(file_data)
                subfolders3_list =[]    
                for subfolder in DriveFolder.objects.filter(parent_folder=folder.id):      
                    subfolder_files_list = []
                    for subfolderfile in Files.objects.filter(folder=subfolder):
                        subfolderfile_data = {
                            'id': subfolderfile.id,
                            'name': os.path.basename(subfolderfile.file.url),
                            'url': subfolderfile.file.url
                        }
                        subfolder_files_list.append(subfolderfile_data)
                    s_subfolder_list = []
                    for s_subfolder in DriveFolder.objects.filter(parent_folder=subfolder.id):
                        s_subfolder_files_list = []
                        for s_subfolderfile in Files.objects.filter(folder=s_subfolder):
                            s_subfolderfile_data = {
                                'id': s_subfolderfile.id,
                                'name': os.path.basename(s_subfolderfile.file.url),
                                'url': s_subfolderfile.file.url
                            }
                            s_subfolder_files_list.append(s_subfolderfile_data)
                        ss_subfolder_list = []    
                        for ss_subfolder in DriveFolder.objects.filter(parent_folder=s_subfolder.id):
                            ss_subfolder_files_list = []
                            for ss_subfolderfile in Files.objects.filter(folder=ss_subfolder):
                                ss_subfolderfile_data = {
                                    'id': ss_subfolderfile.id,
                                    'name': os.path.basename(ss_subfolderfile.file.url),
                                    'url': ss_subfolderfile.file.url
                                }
                                ss_subfolder_files_list.append(ss_subfolderfile_data)
                            ss_subfolder_data = {
                            'id': ss_subfolder.id,
                            'name':ss_subfolder.name,
                            'files':ss_subfolder_files_list,
                             }
                            ss_subfolder_list.append(ss_subfolder_data)       
                        s_subfolder_data = {
                        'id': s_subfolder.id,
                        'name': s_subfolder.name,
                        'files': s_subfolder_files_list,
                        'folders':ss_subfolder_list
                        }
                        s_subfolder_list.append(s_subfolder_data)       

                    subfolder_data = {
                        'id': subfolder.id,
                        'name': subfolder.name,
                        'files': subfolder_files_list,
                        'folders': s_subfolder_list
                        }
                    subfolders3_list.append(subfolder_data)  
                return Response({"folders":subfolders3_list})
        except Exception as E:
            return Response({"app_data": "Something went wrong", "dev_data":str(E)})

    if request.method == "POST":
        try:
            serializer = IntranetFoldersSerializer(data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                return Response({'Success': 'Folder Created','app_data': 'Folder Created '}, status.HTTP_201_CREATED)

        except Exception as E:
            return Response({"app_data": "Something went wrong", "Error":str(E)})
    if request.method == "DELETE":
        try: 
            
            obj = IntranetFolders.objects.get(id=folder_id)
        
            obj.delete()
            return Response({'Success': 'Folder Deleted', 'app_data': 'Folder deleted'})

        except Exception as E:
            return Response ({'Error':str(E),'app_data': 'No Folder found'}, status=status.HTTP_400_BAD_REQUEST)
    if request.method == "PATCH":
        try:
            folder = IntranetFolders.objects.get(id=folder_id)
            serializer = IntranetFoldersGetSerializer(folder,data=request.data,partial=True)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)   
        except Exception as E:          
            return Response ({'Error':str(E),'app_data': 'No Folder found'}, status=status.HTTP_400_BAD_REQUEST)           
        

@api_view(['POST','GET','DELETE'])         
@permission_classes([IsAuthenticated])

def intranet_files(request,file_id=0):
    if request.method =="POST":
        try:    
            folder = IntranetFolders.objects.get(id=request.POST['folder'])
            uploaded_files = request.data.pop('attachment')   
            for file in uploaded_files:
                intranet_files_obj = IntranetFolderFiles.objects.create(folder=folder,attachment=file)
            return Response({'Success': 'file added','app_data': 'file added '}, status.HTTP_201_CREATED)   
        except Exception as E:
            return Response({"app_data": "Something went wrong", "Error":str(E)})   
    if request.method =="DELETE":    
        try:
            file_obj = IntranetFolderFiles.objects.get(id=file_id)
            file_obj.delete()
            return Response({'Success': 'File Deleted', 'app_data': 'File deleted'})
        except Exception as E:
            return Response ({'Error':str(E),'app_data': 'No file found'}, status=status.HTTP_400_BAD_REQUEST)    


#sub folders and files
@api_view(['POST','DELETE','PATCH'])         
@permission_classes([IsAuthenticated])
def intranet_sub_folder(request,sub_folder_id=0):
    if request.method == "POST":
        try:
            serializer = IntranetSubFoldersSerializer(data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                return Response({'Success': 'Folder Created','app_data': 'Folder Created '}, status.HTTP_201_CREATED)

        except Exception as E:
            return Response({"app_data": "Something went wrong", "Error":str(E)})
    if request.method == "DELETE":
        try: 
            
            obj = IntranetSubFolders.objects.get(id=sub_folder_id)
        
            obj.delete()
            return Response({'Success': 'Folder Deleted', 'app_data': 'Folder deleted'})

        except Exception as E:
            return Response ({'Error':str(E),'app_data': 'No Folder found'}, status=status.HTTP_400_BAD_REQUEST)
    if request.method == "PATCH":
        try:
            folder = IntranetSubFolders.objects.get(id=sub_folder_id)
            serializer = IntranetSubFoldersGetSerializer(folder,data=request.data,partial=True)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)   
        except Exception as E:          
            return Response ({'Error':str(E),'app_data': 'No Folder found'}, status=status.HTTP_400_BAD_REQUEST)   

@api_view(['POST','GET','DELETE'])         
@permission_classes([IsAuthenticated])

def intranet_sub_folder_files(request,file_id=0):
    if request.method =="POST":
        try:    
            folder = IntranetSubFolders.objects.get(id=request.POST['folder'])
            uploaded_files = request.data.pop('attachment')   
            for file in uploaded_files:
                intranet_files_obj = IntranetSubFolderFiles.objects.create(folder=folder,attachment=file)
            return Response({'Success': 'file added','app_data': 'file added '}, status.HTTP_201_CREATED)   
        except Exception as E:
            return Response({"app_data": "Something went wrong", "Error":str(E)})   
    if request.method =="DELETE":    
        try:
            file_obj = IntranetSubFolderFiles.objects.get(id=file_id)
            file_obj.delete()
            return Response({'Success': 'File Deleted', 'app_data': 'File deleted'})
        except Exception as E:
            return Response ({'Error':str(E),'app_data': 'No file found'}, status=status.HTTP_400_BAD_REQUEST)  


#sub1 folders and files
@api_view(['POST','DELETE','PATCH'])         
@permission_classes([IsAuthenticated])
def intranet_sub1_folder(request,sub1_folder_id=0):
    if request.method == "POST":
        try:
            
            serializer = IntranetSub1FoldersSerializer(data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                return Response({'Success': 'Folder Created','app_data': 'Folder Created '}, status.HTTP_201_CREATED)
            else:
                return Response({"app_data": "Something went wrong", "Error":serializer.errors})

        except Exception as E:
            return Response({"app_data": "Something went wrong", "Error":str(E)})
    if request.method == "DELETE":
        try: 
            
            obj = IntranetSubFolders2.objects.get(id=sub1_folder_id)
        
            obj.delete()
            return Response({'Success': 'Folder Deleted', 'app_data': 'Folder deleted'})

        except Exception as E:
            return Response ({'Error':str(E),'app_data': 'No Folder found'}, status=status.HTTP_400_BAD_REQUEST)
    if request.method == "PATCH":
        try:
            folder = IntranetSubFolders2.objects.get(id=sub1_folder_id)
            serializer = IntranetSub1FoldersGetSerializer(folder,data=request.data,partial=True)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)  
            else:
                return  Response(serializer.errors)     
        except Exception as E:          
            return Response ({'Error':str(E),'app_data': 'No Folder found'}, status=status.HTTP_400_BAD_REQUEST)   

@api_view(['POST','GET','DELETE'])         
@permission_classes([IsAuthenticated])

def intranet_sub1_folder_files(request,file_id=0):
    if request.method =="POST":
        try:    
            folder = IntranetSubFolders2.objects.get(id=request.POST['folder'])
            uploaded_files = request.data.pop('attachment')   
            for file in uploaded_files:
                intranet_files_obj = IntranetSubFolder2Files.objects.create(folder=folder,attachment=file)
            return Response({'Success': 'file added','app_data': 'file added '}, status.HTTP_201_CREATED)   
        except Exception as E:
            return Response({"app_data": "Something went wrong", "Error":str(E)})   
    if request.method =="DELETE":    
        try:
            file_obj = IntranetSubFolder2Files.objects.get(id=file_id)
            file_obj.delete()
            return Response({'Success': 'File Deleted', 'app_data': 'File deleted'})
        except Exception as E:
            return Response ({'Error':str(E),'app_data': 'No file found'}, status=status.HTTP_400_BAD_REQUEST)  

@api_view(['GET','DELETE','PATCH'])         
@permission_classes([IsAuthenticated])
def folder_segment_list(request,folder_id=0):
    user = Employee.objects.get(user=request.user)
    if request.method == "GET":
        try:
            folders =[]
            for folder in DriveFolder.objects.filter(id =folder_id):
                
                file_list = []  
                for files in Files.objects.filter(folder=folder).order_by('name'):
                    file_data= {
                        'id': files.id,
                        'name':files.name,
                        'url': files.file.url
                    }
                    file_list.append(file_data)
                subfolder_list =[]
                folder_team_individual =DriveFolder.objects.filter(parent_folder=folder_id,type='team-individual').order_by('name')
                general_folder = DriveFolder.objects.filter(parent_folder=folder_id,type='general').order_by('name')
                folder_obj  =  folder_team_individual | general_folder
                for subfolder in folder_obj:
                    subfolder_list.append({'id':subfolder.id,"name":subfolder.name,'type':subfolder.type})


                subfolder_data = {
                    'type':folder.type,
                    'files': file_list, 
                    'folders':subfolder_list,
                    }
                folders.append(subfolder_data)  
                return Response({"folders":folders})
        except Exception as E:
            return Response({"app_data": "Something went wrong", "dev_data":str(E)})


@api_view(['POST','PATCH',"GET"])         
@permission_classes([IsAuthenticated])
def safety_data(request,safety_data_id=0):
    if request.method == "POST":
        try:
            serializer = SafetyDataSerializer(data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                return Response({'Success': 'Safety Data Created','app_data': 'Safety Data Created '}, status.HTTP_201_CREATED)
            else:
                return  Response(serializer.errors) 
        except Exception as E:
            return Response({"app_data": "Something went wrong", "Error":str(E)})
    if request.method == "PATCH":
        try:
            safety_data = SafetyData.objects.get(id=safety_data_id)
            serializer = SafetyDataGetSerializer(safety_data,data=request.data,partial=True)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)  
            else:
                return  Response(serializer.errors)     
        except Exception as E:          
            return Response ({'Error':str(E),'app_data': 'No Safety data found'}, status=status.HTTP_400_BAD_REQUEST)  
    if request.method == "GET":
        try:
            safety_data = SafetyData.objects.get(id=1)
            serializer = SafetyDataGetSerializer(safety_data,many=False)        
            return Response(serializer.data)  
           
        except Exception as E:          
            return Response ({'Error':str(E),'app_data': 'No Safety data found'}, status=status.HTTP_400_BAD_REQUEST)   
         
