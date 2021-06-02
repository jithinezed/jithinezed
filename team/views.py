import os
import datetime
from django.shortcuts import render, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from django.db.models import Q
from rest_framework import status
from django.contrib.auth.models import User
from .models import EmployeeFile,EmployeeFolder,PostImage,EmployeeImages,SafteyInfo
from accounts.models import Employee,EmployeeCertification
from team_file_archive.models import TeamArchiveFolders, TeamArchiveFiles
from .serializers import( EmployeeSerializer, EmployeeGetSerializer, EmployeeCertificationSerializer,
EmployeeFileGetSerializer,EmployeeFileSerializer,EmployeeFolderSerializer,EmployeeFolderGetSerializer,EmployeeImagesGetSerializer,
EmployeeImagesSerializer,SafteyInfoSerializer,SafteyInfoGetSerializer)
from accounts.models import permissions_choices
from notification.models import Notification_hub
from notification.serializer import NotificationGetSerializer
from accounts.general import push_notifier
from datetime import date
from drive.models import DriveFolder,Files
from drive.serializers import DriveFolderSerializer





@api_view(['GET'])
@permission_classes([IsAuthenticated])
def teamGetAPI(request, id):
    if request.method == 'GET':
        try:  
            data={}
            employee = Employee.objects.get(id=id)          
            serializer = EmployeeGetSerializer(employee,many=False)  

            data.update(serializer.data)  
            try:
                folders = TeamArchiveFolders.objects.all()
                folder_data = []
                for folder in folders:
                    if TeamArchiveFiles.objects.filter(employee=employee, team_archive_folder=folder):
                        in_dict = {'folder_name':folder.name, 'files': TeamArchiveFiles.objects.filter(employee=employee, team_archive_folder=folder).values('id', 'file_item')}
                        folder_data.append(in_dict)
                data.update({'folders': folder_data}) 
            except Exception as E:
               
                return Response({'Error': str(E), 'app_data': 'File operation filed '}, status=status.HTTP_400_BAD_REQUEST) 
            return Response(data)
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'No such a employee found '}, status=status.HTTP_400_BAD_REQUEST)    


@api_view(['POST'])
def teamCreateAPI(request):
    if request.method == 'POST':
        try:
            try:
                emp_id = request.POST['employee_id']
                email = request.POST['email']
                username = request.POST['username']
                password = request.POST['password']    
                
            except Exception as E:
                return Response({'Error': str(E),
                    'app_data': 'Mandatory fields are required'}, status=status.HTTP_400_BAD_REQUEST)    
            if(Employee.objects.filter(employee_id = emp_id).exists() and User.objects.filter(username=username).exists()):

                return Response({'Error': 'Registration failed',
                    'app_data': 'Employee ID or User name already exist'}, status=status.HTTP_400_BAD_REQUEST)   

            else:  
                
                serializer = EmployeeSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                
                    
                try: 
                    if(User.objects.filter(username=username).exists()):
                        employee= Employee.objects.get(id=serializer.data['id'])
                    #  employee.active_status=False
                        employee.delete()
                        return Response({'Error': 'Username is already exist','app_data': 'Username already exist'}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        user = User.objects.create_user(username=username,email=email,password=password)
                        user.save()
                        employee_temp = Employee.objects.get(id=serializer.data['id'])
                        employee_temp.user=user
                        employee_temp.permission_type=serializer.data['user_type']
                        employee_temp.save()
                        employee_id= Employee.objects.get(id=serializer.data['id'])
                        if 'driving_license' in request.data:
                            try:
                                licence =request.FILES['driving_license']
                                expiry_date = request.POST['expiry_date']
                                alert_before =  request.POST['alert_before'] 

                                try:

                                    folder_dr = DriveFolder.objects.get(name = "Drivers License",type='team-individual')
                                except:
                                    folder_dr = DriveFolder.objects.create(name="Drivers License",parent_folder=1,type='team-individual')    

                                try:
                                    name =os.path.basename(str(licence))
                                    split_name = name.split(".", 1)
                                    re_name = split_name[0]
                                except:
                                    re_name ="name?" 

                                obj = Files.objects.create(created_by=employee_id,folder=folder_dr,file=licence,expiry_date=expiry_date,alert_before=alert_before,name=re_name)
                                obj.save()
                                


                            except Exception as E:
                                            return Response({'Error': str(E), 'app_data': 'No such employee found '}, status=status.HTTP_400_BAD_REQUEST)                                       
                        team = Employee.objects.filter(user_type='manager')
                        notification_hub_obj = Notification_hub.objects.create(type='added',model_type='employee',reference_id=employee_id.id)
                        for employee in team:
                            notification_hub_obj.send_to_team.add(employee.id) 
                        return Response({'Success': 'Employee created','app_data': 'Employee Created '}, status.HTTP_201_CREATED)
                except Exception as E:
                    employee= Employee.objects.get(id=serializer.data['id'])
                    #  employee.active_status=False
                    employee.delete()
                    return Response({'Error': str(E),
                    'app_data': 'Employee Registration failed'}, status=status.HTTP_400_BAD_REQUEST)
            
                    
        except Exception as E:
                return Response({'Error': str(E),
                    'app_data': 'Employee Registration failed'}, status=status.HTTP_400_BAD_REQUEST)              

        

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def teamGetAllAPI(request):
    if request.method == 'GET':
        try:  
            employee = Employee.objects.filter(active_status=True)          
            serializer = EmployeeGetSerializer(employee,many=True)                   
            return Response(serializer.data)
        except:
            return Response({'Error': 'No such employee found', 'app_data': 'No such employee found '}, status=status.HTTP_400_BAD_REQUEST)    

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def teamDeleteAPI(request, employee_id):
    if request.method == 'DELETE':
        try:  
            print(employee_id)
            employee = Employee.objects.get(employee_id=employee_id)
            employee.active_status=False
            employee.save()                        
            team = Employee.objects.filter(user_type='manager')
            notification_hub_obj = Notification_hub.objects.create(type='deleted',model_type='employee',reference_id=employee.id)

            for employee in team:
                notification_hub_obj.send_to_team.add(employee.id)                        
            return Response({'Success': 'Employee Deleted', 'app_data': 'Employee was deleted'})
        except:
            return Response({'Error': 'No such employee found', 'app_data': 'No such a employee found '}, status=status.HTTP_400_BAD_REQUEST)    

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def teamEditAPI(request,employee_id):
    if request.method == 'PATCH':
        user =User.objects.get(id=request.user.id)
        logined_emp = Employee.objects.get(user=user)
        try:
            employee = Employee.objects.get(employee_id=int(employee_id))
            if 'password' in request.data:
                if logined_emp.user_type !="manager":
                    return Response({"app_data":"You have no privilege to change password","dev_data":"no Access"},status=status.HTTP_400_BAD_REQUEST)
                if request.POST['password']!='':
                    p= employee.user
                    p.set_password(request.POST['password'])
                    p.save()
                    print(p.password)
            if 'username' in request.data:
                if logined_emp.user_type !="manager":
                    return Response({"app_data":"You have no privilege to change username","dev_data":"no Access"},status=status.HTTP_400_BAD_REQUEST)
                if request.POST['username']!='':

                    u= employee.user
                    if u.username ==request.POST['username']:
                        return Response({"app_data":"username is already taken"},status=status.HTTP_400_BAD_REQUEST)
                    u.username=request.POST['username']
                    u.save()
            if 'expiry_date' in request.data:
                try:
                    folder_dr = DriveFolder.objects.get(name="Drivers License")
                    file_obj = Files.objects.get(created_by=employee,folder=folder_dr)
                    file_obj.expiry_date= request.POST['expiry_date']
                    file_obj.save()
                except Exception as E:
                    return Response({"Error":str(E),'app_data':'update failed'},status=status.HTTP_400_BAD_REQUEST)    
            if 'alert_before' in request.data:
                try:
                    folder_dr = DriveFolder.objects.get(name="Drivers License")
                    file_obj = Files.objects.get(created_by=employee,folder=folder_dr)
                    file_obj.alert_before= request.POST['alert_before']
                    file_obj.save()
                except Exception as E:
                    return Response({"Error":str(E),'app_data':'update failed'},status=status.HTTP_400_BAD_REQUEST)     
        
            if 'driving_license' in request.data:
                try:
                    folder_dr = DriveFolder.objects.get(name="Drivers License")
                    file_obj = Files.objects.get(created_by=employee,folder=folder_dr)
                    license_file= request.FILES['driving_license']
                    file_obj.file = license_file
                    file_obj.save() 
                except Exception as E:
                    return Response({"Error":str(E),'app_data':'update failed'},status=status.HTTP_400_BAD_REQUEST)    
            employee = Employee.objects.get(employee_id=employee_id)          
            serializer = EmployeeSerializer(employee, data=request.data, partial=True)   
            if serializer.is_valid():
                serializer.save()         
                team = Employee.objects.filter(user_type='manager',active_status=True)
                notification_hub_obj = Notification_hub.objects.create(type='edited ',model_type='employee',reference_id=employee.id)
                for employee in team:
                    notification_hub_obj.send_to_team.add(employee.id)  
            employee1 = Employee.objects.get(employee_id=employee_id)        
            serializer1= EmployeeGetSerializer(employee1, many=False)                 
            return Response(serializer1.data)
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'No such a employee found'}, status=status.HTTP_400_BAD_REQUEST)    


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def searchEmployee(request):
    if request.method == 'POST':
        try:
            key = request.POST['key']
            if(key ==' '):
                employee_found=Employee.objects.filter(active_status=True)
                serializer = EmployeeGetSerializer(employee_found,many=True)   
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                employee_found=Employee.objects.filter(Q(employee_id__istartswith=key) | Q(name__istartswith=key)).filter(active_status=True)
                serializer = EmployeeGetSerializer(employee_found,many=True)   
                return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"Fields Required": "key, Employee"}, status=status.HTTP_400_BAD_REQUEST)
            
@api_view(['POST'])
def CreateCertificate(request):
    if request.method == 'POST':
        try:
            employee_id = request.POST['employee_id']
            if Employee.objects.filter(employee_id =employee_id).exists()==False:
                return Response({'Error': 'Invalide Employee id','app_data': 'Enter valid Employee id'}, status=status.HTTP_400_BAD_REQUEST)
            serializer = EmployeeCertificationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                try:                   
                    certificate = EmployeeCertification.objects.get( id=serializer.data['id'])
                    emp = Employee.objects.get(employee_id =employee_id)
                    emp.certifications.add(certificate)
                    emp.save()
                    return Response({'Success': 'Employee Certificate','app_data': 'certificate Created '}, status.HTTP_201_CREATED)
                except:
                    return Response({'Error': 'Error while generating certificate','app_data': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)    
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'Error': 'Error Creating Certificate',
                'app_data': 'Certificate creation failed'}, status=status.HTTP_400_BAD_REQUEST) 


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def employeeIdAvailability(request):
    try: 
        if (Employee.objects.filter(employee_id = request.POST['employee_id']).exists()):
            return Response({'Error': 'employee_id is already exist', 'app_data': 'Employee Id is already exist'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'Success': 'Employee id not exists', 'app_data': 'Valid employee id'})
    except:
        return Response({'Fields Required': 'Employee Id'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def contactAvailability(request):
    try: 
        if (Employee.objects.filter(contact_number = request.POST['contact_number']).exists()):
            return Response({'Error': 'Contact number is already exist', 'app_data': 'Contact number is already exist'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'Success': 'Employee id not exists', 'app_data': 'Valid Contact number'})
    except:
        return Response({'Fields Required': 'Contact number'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def usernameAvailability(request):
    try: 
        if (Employee.objects.filter(name = request.POST['username']).exists()):
            return Response({'Error': 'Username is already exist', 'app_data': 'Username is already exist'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'Success': 'Username not exists', 'app_data': 'Valid Username'})
    except:
        return Response({'Fields Required': 'username'}, status=status.HTTP_400_BAD_REQUEST)  

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def emailAvailability(request):
    try: 
        if (User.objects.filter(email= request.POST['email']).exists()):
            return Response({'Error': 'Email ID is already exist', 'app_data': 'Email ID is already exist'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'Success': 'Email ID not exists', 'app_data': 'Valid Email ID'})
    except:
        return Response({'Fields Required': 'email'}, status=status.HTTP_400_BAD_REQUEST)      



 #_____________________________________________________PROFILE_______________________________________________#

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProfile(request):
    if request.method == 'GET':
        try:  
            employee = Employee.objects.get(user=request.user)
            print(employee)          
            serializer = EmployeeGetSerializer(employee)                   
            return Response(serializer.data)
        except:
            return Response({'Error': 'No such profile found', 'app_data': 'No such profile found '}, status=status.HTTP_400_BAD_REQUEST)    
        
#_______________________-folder-___________________________#

@api_view(['GET','POST','PATCH','DELETE'])
@permission_classes([IsAuthenticated])
def folders(request,emp_id=0):
    # if request.method == 'GET':
      
    #     try:
    #         employee = EmployeeFile.objects.filter(active_status=True)  
    #         print(employee)
    #         serializer = EmployeeFileGetSerializer(employee,many=True)                   
    #         return Response(serializer.data)                         
    #     except:
    #         return Response({'Error': 'No such profile found', 'app_data': 'No such profile found '}, status=status.HTTP_400_BAD_REQUEST) 
    
    if request.method == 'POST':
        try:
            folder_get = request.POST['folder']
            client = Employee.objects.get(id=emp_id)
            try:
                request.data._mutable = True
            except:
                pass
            request.data.update({"employee": client.id})
            try:
                request.data._mutable = False
            except:
                pass
            serializer = EmployeeImagesSerializer(data=request.data)
            if serializer.is_valid():
                new_serializer_object = serializer.save()
                try:
                    request.data._mutable = True
                except:
                    pass
                file_upload_errors = {'error_status': False, 'error': 'No errors', 'dev_data': 'There was no attachments to upload'}
                
                if 'attachments_list' in request.data:
                    try:      
                        uploaded_files = request.data.pop('attachments_list')
                        if not uploaded_files == ['']:
                            get_item=[]
                            for attachment in uploaded_files: 
                            
                                file_upload_errors = {'error_status': False, 'error': 'No errors', 'dev_data': 'Files uploaded'}
                                thiss=new_serializer_object.attachments.create(file=attachment)
                                get_item.append(thiss)

                            try:
                                request.data._mutable = False
                            except:
                                pass

                            attachment_list =[]
                            base = "https://deep.envirowasteadmin.com.au/"
                            for attachment in new_serializer_object.attachments.all():
                               attachment_list.append({'id':attachment.id,'url':base + str(attachment.file.url),'name': os.path.basename(attachment.file.url)})
                                
                            return Response({'Success': 'files uploaded','app_data': attachment_list}, status.HTTP_201_CREATED)  


                    except Exception as E:
                        return Response({'error':str(E) , 'app_data': 'Attachmets files are not saved'})  

                    #to sent recently inserted data as a response    
        except Exception as E:
                   return Response({'error':str(E) , 'app_data': 'Attachmets files are not saved'})
           









    # if request.method == 'PATCH':
    #     try:  
    #         files = EmployeeFile.objects.get(id=file_id)          
    #         serializer = EmployeeFileGetSerializer(files, data=request.data, partial=True)   
    #         if serializer.is_valid():
    #             serializer.save()                
    #         return Response(serializer.data)
    #     except:
    #         return Response({'Error': 'file update failed', 'app_data': 'File update failed'}, status=status.HTTP_400_BAD_REQUEST)               

    # if request.method == 'DELETE':
    #     try:  
    #         print(employee_id)
    #         employee = Employee.objects.get(employee_id=employee_id)
    #         employee.active_status=False
    #         employee.save()                         
    #         return Response({'Success': 'Employee Deleted', 'app_data': 'Employee was deleted'})
    #     except:
    #         return Response({'Error': 'No such employee found', 'app_data': 'No such a employee found '}, status=status.HTTP_400_BAD_REQUEST)    


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getFolder(request,folder_id=0):
    if request.method == 'GET':
        try:
            folder = EmployeeFile.objects.filter(active_status=True,employee_folder=folder_id)  
            serializer = EmployeeFileGetSerializer(folder,many=True)                   
            return Response(serializer.data)                         
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'No such folder found '}, status=status.HTTP_400_BAD_REQUEST) 



@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def getEmp(request,emp_id=0):
    if request.method == 'GET':
        try:
            employee = Employee.objects.get(id=emp_id)  
            folders = EmployeeFolder.objects.all()
            data = []
            for folder in folders:
                obj = EmployeeImages.objects.filter(employee=employee,folder=folder)
                serializer = EmployeeImagesGetSerializer(obj,many=True)  
                in_dict = {'folder_id':folder.id,'folder_name':folder.name, 'files':serializer.data}
                data.append(in_dict)
                
            return Response(data)


        except Exception as E:
            return Response({'Error': str(E), 'app_data':'Something went wrong while fetching files'}, status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def searchEmployeeInFolder(request):
    if request.method == 'POST':
        try:
            key = request.POST['key']
            emp=EmployeeFile.objects.filter(Q(employee__name__istartswith=key) | 
            Q(employee__employee_id__istartswith=key)).filter(active_status=True)
            serializer = EmployeeFileGetSerializer(emp,many=True)  
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"Fields Required": "key, Employee"}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST','GET'])
@permission_classes([IsAuthenticated])
def createFolder(request):
    if request.method == 'POST':
        try:
            
            serializer=EmployeeFolderSerializer(data=request.data)
            if (serializer.is_valid()):
                serializer.save()
            return Response({'Success': 'folder created','app_data': 'folder Created '}, status.HTTP_201_CREATED)
        except:
            return Response({"Error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)            


    if request.method == 'GET':
        try:
            folder = EmployeeFolder.objects.all()  
            serializer = EmployeeFolderGetSerializer(folder,many=True)                
            return Response(serializer.data)                         
        except:
            return Response({'Error': 'Not an active folder', 'app_data': 'folder does not exist'}, status=status.HTTP_400_BAD_REQUEST)    


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_designations(request):
    if request.method == 'GET':     
        desig =[]
        designations =permissions_choices
        for i in designations:
            user_designation=(i[0])
            desig.append({"user_type":user_designation})
        
        return Response({'designations':desig})
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_emp_files(request,file_id):
    if request.method == 'DELETE':   
        try:

            delete_file = PostImage.objects.get(id=file_id)
            delete_file.delete()

            return Response({'Success': 'File Deleted', 'app_data': 'File  deleted'})
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'file  error '}, status=status.HTTP_400_BAD_REQUEST)    

# Notification 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getNotifications(request):
    if request.method == 'GET':
        try:
            user = request.user
            employee_obj = Employee.objects.get(user=user)
            # if (employee_obj.user_type =='manager'):
            notificaion_obj = Notification_hub.objects.all()
            serializer = NotificationGetSerializer(notificaion_obj,many=True)
            return Response(serializer.data)
        except Exception as E:
            return Response ({'Error':str(E),'app_data':"something went wrong"})  
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def team_status(request,team_status):
    if request.method == 'GET':
        try:
            if team_status =="terminated":
                team = Employee.objects.exclude(termination_date__isnull =True).filter(active_status=True)   
                serializer = EmployeeGetSerializer(team,many=True) 
            if team_status =="current":
                team = Employee.objects.filter(termination_date__isnull=True,active_status=True)
                serializer = EmployeeGetSerializer(team,many=True)  

        
            return Response(serializer.data)
           
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'No such a employee found '}, status=status.HTTP_400_BAD_REQUEST)  
@api_view(['GET',"POST","PATCH","DELETE"])
@permission_classes([IsAuthenticated])
def safety_info(request,id=0,employee_id=0):
    employee =Employee.objects.get(id=employee_id)
    if request.method == 'GET':
        try:
            if SafteyInfo.objects.filter(employee=employee_id).exists():
           
                safety_info_obj = SafteyInfo.objects.get(employee=employee_id)
                serializer = SafteyInfoSerializer(safety_info_obj,many=False)
            
                return Response(serializer.data)
            else:
                data = SafteyInfo.objects.create(employee=employee)
                safety_info_obj = SafteyInfo.objects.get(id = data.id)
                serializer = SafteyInfoGetSerializer(safety_info_obj,many=False)
                return Response(serializer.data)




           
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'No such a employee found '}, status=status.HTTP_400_BAD_REQUEST)  
    if request.method == 'POST':
        try:
            serializer = SafteyInfoSerializer(data=request.data)
        
            if serializer.is_valid():
                new_data = serializer.save()
                new_data.employee = employee
                new_data.save()
                return Response(serializer.data)
            else:
                return Response ({"Error":serializer.errors,'app_data':"failed"})    
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'No such a employee found '}, status=status.HTTP_400_BAD_REQUEST)  
    if request.method == 'PATCH':
        try:
            dangerous_obj = SafteyInfo.objects.get(id = id)
                
            serializer = SafteyInfoSerializer(dangerous_obj,data=request.data,partial=True)
        
            if serializer.is_valid():
                new_data = serializer.save()
                new_data.employee = employee
                new_data.save()
                return Response(serializer.data)
            else:
                return Response ({"Error":serializer.errors,'app_data':"failed"})    
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'No such a employee found '}, status=status.HTTP_400_BAD_REQUEST)          
    if request.method == 'PATCH':
        try:
            safety_info_obj = SafteyInfo.objects.get(id=employee_id)
            serializer = SafetyDatesSerializer(safety_info_obj,data=request.data,partail=True)
            if serializer.is_valid():
               serializer.save()
               return Response(serializer.data)  
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'No such a employee found '}, status=status.HTTP_400_BAD_REQUEST)                
      

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def warning_info(request,employee_id=0):
    if request.method == 'GET':
        try:
            try:
                employee= Employee.objects.get(id=employee_id)
                folder = DriveFolder.objects.get(name="Drivers License")


                file_obj = Files.objects.get(created_by=employee,folder=folder)
            except Exception as E:
                return Response({'app_data':'No data found', 'Error':str(E)},status=status.HTTP_400_BAD_REQUEST)    
            
            expiry_date=file_obj.expiry_date
            year =expiry_date.year
            day = expiry_date.day
            month = expiry_date.month
            current_day = datetime.datetime.now().day
            current_month = datetime.datetime.now().month
            current_year = datetime.datetime.now().year
            end_date = datetime. datetime(year,month,day)
            start_date= datetime. datetime(current_year,current_month,current_day)
            # counting months
            num_months = (end_date. year - start_date. year) * 12 + (end_date. month - start_date. month)
           
            
            #counting days
            num_days = end_date - start_date
            days_string =str(num_days)
            days = days_string[:-14]
            alert =[] 
            print(len(days),"djfsjdkf")
            if len(days) == 0:
                alert.append({'alert':"Driving licence expired"})
                return Response({"message":alert})
            if int(days) <=31:
                if int(days)<1:
                    alert.append({'alert':"Driving licence expires today"})
                    return Response({"message":alert})
                alert.append({'alert':"Driving licence expires in " + days_string[:-9]})
                return Response({"message":alert})
            else:
                alert =[]
                alert.append({'alert':"Driving licence expires in " + str(num_months) + " months"})
                return Response({"message":alert}) 
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'No such a employee found '}, status=status.HTTP_400_BAD_REQUEST) 
@api_view(['GET','DELETE','POST','PATCH'])
@permission_classes([IsAuthenticated])
def update_team_folder(request,f_type,f_id=0):
    if request.method == 'DELETE':
        try:
            if f_type =="folder":
                folders = EmployeeFolder.objects.get(id =f_id)
                if folders.accessibility==False:
                    return Response({"app_data":"You have no permission to delete this folder",'dev_data':'important folder'},status=status.HTTP_400_BAD_REQUEST)
                folders.delete()
            if f_type =="file":    
                file_obj = EmployeeFile.objects.get(id=f_id)
                file_obj.delete()
            return Response({"app_data":'deleted','dev_data':'deleted succssefully'})

        except Exception as E:
            return Response({'Error': str(E), 'app_data':'Something went wrong while fetching files'}, status=status.HTTP_400_BAD_REQUEST) 
    if request.method == 'PATCH':
        try:
            if f_type =="folder":
                if folders.accessibility==False:
                    return Response({"app_data":"You have no permission to edit this folder",'dev_data':'important folder'},status=status.HTTP_400_BAD_REQUEST)
                folders = EmployeeFolder.objects.get(id =f_id)
                serializer = EmployeeFolderGetSerializer(folders,data=request.data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
            if f_type =='file':
                file_obj = EmployeeFile.objects.get(id=f_id)
                serializer = EmployeeFileGetSerializer(file_obj,data=request.data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return (serializer.data)
        except Exception as E:
            return Response({'Error': str(E),'app_data':'Something went wrong while fetching files'}, status=status.HTTP_400_BAD_REQUEST)  
    if request.method == 'POST':
        try:
            if f_type =="folder":
                if f_type=="folder":
                    serializer = EmployeeFolderSerializer(data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data)
                    else:
                        return Response({"Error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)    
            else:
                return Response({'dev_data':"invalid folder  key" , 'app_data':'folder  key is invalid'}, status=status.HTTP_400_BAD_REQUEST) 
            if f_type =="file":
                if f_type=="file": 
                    serializer = EmployeeFileSerializer(data=request.data)  
                    if serializer.is_valid():
                        serializer.save()
                        return Response (serializer.data)
                    else:
                        return Response({"Error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'dev_data':"file key invalid " , 'app_data':'file  key is invalid'}, status=status.HTTP_400_BAD_REQUEST)                                                            
        except Exception as E:
            return Response({'Error': str(E), 'app_data':'Something went wrong while fetching files'}, status=status.HTTP_400_BAD_REQUEST)  

                     