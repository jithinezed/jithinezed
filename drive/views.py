from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers

from django.db.models import Avg, Max, Min, Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework import status


from django.http import JsonResponse
from django.conf import settings
from .models import (
DriveFolder,
Files)
from .serializers import DriveFolderSerializer,DriveFolderGetSerializer,FilesGetSerializer
from accounts.models import Employee,Client
from vehicles.models import Vehicle
from django.db.models import Q

import os

@api_view(['GET'])         
@permission_classes([IsAuthenticated])
def drive(request):
    if(request.method =='GET'):

        try:
            folders = []
            for folder in Level1Folders.objects.filter():

                files_list = []
                for files in Level1FolderFile.objects.filter(name=folder):
                    file_data= {
                        'id': files.id,
                        'name': os.path.basename(files.file.url),
                        'url': files.file.url
                    }
                    files_list.append(file_data)

                sub_folders_list = []
                for subfolder in Level2SubFolders.objects.filter(folder=folder):
                    
                    subfolderfile_list = []
                    for subfolderfile in Level2SubFolderFile.objects.filter(name=subfolder):
                        subfolderfile_data = {
                            'id': subfolderfile.id,
                            'name': os.path.basename(subfolderfile.file.url),
                            'url': subfolderfile.file.url
                        }
                        subfolderfile_list.append(subfolderfile_data)  
                    subfolders2_list =[]
                    for subfolder2 in Level3SubFolders.objects.filter(folder=subfolder):
                        
                        subfolder2_files_list = []
                        for subfolder2_file in Level3SubFolderFile.objects.filter(name=subfolder2):
                            subfolder2_files_content = {
                                'id': subfolder2_file.id,
                                'name': os.path.basename(subfolder2_file.file.url),
                                'url': subfolder2_file.file.url
                            }
                            subfolder2_files_list.append(subfolder2_files_content)
                        subfolders3_list =[]
                        for subfolder3 in Level4SubFolders.objects.filter(folder=subfolder2):
                            
                            subfolder3_files_list = []
                            for subfolder3_file in Level4SubFolderFile.objects.filter(name=subfolder3):
                                subfolder3_files_content = {
                                    'id': subfolder3_file.id,
                                    'name': os.path.basename(subfolder3_file.file.url),
                                    'url': subfolder3_file.file.url
                                }
                                subfolder3_files_list.append(subfolder3_files_content)
                            subfolder3_data = {
                            'id': subfolder3.id,
                            'name': subfolder3.name,
                            'files': subfolder3_files_list
                            }
                            subfolders3_list.append(subfolder3_data)
    
            

                        subfolder2_data = {
                            'id': subfolder2.id,
                            'name': subfolder2.name,
                            'files': subfolders3_list
                        }
                        subfolders2_list.append(subfolder2_data)

                    sub_folder_data = {
                        'id': subfolder.id,
                        'name': subfolder.name,
                        'files': subfolderfile_list,
                        'sub_folders': subfolders2_list
                    }
                    sub_folders_list.append(sub_folder_data)

                folderdata = {
                    'id': folder.id,
                    'name':folder.name,
                    'files': files_list,
                    'sub_folders': sub_folders_list
                }
                folders.append(folderdata)

            return JsonResponse({"folders":folders})


        except Exception as E:
            return HttpResponse({"app_data": "Something went wrong", "dev_data":str(E)})
@api_view(['POST'])         
@permission_classes([IsAuthenticated])
def folder_drive(request):
    if(request.method =='POST'):
        try:
            
            serializer = DriveFolderSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({"folders":"added"})
            else:
                return Response({'Error':serializer.errors,'app_data': 'Pre-inspection check adding failed'}, status=status.HTTP_400_BAD_REQUEST)     

            
            
        except Exception as E:
            return HttpResponse({"app_data": "Something went wrong", "dev_data":str(E)})
            
@api_view(['GET','POST','PUT'])         
@permission_classes([IsAuthenticated])
def file_drive(request,file_id =0):
    if(request.method =='POST'):
     
            folder_obj = DriveFolder.objects.get(id=request.POST['folder'])
            try:
                request.data._mutable = True
            except:
                 pass
            uploaded_file = request.data.pop('file')
           
            for single_file in uploaded_file:
                name =os.path.basename(str(single_file))
                
                split_name = name.split(".", 1)
                re_name = split_name[0]
                obj = Files.objects.create(file =single_file,folder=folder_obj,name=re_name)
            try:
                request.data._mutable = False                                           
            except:
                 pass    
            return JsonResponse({"file":"added"})
    if(request.method =='PUT'):
            try:

                file_obj = Files.objects.get(id = file_id)
                file_obj.name = request.POST['name']
                file_obj.save()
                
                return Response({"file":"Renamed"})        
            except Exception as E:
                return Response({"app_data": "Something went wrong", "dev_data":str(E)},status=status.HTTP_400_BAD_REQUEST)    
                
    if(request.method =='GET'):
           
            item=DriveFolder.objects.all().aggregate(Max('parent_folder'))
            all_values = item.values()
            max_value = max(all_values)
            
            
            folders = []
            for folder in DriveFolder.objects.filter(parent_folder = 0):
                

                files_list = []
                for files in Files.objects.filter(folder=folder):
                    file_data= {
                        'id': files.id,
                        'name': os.path.basename(files.file.url),
                        'url': files.file.url
                    }
                    files_list.append(file_data)
                #     files_list
                subfolders3_list =[]
                for i in range(1,int(max_value)):
                    
                    
                    for subfolder in DriveFolder.objects.filter(parent_folder=i):
                        
                        subfolder_files_list = []
                        for subfolderfile in Files.objects.filter(folder=subfolder):
                            subfolderfile_data = {
                                'id': subfolderfile.id,
                                'name': os.path.basename(subfolderfile.file.url),
                                'url': subfolderfile.file.url
                            }
                            subfolder_files_list.append(subfolderfile_data)
                        s_subfolder_list = []
                        for s_subfolder in DriveFolder.objects.filter(parent_folder=i+1):
                            print("s______")
                            s_subfolder_files_list = []
                            for s_subfolderfile in Files.objects.filter(folder=s_subfolder):
                                s_subfolderfile_data = {
                                    'id': s_subfolderfile.id,
                                    'name': os.path.basename(s_subfolderfile.file.url),
                                    'url': s_subfolderfile.file.url
                                }
                                s_subfolder_files_list.append(s_subfolderfile_data)
                            print(s_subfolder.name)
                            s_subfolder_data = {
                            'id': s_subfolder.id,
                            'name': s_subfolder.name,
                            'files': s_subfolder_files_list,
                            }
                            s_subfolder_list.append(s_subfolder_data)       

                        subfolder_data = {
                            'id': subfolder.id,
                            'name': subfolder.name,
                            'files': subfolder_files_list,
                            'folders': s_subfolder_list
                            }
                        subfolders3_list.append(subfolder_data)  
                
                folderdata = {
                'id': folder.id,
                'name':folder.name,
                'files': files_list,
                'folders': subfolders3_list
                }
                folders.append(folderdata)  
                print("last line")
                    

            return JsonResponse({"folders":folders})
@api_view(['DELETE'])         
@permission_classes([IsAuthenticated])
def folder_delete(request,id):
    if(request.method =='DELETE'):
        try:
            
            obj = DriveFolder.objects.get(id=id)
            if obj.type =="team-individual":
                 return Response({"app_data":"You have no permission to delete this folder",'dev_data':'team-individual folder'},status=status.HTTP_400_BAD_REQUEST)


            if obj.accessibility ==False:
                return Response({"app_data":"You have no permission to delete this folder",'dev_data':'important folder'},status=status.HTTP_400_BAD_REQUEST)
            obj.delete()
        

            return JsonResponse({"folders":"deleted"})
            
        except Exception as E:
            return HttpResponse({"app_data": "Something went wrong", "dev_data":str(E)})  
@api_view(['DELETE'])         
@permission_classes([IsAuthenticated])
def file_delete(request,file_id,folder_id):
    if(request.method =='DELETE'):
        try:
            folder = DriveFolder.objects.get(id=folder_id)
            obj = Files.objects.get(id=file_id,folder=folder)
            if obj.accessibility ==False:
                return Response({"app_data":"You have no permission to delete this folder",'dev_data':'important folder'},status=status.HTTP_400_BAD_REQUEST)
            obj.delete()
            

            return Response({"app_data":"file deleted","dev_data":"file deleted"})
            
        except Exception as E:
            return HttpResponse({"app_data": "Something went wrong", "dev_data":str(E)},status=status.HTTP_400_BAD_REQUEST)                    

@api_view(['PUT'])         
@permission_classes([IsAuthenticated])
def folder_rename(request,folder_id):
    if(request.method =='PUT'):
        try:
           
            folder = DriveFolder.objects.get(id=folder_id)
            folder.name =request.data['name']
            folder.save()


            return Response({"app_data":"folder renamed","dev_data":"folder renamed"})
            
        except Exception as E:
            return Response({"app_data": "Something went wrong", "dev_data":str(E)})

@api_view(['GET'])         
@permission_classes([IsAuthenticated])
def get_root_folder(request):
    if(request.method =='GET'):
        try:
            root_folder =DriveFolder.objects.get(parent_folder=0)
            return Response({"id":root_folder.id,"folder_name":root_folder.name})

        except Exception as E:
            return Response ({"Error":str(E),"app_data":"something went wrong"},status=status.HTTP_400_BAD_REQUEST)    

@api_view(['GET','POST'])         
@permission_classes([IsAuthenticated])
def create_file_in_team_member(request):
    
    
    if(request.method =='POST'):
            try:
                folder_obj = DriveFolder.objects.get(id=request.POST['folder'])
            except:
                return Response ({'app_data':'No folder exists','dev_data':'something went wrong'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                request.data._mutable = True
            except:
                pass   
            employee = Employee.objects.get(id=request.POST['employee'] )
            uploaded_file = request.data.pop('file')
            for single_file in uploaded_file:
                name =os.path.basename(str(single_file))
                
                split_name = name.split(".", 1)
                re_name = split_name[0]
                obj = Files.objects.create(file =single_file,folder=folder_obj,created_by=employee,name=re_name)
            try:
                request.data._mutable = False
            except:
                pass    
            return JsonResponse({"file":"added"})  
#file adding for site         
@api_view(['GET','POST'])         
@permission_classes([IsAuthenticated])
def create_file_in_site_member(request):
    if(request.method =='POST'):
            try:
                folder_obj = DriveFolder.objects.get(id=request.POST['folder'])
            except:
                return Response ({'app_data':'No folder exists','dev_data':'something went wrong'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                request.data._mutable = True
            except:
                pass   
            site = Client.objects.get(id=request.POST['site'] )
            uploaded_file = request.data.pop('file')
            for single_file in uploaded_file:
                name =os.path.basename(str(single_file))
                
                split_name = name.split(".", 1)
                re_name = split_name[0]
                obj = Files.objects.create(file =single_file,folder=folder_obj,created_site=site,name=re_name)
            try:
                request.data._mutable = False
            except:
                pass    
            return JsonResponse({"file":"added"})                    

#team indivudual folder
@api_view(['POST'])         
@permission_classes([IsAuthenticated])
def team_individual_folder(request):
    if(request.method =='POST'):
        user = request.user
        employee_obj = Employee.objects.get(user=user)
        # try:
        #     parent_folder = DriveFolder.objects.get(name="Private Folders")
        # except:
        #     parent_folder = DriveFolder.objects.create(name="Private Folders",type="team-individual-private",parent_folder=1)

        try:
            request.data._mutable = True
        except:
            pass
         
        request.data.update({"type": "team-individual"})
        try:
            request.data._mutable = False
        except:
            pass
        try:
            serializer = DriveFolderSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"folders":"added"})
            else:
                return Response({'Error':serializer.errors,'app_data': 'folder creating failed'}, status=status.HTTP_400_BAD_REQUEST)   
        except Exception as E:
            return Response({'Error': str(E), 'app_data':'Something went wrong while fetching files'}, status=status.HTTP_400_BAD_REQUEST)  

@api_view(['POST'])         
@permission_classes([IsAuthenticated])
def team_folder(request):
    if(request.method =='POST'):
        user = request.user
       
        # try:
        #     parent_folder = DriveFolder.objects.get(name="Private Folders")
        # except:
        #     parent_folder = DriveFolder.objects.create(name="Private Folders",type="team-individual-private",parent_folder=1)

        try:
            request.data._mutable = True
        except:
            pass
        # request.data.update({"parent_folder":parent_folder.id})  
        request.data.update({"type": "team-individual-private"})
        
        try:
            request.data._mutable = False
        except:
            pass
        try:
            serializer = DriveFolderSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"folders":"added"})
            else:
                return Response({'Error':serializer.errors,'app_data': 'folder creating failed'}, status=status.HTTP_400_BAD_REQUEST)   
        except Exception as E:
            return Response({'Error': str(E), 'app_data':'Something went wrong while fetching files'}, status=status.HTTP_400_BAD_REQUEST)  


@api_view(['POST'])         
@permission_classes([IsAuthenticated])
def private_site_folder(request):
    if(request.method =='POST'):
        

        try:
            request.data._mutable = True
        except:
            pass
       
        request.data.update({"type": "site-individual-private"})
        
        try:
            request.data._mutable = False
        except:
            pass
        try:
            serializer = DriveFolderSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"folders":"added"})
            else:
                return Response({'Error':serializer.errors,'app_data': 'folder creating failed'}, status=status.HTTP_400_BAD_REQUEST)   
        except Exception as E:
            return Response({'Error': str(E), 'app_data':'Something went wrong while fetching files'}, status=status.HTTP_400_BAD_REQUEST) 

                                                                                                                                 


@api_view(['POST','GET'])         
@permission_classes([IsAuthenticated])
def vehicle_folder(request,vehicle_type="",vehicle_id = 0,folder_id=0,tab_type="waste"):
    if(request.method =='POST'):
        user = request.user
        employee_obj = Employee.objects.get(user=user)
        # try:
        #     parent_folder = DriveFolder.objects.get(name="Private Folders")
        # except:
        #     parent_folder = DriveFolder.objects.create(name="Private Folders",type="vehicle-individual-private",parent_folder=1)
        try:
            request.data._mutable = True
        except:
            pass
        # request.data.update({"parent_folder":parent_folder.id})  
        request.data.update({"type": "vehicle-individual-private"})
        request.data.update({"employee": employee_obj.id})
        request.data.update({"vehicle": True})
        # request.data.update({"vehicle_type": vehicle_type})
        try:
            request.data._mutable = False
        except:
            pass
        try:
            serializer = DriveFolderSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"folders":"added"})
            else:
                return Response({'Error':serializer.errors,'app_data': 'folder creating failed'}, status=status.HTTP_400_BAD_REQUEST)   
        except Exception as E:
            return Response({'Error': str(E), 'app_data':'Something went wrong while fetching files'}, status=status.HTTP_400_BAD_REQUEST)  
    if request.method == "GET":
        try:
            vehicle = Vehicle.objects.get(id=vehicle_id)
            
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
                for subfolder in DriveFolder.objects.filter(vehicle_id = vehicle,parent_folder=folder_id,vehicle_type=vehicle_type).order_by('name'):
                    subfolder_list.append({'id':subfolder.id,"name":subfolder.name,'type':vehicle_type})
                subfolder_data = {
                    'type':folder.type,
                    'files': file_list,
                    'folders':subfolder_list,
                      'type':vehicle_type
                    }
                folders.append(subfolder_data)  
                return Response({"folders":folders})
        except Exception as E:
            return Response({"app_data": "Something went wrong", "dev_data":str(E)})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def search_folder_files(request,type):
    if request.method == 'POST':
        try:
            key = request.POST['key']
            folder = request.POST['folder_id']
            related_folders = DriveFolder.objects.filter(parent_folder=folder)
            
            if type =="folder": 
                search_type =  request.POST['search_type']
                if search_type =="team-individual":
                    if key =="":
                        folder_found=DriveFolder.objects.filter(parent_folder = folder,type="team-individual")
                    else:
                        folder_found=DriveFolder.objects.filter(Q(parent_folder = folder,name__istartswith=key,type="team-individual") | Q( parent_folder = folder,type="team-individual",employee__name__istartswith=key)  ) 
                    serializer = DriveFolderGetSerializer(folder_found,many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                if search_type =="team-individual-private":
                    employee = Employee.objects.get(id=request.POST['employee'])
                    if key =="":
                        folder_general =DriveFolder.objects.filter(type='team-individual',parent_folder = folder)
                        emp_folder_private = DriveFolder.objects.filter(type='team-individual-private',employee=employee)
                        folder_obj  = folder_general | emp_folder_private
                        folder_found=folder_obj
                    else:
                        folder_general =DriveFolder.objects.filter(type='team-individual',parent_folder = folder)
                        emp_folder_private = DriveFolder.objects.filter(type='team-individual-private',employee=employee)
                        folder_obj  = folder_general | emp_folder_private
                        folder_found=folder_obj.filter(name__istartswith=key)    

                    serializer = DriveFolderGetSerializer(folder_found,many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                if search_type =="general":
                    if key =="":
                        folder_found=DriveFolder.objects.filter(type="general")
                    else:
                        folder_found=DriveFolder.objects.filter(name__istartswith=key,type="general")    
                    serializer = DriveFolderGetSerializer(folder_found,many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)   
                if search_type =="car":
                    vehicle = request.POST['vehicle_id']

                    if key =="":
                        
                        folder_found=DriveFolder.objects.filter(parent_folder = folder,vehicle_id= vehicle,vehicle_type="car")
                    else:
                        folder_found=DriveFolder.objects.filter(parent_folder = folder,name__istartswith=key,type="vehicle-individual-private",vehicle_id=vehicle,vehicle_type="car")    
                    serializer = DriveFolderGetSerializer(folder_found,many=True)  
                    return Response(serializer.data, status=status.HTTP_200_OK)
                if search_type =="truck":
                    vehicle = request.POST['vehicle_id']

                    if key =="":
                        
                        folder_found=DriveFolder.objects.filter(parent_folder = folder,vehicle_id= vehicle,vehicle_type="truck")
                    else:
                        folder_found=DriveFolder.objects.filter(parent_folder = folder,name__istartswith=key,type="vehicle-individual-private",vehicle_id=vehicle,vehicle_type="truck")    
                    serializer = DriveFolderGetSerializer(folder_found,many=True)  
                    return Response(serializer.data, status=status.HTTP_200_OK)  
                if search_type =="fork-lift":
                    vehicle = request.POST['vehicle_id']

                    if key =="":
                        
                        folder_found=DriveFolder.objects.filter(parent_folder = folder,vehicle_id= vehicle,vehicle_type="fork-lift")
                    else:
                        folder_found=DriveFolder.objects.filter(parent_folder = folder,name__istartswith=key,type="vehicle-individual-private",vehicle_id=vehicle,vehicle_type="fork-lift")    
                    serializer = DriveFolderGetSerializer(folder_found,many=True)  
                    return Response(serializer.data, status=status.HTTP_200_OK)         
                if search_type =="accounts":
                    # vehicle = request.POST['vehicle_id']

                    if key =="":
                        
                        folder_found=DriveFolder.objects.filter(parent_folder = folder,accounts_files=True)
                    else:
                        folder_found=DriveFolder.objects.filter(parent_folder = folder,name__istartswith=key,accounts_files=True)    
                    serializer = DriveFolderGetSerializer(folder_found,many=True)  
                    return Response(serializer.data, status=status.HTTP_200_OK)    
                if search_type =="intranet":
                    # vehicle = request.POST['vehicle_id']

                    if key =="":
                        
                        folder_found=DriveFolder.objects.filter(parent_folder = folder,intranet=True)
                    else:
                        folder_found=DriveFolder.objects.filter(parent_folder = folder,name__istartswith=key,intranet=True)    
                    serializer = DriveFolderGetSerializer(folder_found,many=True)  
                    return Response(serializer.data, status=status.HTTP_200_OK)  
                if search_type =="description_of_waste":
                    # vehicle = request.POST['vehicle_id']

                    if key =="":
                        
                        folder_found=DriveFolder.objects.filter(parent_folder = folder,description_of_waste=True)
                    else:
                        folder_found=DriveFolder.objects.filter(parent_folder = folder,name__istartswith=key,description_of_waste=True)    
                    serializer = DriveFolderGetSerializer(folder_found,many=True)  
                    return Response(serializer.data, status=status.HTTP_200_OK)   
                if search_type =="marketing":
                    # vehicle = request.POST['vehicle_id']

                    if key =="":
                        
                        folder_found=DriveFolder.objects.filter(parent_folder = folder,marketing=True)
                    else:
                        folder_found=DriveFolder.objects.filter(parent_folder = folder,name__istartswith=key,marketing=True)    
                    serializer = DriveFolderGetSerializer(folder_found,many=True)  
                    return Response(serializer.data, status=status.HTTP_200_OK)
                if search_type =="power_point":
                    # vehicle = request.POST['vehicle_id']

                    if key =="":
                        
                        folder_found=DriveFolder.objects.filter(parent_folder = folder,power_point=True)
                    else:
                        folder_found=DriveFolder.objects.filter(parent_folder = folder,name__istartswith=key,power_point=True)    
                    serializer = DriveFolderGetSerializer(folder_found,many=True)  
                    return Response(serializer.data, status=status.HTTP_200_OK)  
                if search_type =="pricing":
                    # vehicle = request.POST['vehicle_id']

                    if key =="":
                        
                        folder_found=DriveFolder.objects.filter(parent_folder = folder,pricing=True)
                    else:
                        folder_found=DriveFolder.objects.filter(parent_folder = folder,name__istartswith=key,pricing=True)    
                    serializer = DriveFolderGetSerializer(folder_found,many=True)  
                    return Response(serializer.data, status=status.HTTP_200_OK)    
                if search_type =="tender":
                    # vehicle = request.POST['vehicle_id']

                    if key =="":
                        
                        folder_found=DriveFolder.objects.filter(parent_folder = folder,tender=True)
                    else:
                        folder_found=DriveFolder.objects.filter(parent_folder = folder,name__istartswith=key,tender=True)    
                    serializer = DriveFolderGetSerializer(folder_found,many=True)  
                    return Response(serializer.data, status=status.HTTP_200_OK)                               
            if type =="file":
                p_folder = request.POST['folder_id']
                search_type =  request.POST['search_type']
                folders =[]
                if key =="":
                    for folder in DriveFolder.objects.filter(id =p_folder):
                        try:
                            for files in Files.objects.filter(folder=folder):
                                try:
                                    file_crteated_by = files.created_by.name
                                except:
                                    file_crteated_by = files.name
                                file_data= {
                                    'id': files.id,
                                    'name':files.name,
                                    'url': files.file.url,
                                    "team_member":file_crteated_by
                                }
                                file_list.append(file_data)
                        except:
                            print("eroor")
                            pass        
                        subfolder_list =[]
                        if search_type =="car":
                            vehicle = Vehicle.objects.get(id =request.POST['vehicle_id'])

                            for subfolder in DriveFolder.objects.filter(vehicle_type ="car",parent_folder=p_folder,vehicle_id=vehicle):
                                subfolder_list.append({'id':subfolder.id,"name":subfolder.name,'type':"car"})
                            types = "car"    
                        if search_type =="fork-lift":
                            vehicle = Vehicle.objects.get(id =request.POST['vehicle_id'])

                            for subfolder in DriveFolder.objects.filter(vehicle_type ="fork-lift",parent_folder=p_folder,vehicle_id=vehicle):
                                subfolder_list.append({'id':subfolder.id,"name":subfolder.name,'type':"fork-lift"})
                            types = "fork-lift"
                        if search_type =="truck":
                            vehicle = Vehicle.objects.get(id =request.POST['vehicle_id'])

                            for subfolder in DriveFolder.objects.filter(vehicle_type ="truck",parent_folder=p_folder,vehicle_id=vehicle):
                                subfolder_list.append({'id':subfolder.id,"name":subfolder.name,'type':"truck"})
                            types = "truck"            
                        if search_type =="team-individual-private":
                            private = DriveFolder.objects.filter(type='team-individual-private',parent_folder=p_folder)
                            individual = DriveFolder.objects.filter(type='team-individual',parent_folder=p_folder)
                            sub = private | individual
                            for subfolder in sub:
                                subfolder_list.append({'id':subfolder.id,"name":subfolder.name})
                            types ="team-individual-private"      
                        if search_type =="team-individual":

                            for subfolder in DriveFolder.objects.filter(type='team-individual',parent_folder=p_folder):
                                subfolder_list.append({'id':subfolder.id,"name":subfolder.name,"type": "team-individual"})        
                            types ="team-individual" 
                        if search_type =="general":
                            private = DriveFolder.objects.filter(type='general',parent_folder=p_folder)
                            individual = DriveFolder.objects.filter(type='team-individual',parent_folder=p_folder)
                            sub = private | individual     
                            for subfolder in sub:
                                subfolder_list.append({'id':subfolder.id,"name":subfolder.name})
                            types ="general"      
                        if search_type =="accounts":
                            private = DriveFolder.objects.filter(accounts_files=True,parent_folder=p_folder)
                           
                            for subfolder in private:
                                subfolder_list.append({'id':subfolder.id,"name":subfolder.name,"type":"accounts"})
                            types ="accounts"
                        if search_type =="intranet":
                            private = DriveFolder.objects.filter(intranet=True,parent_folder=p_folder)
                          
                            for subfolder in private:
                                subfolder_list.append({'id':subfolder.id,"name":subfolder.name,"type":"intranet"})
                            types ="intranet"     
                        if search_type =="marketing":
                            private = DriveFolder.objects.filter(marketing=True,parent_folder=p_folder)
                           
                            for subfolder in private:
                                subfolder_list.append({'id':subfolder.id,"name":subfolder.name,"type":"marketing"})
                            types ="marketing"
                        if search_type =="tinder":
                            private = DriveFolder.objects.filter(tinder=True,parent_folder=p_folder)
                             
                            for subfolder in private:
                                subfolder_list.append({'id':subfolder.id,"name":subfolder.name,"type" :"tinder"})
                            types ="tinder"
                        if search_type =="pricing":
                            private = DriveFolder.objects.filter(pricing=True,parent_folder=p_folder)
                              
                            for subfolder in private:
                                subfolder_list.append({'id':subfolder.id,"name":subfolder.name,"type" :"pricing"})
                            types ="pricing"  
                        if search_type =="power_point":
                            private = DriveFolder.objects.filter(power_point=True,parent_folder=p_folder)
                           
                            for subfolder in private:
                                subfolder_list.append({'id':subfolder.id,"name":subfolder.name,"type" :"power_point"})
                            types ="power_point" 
                        if search_type =="description_of_waste":
                            private = DriveFolder.objects.filter(description_of_waste=True,parent_folder=p_folder)
                              
                            for subfolder in private:
                                subfolder_list.append({'id':subfolder.id,"name":subfolder.name,"type" :"description_of_waste"})
                            types ="description_of_waste"     
                                     

                        subfolder_data = {
                        
                            'files': file_list,
                            'folders':subfolder_list,
                            'type':types
    
                            }
                        folders.append(subfolder_data)  
                        return Response({"folders":folders})

                        folder_obj = DriveFolder.objects.get(id=request.POST['folder_id'])
                        if key =="":
                            file_found=Files.objects.filter(folder=folder_obj)
                        else:
                            file_found=Files.objects.filter(name__istartswith=key,folder=folder_obj)
                        serializer = FilesGetSerializer(file_found,many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)   
                else:
                    for folder in DriveFolder.objects.filter(id =request.POST['folder_id']):
                        print(folder)
                        file_list = []  
                        for files in Files.objects.filter(Q(folder=folder,name__istartswith=key) | Q(folder=folder,created_by__name__istartswith=key)):
                            try:
                                file_crteated_by = files.created_by.name
                            except:
                                file_crteated_by = files.name
                            file_data= {
                                'id': files.id,
                                'name':files.name,
                                'url': files.file.url,
                                "team_member":file_crteated_by
                            }
                            file_list.append(file_data)
                        subfolder_list =[]
                        if search_type =="vehicle":
                            vehicle = Vehicle.objects.get(id =request.POST['vehicle_id'])

                            for subfolder in DriveFolder.objects.filter(type='vehicle-individual-private',parent_folder=p_folder,name__istartswith=key,vehicle_id=vehicle):
                                subfolder_list.append({'id':subfolder.id,"name":subfolder.name})
                            types = "vehicle-individual-private"    
                        if search_type =="team-individual-private":
                            private = DriveFolder.objects.filter(type='team-individual-private',parent_folder=p_folder,name__istartswith=key)
                            individual = DriveFolder.objects.filter(type='team-individual',parent_folder=p_folder,name__istartswith=key)
                            sub = private | individual
                            for subfolder in sub:
                                subfolder_list.append({'id':subfolder.id,"name":subfolder.name})
                            types ="team-individual-private"      
                        if search_type =="team-individual":

                            for subfolder in DriveFolder.objects.filter(type='team-individual',parent_folder=p_folder,name__istartswith=key):
                                subfolder_list.append({'id':subfolder.id,"name":subfolder.name})        
                            types ="team-individual" 
                        if search_type =="general":
                            private = DriveFolder.objects.filter(type='general',parent_folder=p_folder,name__istartswith=key)
                            individual = DriveFolder.objects.filter(type='team-individual',parent_folder=p_folder,name__istartswith=key)
                            sub = private | individual     
                            for subfolder in sub:
                                subfolder_list.append({'id':subfolder.id,"name":subfolder.name})
                            types ="general"   
                        if search_type =="accounts":
                            private = DriveFolder.objects.filter(accounts_files=True,parent_folder=p_folder,name__istartswith=key) 
                            for subfolder in private:
                                subfolder_list.append({'id':subfolder.id,"name":subfolder.name,"type":"accounts"})
                            types ="accounts"
                        if search_type =="intranet":
                            private = DriveFolder.objects.filter(intranet=True,parent_folder=p_folder,name__istartswith=key)
                         
                            for subfolder in private:
                                subfolder_list.append({'id':subfolder.id,"name":subfolder.name})
                            types ="intranet"  
                        if search_type =="marketing":
                            private = DriveFolder.objects.filter(marketing=True,parent_folder=p_folder,name__istartswith=key)
                          
                            for subfolder in private:
                                subfolder_list.append({'id':subfolder.id,"name":subfolder.name,"type":"marketing"})
                            types ="marketing"
                        if search_type =="tinder":
                            private = DriveFolder.objects.filter(tinder=True,parent_folder=p_folder,name__istartswith=key)
                         
                            for subfolder in private:
                                subfolder_list.append({'id':subfolder.id,"name":subfolder.name,"type" :"tinder"})
                            types ="tinder"
                        if search_type =="pricing":
                            private = DriveFolder.objects.filter(pricing=True,parent_folder=p_folder,name__istartswith=key)
                          
                            for subfolder in private:
                                subfolder_list.append({'id':subfolder.id,"name":subfolder.name,"type" :"pricing"})
                            types ="pricing"  
                        if search_type =="power_point":
                            private = DriveFolder.objects.filter(power_point=True,parent_folder=p_folder,name__istartswith=key)
                            
                            for subfolder in private:
                                subfolder_list.append({'id':subfolder.id,"name":subfolder.name,"type" :"power_point"})
                            types ="power_point" 
                        if search_type =="description_of_waste":
                            private = DriveFolder.objects.filter(description_of_waste=True,parent_folder=p_folder,name__istartswith=key)
                           
                            for subfolder in private:
                                subfolder_list.append({'id':subfolder.id,"name":subfolder.name,"type" :"description_of_waste"})
                            types ="description_of_waste" 
                        if search_type =="car":
                            private = DriveFolder.objects.filter(vehicle_type="car",parent_folder=p_folder,name__istartswith=key)
                           
                            for subfolder in private:
                                subfolder_list.append({'id':subfolder.id,"name":subfolder.name,"type" :"car"})
                            types ="car"      
                        if search_type =="car":
                            private = DriveFolder.objects.filter(vehicle_type="car",parent_folder=p_folder,name__istartswith=key)
                           
                            for subfolder in private:
                                subfolder_list.append({'id':subfolder.id,"name":subfolder.name,"type" :"car"})
                            types ="car"                


                        subfolder_data = {
                        
                            'files': file_list,
                            'folders':subfolder_list,
                            'type':types
                            }
                        folders.append(subfolder_data)  
                        return Response({"folders":folders})

                        folder_obj = DriveFolder.objects.get(id=request.POST['folder_id'])
                        if key =="":
                            file_found=Files.objects.filter(folder=folder_obj)
                        else:
                            file_found=Files.objects.filter(name__istartswith=key,folder=folder_obj)
                        serializer = FilesGetSerializer(file_found,many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK) 

        except Exception as E:
            return Response({"ERROR": str(E),'dev_data':"something went wrong"}, status=status.HTTP_400_BAD_REQUEST)    



@api_view(['POST','GET'])
@permission_classes([IsAuthenticated])
def get_team_master_folders(request,folder_id=0):
   if request.method == "GET":
        try:
            folders =[]
            for folder in DriveFolder.objects.filter(id =folder_id):
                file_list = []  
                for files in Files.objects.filter(folder=folder).order_by('created_by__name','name'):
                    try:
                        file_data= {
                            'id': files.id,
                            'name':files.name,
                            'url': files.file.url,
                            'team_member':files.created_by.name
                        }
                        file_list.append(file_data)
                    except:
                        pass    
                    
                subfolder_list =[]    
                for subfolder in DriveFolder.objects.filter(parent_folder=folder_id,type="team-individual").order_by('name'):
                    subfolder_list.append({'id':subfolder.id,"name":subfolder.name,"type":subfolder.type})
                subfolder_data = {
                    'files': file_list,
                    'folders':subfolder_list,
                    'type':"team-individual"
                    
                    }
                folders.append(subfolder_data)  
                return Response({"folders":folders})
        except Exception as E:
            return Response({"app_data": "Something went wrong", "dev_data":str(E)})                                                                                                                                        


@api_view(['POST','GET'])
@permission_classes([IsAuthenticated])
def get_employee_folders(request,emp_id,folder_id=0):

    employee = Employee.objects.get(id=emp_id)
    if request.method == "GET":
        try:
            folders =[]
            for folder in DriveFolder.objects.filter(id =folder_id):
               
                
                file_list = []  
                for files in Files.objects.filter(folder=folder,created_by = employee).order_by('name'):
                    file_data= {
                        'id': files.id,
                        'name':files.name,
                        'url': files.file.url
                    }
                    file_list.append(file_data)
                subfolder_list =[]    
              
                folder_general =DriveFolder.objects.filter(parent_folder=folder_id,type='team-individual').order_by('name')
                emp_folder_private = DriveFolder.objects.filter(parent_folder=folder_id,type='team-individual-private',employee=employee).order_by('name')
                folder_obj  = folder_general | emp_folder_private
                
               
                for subfolder in folder_obj:
                    subfolder_list.append({'id':subfolder.id,"name":subfolder.name,"type":subfolder.type})


                subfolder_data = {
                    'type':folder.type,
                    'files': file_list,
                    'folders':subfolder_list,
                    'type':"team-individual-private"
                    }
                folders.append(subfolder_data)  
                return Response({"folders":folders})
        except Exception as E:
            return Response({"app_data": "Something went wrong", "dev_data":str(E)})


@api_view(['POST','GET'])
@permission_classes([IsAuthenticated])
def get_site_folders(request,site_id,folder_id=0):
    site = Client.objects.get(id=site_id)
    if request.method == "GET":
        try:
            folders =[]
            for folder in DriveFolder.objects.filter(id =folder_id):
                file_list = []
                for files in Files.objects.filter(folder=folder,created_site=site).order_by('name'):
                    file_data= {
                        'id': files.id,
                        'name':files.name,
                        'url': files.file.url
                    }
                    file_list.append(file_data)
                subfolder_list =[]    
                folder_general =DriveFolder.objects.filter(parent_folder=folder_id,type='site-individual').order_by('name')
                emp_folder_private = DriveFolder.objects.filter(parent_folder=folder_id,type='site-individual-private',site=site).order_by('name')
                folder_obj  = folder_general | emp_folder_private
                
               
                for subfolder in folder_obj:
                    subfolder_list.append({'id':subfolder.id,"name":subfolder.name,"type":subfolder.type})


                subfolder_data = {
                    'type':folder.type,
                    'files': file_list,
                    'folders':subfolder_list,
                    'type':"site-individual-private"
                    }
                folders.append(subfolder_data)  
                return Response({"folders":folders})
        except Exception as E:
            return Response({"app_data": "Something went wrong", "dev_data":str(E)})



#site indivudual folder
@api_view(['POST'])         
@permission_classes([IsAuthenticated])
def site_individual_folder(request):
    if(request.method =='POST'):
        # try:
        #     parent_folder = DriveFolder.objects.get(name="Private Folders")
        # except:
        #     parent_folder = DriveFolder.objects.create(name="Private Folders",type="team-individual-private",parent_folder=1)

        try:
            request.data._mutable = True
        except:
            pass
         
        request.data.update({"type": "site-individual"})
        try:
            request.data._mutable = False
        except:
            pass
        try:
            serializer = DriveFolderSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"folders":"added"})
            else:
                return Response({'Error':serializer.errors,'app_data': 'folder creating failed'}, status=status.HTTP_400_BAD_REQUEST)   
        except Exception as E:
            return Response({'Error': str(E), 'app_data':'Something went wrong while fetching files'}, status=status.HTTP_400_BAD_REQUEST)  

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def site_search_folder_files(request,type):
    if request.method == 'POST':
        try:
            key = request.POST['key']
            folder = request.POST['folder_id']

            related_folders = DriveFolder.objects.filter(parent_folder=folder)
            
            if type =="folder": 
                search_type =  request.POST['search_type']
                if search_type =="site-individual":
                    if key =="":
                        folder_found=DriveFolder.objects.filter(parent_folder = folder,type="site-individual").order_by('name')
                    else:
                        folder_found=DriveFolder.objects.filter(parent_folder = folder,name__istartswith=key,type="site-individual")
                    serializer = DriveFolderGetSerializer(folder_found,many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                if search_type =="site-individual-private":
                    site = Client.objects.get(id=request.POST['site'])
                    if key =="":
                        folder_general =DriveFolder.objects.filter(type='site-individual',parent_folder = folder).order_by('name')
                        emp_folder_private = DriveFolder.objects.filter(type='site-individual-private',site=site)
                        folder_obj  = folder_general | emp_folder_private
                        folder_found=folder_obj
                    else:
                        folder_general =DriveFolder.objects.filter(type='site-individual',parent_folder = folder)
                        emp_folder_private = DriveFolder.objects.filter(type='site-individual-private',site=site)
                        folder_obj  = folder_general | emp_folder_private
                        folder_found=folder_obj.filter(name__istartswith=key)    

                    serializer = DriveFolderGetSerializer(folder_found,many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)

            if type =="file":
                p_folder = request.POST['folder_id']
                search_type =  request.POST['search_type']
                site = request.POST['site']
                folders =[]
                if key =="":
                    for folder in DriveFolder.objects.filter(id =p_folder):
                        file_list = []  
                        for files in Files.objects.filter(folder=folder).order_by('name'):
                            file_data= {
                                'id': files.id,
                                'name':files.name,
                                'url': files.file.url
                            }
                            file_list.append(file_data)
                        subfolder_list =[]
                        
                        if search_type =="site-individual":

                            for subfolder in DriveFolder.objects.filter(type='site-individual',parent_folder=p_folder).order_by('name'):
                                subfolder_list.append({'id':subfolder.id,"name":subfolder.name})        
                            types ="site-individual" 
                        
                        if search_type =="site-individual-private":
                            private = DriveFolder.objects.filter(type ="site-individual-private",parent_folder=p_folder,site=site).order_by('name')
                              
                            for subfolder in private:
                                subfolder_list.append({'id':subfolder.id,"name":subfolder.name,"type" :"site-individual-private"})
                            types ="site-individual-private"            

                        subfolder_data = {
                        
                            'files': file_list,
                            'folders':subfolder_list,
                            'type':types
                            }
                        folders.append(subfolder_data)  
                        return Response({"folders":folders})

                        folder_obj = DriveFolder.objects.get(id=request.POST['folder_id'])
                        if key =="":
                            file_found=Files.objects.filter(folder=folder_obj,created_site=site).order_by('name')
                        else:
                            file_found=Files.objects.filter(name__istartswith=key,folder=folder_obj,created_site=site)
                        serializer = FilesGetSerializer(file_found,many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)   
                else:
                    for folder in DriveFolder.objects.filter(id =request.POST['folder_id']):
                        file_list = []  
                        for files in Files.objects.filter(folder=folder,name__istartswith=key):
                            file_data= {
                                'id': files.id,
                                'name':files.name,
                                'url': files.file.url
                            }
                            file_list.append(file_data)
                        subfolder_list =[]
                        
                        if search_type =="site-individual-private":
                            private = DriveFolder.objects.filter(type='site-individual-private',parent_folder=p_folder,name__istartswith=key,site=site)
                            individual = DriveFolder.objects.filter(type='site-individual',parent_folder=p_folder,name__istartswith=key)
                            sub = private | individual
                            for subfolder in sub:
                                subfolder_list.append({'id':subfolder.id,"name":subfolder.name})
                            types ="site-individual-private"      
                        if search_type =="site-individual":

                            for subfolder in DriveFolder.objects.filter(type='site-individual',parent_folder=p_folder,name__istartswith=key):
                                subfolder_list.append({'id':subfolder.id,"name":subfolder.name})        
                            types ="site-individual" 
                       
                        
                        
                       
                       


                        subfolder_data = {
                        
                            'files': file_list,
                            'folders':subfolder_list,
                            'type':types
                            }
                        folders.append(subfolder_data)  
                        return Response({"folders":folders})

                        folder_obj = DriveFolder.objects.get(id=request.POST['folder_id'])
                        
                        serializer = FilesGetSerializer(file_found,many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK) 

        except Exception as E:
            return Response({"ERROR": str(E),'dev_data':"something went wrong"}, status=status.HTTP_400_BAD_REQUEST)           
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def drive_multipe_delete(request,type):
    if request.method =="POST":
        request.data._mutable=True
        list_id = request.data.pop('id')
        print(list_id)
        request.data._mutable=False
        if type =="folder":
            for ids in list_id:
                try:
                    folder_obj = DriveFolder.objects.get(id=ids)
                    folder_obj.delete()
                except Exception as E:
                    return Response({"ERROR": str(E),'dev_data':"folder does not exist, please check inputs"}, status=status.HTTP_400_BAD_REQUEST)    
            return Response({"app_data":"successfully deleted all folders","dev_data":"deleted"})
        if type =="file":
            for ids in list_id:
                try:
                    file_obj = Files.objects.get(id=ids)
                    file_obj.delete()
                except Exception as E:
                    return Response({"ERROR": str(E),'dev_data':"file does not exist, please check inputs"}, status=status.HTTP_400_BAD_REQUEST)    
            return Response({"app_data":"successfully deleted all files","dev_data":"deleted"})     
                        