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
from .models import Schedule, Schedule_comment,AdditionalVehicles
from datetime import timedelta
from django.utils import timezone
from .serializer import ScheduleGetSerializer, ScheduleMobileGetSerializer, VehicleSerializer, EmployeeSerializer
from jobs.serializer import JobGetSerializer
from vehicles.models import Vehicle
from accounts.models import Employee
from drive.models import DriveFolder,Files
from .serializer import CommentSerializer,CommentGetSerializer,JobSingleGetSerializer,AdditionalVehicleSerializer,AdditionalVehicleGetSerializer
from django.contrib.auth.models import User
from accounts.general import push_notifier,push_notifier_for_team
from sales_quotes.models import LoggingInfo
@api_view(['GET'])         
@permission_classes([IsAuthenticated])
def schedule_view(request,api_type,page=1):
    if request.method == 'GET':
        user=User.objects.get(id=request.user.id)
        print(user)
        login_employee = Employee.objects.get(user=user)
        if api_type == 'waste':
            try:                     
                all_schedule = Schedule.objects.all()
            except Exception as E:
                return Response({'Error': str(E), 'app_data': 'Schedule fetching failed'}, status=status.HTTP_400_BAD_REQUEST)
        elif api_type == 'all':
            try:                     
                all_schedule = Schedule.objects.all()
            except Exception as E:
                return Response({'Error': str(E), 'app_data': 'Schedule fetching failed'}, status=status.HTTP_400_BAD_REQUEST)
        elif api_type == 'hills':
            try:                     
                all_schedule = Schedule.objects.filter(tab_type='hills')
            except Exception as E:
                return Response({'Error': str(E), 'app_data': 'Schedule fetching failed'}, status=status.HTTP_400_BAD_REQUEST)
        
        elif api_type == 'pumps':
            try:                     
                all_schedule = Schedule.objects.filter(tab_type='pumps')
            except Exception as E:
                return Response({'Error': str(E), 'app_data': 'Schedule fetching failed'}, status=status.HTTP_400_BAD_REQUEST)
        
        elif api_type == 'destruction':
            try:                     
                all_schedule = Schedule.objects.filter(tab_type='destruction')
            except Exception as E:
                return Response({'Error': str(E), 'app_data': 'Schedule fetching failed'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'app_data': 'type should be waste, pumps, hills or destruction'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            page = 1
            limit = 20
            try:
                page = int(request.GET['page'])
                limit = int(request.GET['limit'])
            except:
                pass
            data = []
            scheduling_members = []
            scheduling_vehicles = []
            last_10_days = []
            # for getting last 10 days
            from_number = 0
            to_number = 10
            from_date = timezone.now().date()
            # default 10 days
            try:
                from_date= datetime.strptime(request.GET['from'], '%Y-%m-%d').date()
                to_date = datetime.strptime(request.GET['to'], '%Y-%m-%d').date()
                to_number = abs((from_date - to_date).days) + 1
            except:
                pass

            for i in range(from_number,to_number):
                last_10_days.append(from_date + timedelta(days=i))
                # new change
            
            # for getting all scheduling members - to delete
            for scheduling_members_object in Schedule.objects.all().order_by('job__created_by__id').distinct('job__created_by__id'):
                scheduling_members.append(scheduling_members_object.job.created_by)

            # for getting all scheduling vehicles
            for scheduling_vehicles_object in Schedule.objects.all().order_by('vehicle__id').distinct('vehicle__id'):
                if scheduling_vehicles_object.vehicle == None:
                    pass
                else:
                    scheduling_vehicles.append(scheduling_vehicles_object.vehicle)
            
            for this_day in last_10_days:
                this_day_schedule_members=[]
                for scheduling_vehicle in scheduling_vehicles:
                    this_vehicle_schedule_jobs = []
                    
                   # filtered_schedule_objects = Q(start_date=this_day)
                    # filtered_schedule_objects.add(Q(end_date__lte=this_day), Q.OR)
                    schedule_objects_filter_objects = all_schedule.filter(start_date=this_day)
                    for this_member_schedule_this_date in schedule_objects_filter_objects:
                        # new change

                        if(this_member_schedule_this_date.vehicle == scheduling_vehicle):
                            serializer = ScheduleGetSerializer(this_member_schedule_this_date,context={"member":login_employee.id})
                            this_vehicle_schedule_jobs.append(serializer.data)
                    this_day_schedule_members.append({
                        'id':scheduling_vehicle.id,
                        'registration':scheduling_vehicle.registration,
                        'vehicle_type':scheduling_vehicle.vehicle_type,
                        'registration':scheduling_vehicle.registration,
                        'types':scheduling_vehicle.types,
                        'engine_numbers':scheduling_vehicle.engine_numbers,
                        'job_schedules':this_vehicle_schedule_jobs
                    })
                schedules_with_no_verhicle=[]
                w_serializer = ScheduleGetSerializer(Schedule.objects.filter(start_date=this_day, vehicle=None), many=True)
                print(w_serializer.data)
                schedules_with_no_verhicle.append(w_serializer.data)
                data.append({
                    'date':this_day,
                    'weekday':this_day.strftime("%A"),
                    'vehicles': this_day_schedule_members,
                    'non_vehicles': schedules_with_no_verhicle
                })
            paginated_data = paginate(data, page, limit)
            return Response(paginated_data)
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'Schedule fetching failed'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])         
@permission_classes([IsAuthenticated])
def schedule_view_vehicle(request):
    if request.method == 'GET':
        user=User.objects.get(id=request.user.id)
        print(user)
        login_employee = Employee.objects.get(user=user)
        data = []
        
        try:
            scheduling_vehicles = []
            # for getting all scheduling vehicles
            for scheduling_vehicles_object in Schedule.objects.all().order_by('vehicle__id').distinct('vehicle__id'):
                if scheduling_vehicles_object.vehicle == None:
                    pass
                else:
                    scheduling_vehicles.append(scheduling_vehicles_object.vehicle)

            for scheduling_vehicle in scheduling_vehicles:
                data.append({
                    'id':scheduling_vehicle.id,
                    'registration':scheduling_vehicle.registration,
                    'vehicle_type':scheduling_vehicle.vehicle_type,
                    'registration':scheduling_vehicle.registration,
                    'types':scheduling_vehicle.types,
                    'engine_numbers':scheduling_vehicle.engine_numbers,
                })
                
            return Response(data)
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'Vehicle fetching failed'}, status=status.HTTP_400_BAD_REQUEST)       
        

@api_view(['GET'])         
@permission_classes([IsAuthenticated])
def schedule_view_mobile(request,api_type):
    if request.method == 'GET': 
        user=User.objects.get(id=request.user.id)
        login_employee = Employee.objects.get(user=user)
        if api_type == 'waste':
            try:                     
                all_schedule = Schedule.objects.filter(tab_type='waste')
            except Exception as E:
                return Response({'Error': str(E), 'app_data': 'Schedule fetching failed'}, status=status.HTTP_400_BAD_REQUEST)
        elif api_type == 'all':
            try:                     
                all_schedule = Schedule.objects.all()
            except Exception as E:
                return Response({'Error': str(E), 'app_data': 'Schedule fetching failed'}, status=status.HTTP_400_BAD_REQUEST)
        elif api_type == 'hills':
            try:                     
                all_schedule = Schedule.objects.filter(tab_type='hills')
            except Exception as E:
                return Response({'Error': str(E), 'app_data': 'Schedule fetching failed'}, status=status.HTTP_400_BAD_REQUEST)
        
        elif api_type == 'pumps':
            try:                     
                all_schedule = Schedule.objects.filter(tab_type='pumps')
            except Exception as E:
                return Response({'Error': str(E), 'app_data': 'Schedule fetching failed'}, status=status.HTTP_400_BAD_REQUEST)
        
        elif api_type == 'destruction':
            try:                     
                all_schedule = Schedule.objects.filter(tab_type='destruction')
            except Exception as E:
                return Response({'Error': str(E), 'app_data': 'Schedule fetching failed'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'app_data': 'type should be waste, pumps, hills or destruction'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            page = 1
            limit = 20
            try:
                page = int(request.GET['page'])
                limit = int(request.GET['limit'])
            except:
                pass
            data = []
            scheduling_members = []
            last_10_days = []
            # for getting last 10 days
            from_number = 0
            to_number = 10
            from_date = timezone.now().date()
            # default 10 days
            try:
                from_date= datetime.strptime(request.GET['from'], '%Y-%m-%d').date()
                to_date = datetime.strptime(request.GET['to'], '%Y-%m-%d').date()
                to_number = abs((from_date - to_date).days) + 1
            except:
                pass

            for i in range(from_number,to_number):
                last_10_days.append(from_date - timedelta(days=i))
                        
            for this_day in last_10_days:
                for sc in Schedule.objects.filter(team_employees__in=[login_employee],start_date=this_day):
                    print(sc)
                    serializer = ScheduleMobileGetSerializer(sc,context={"member":login_employee.id})
                    data.append(serializer.data)
            paginated_data = paginate(data, page, limit)
            return Response(paginated_data)
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'Schedule fetching failed'}, status=status.HTTP_400_BAD_REQUEST)
        

        
@api_view(['GET'])         
@permission_classes([IsAuthenticated])
def availability(request):
    if request.method == 'GET': 
        try:
            start = request.GET['start']
            end = request.GET['end']
            vehicles = Vehicle.objects.all()
            team = Employee.objects.all()
            vehicle_serializer = VehicleSerializer(vehicles, many=True,context={'start':start,'end':end})
            team_serializer = EmployeeSerializer(team, many=True,context={'start':start,'end':end})
            data = {
                'vehicle':vehicle_serializer.data,
                'team':team_serializer.data
            }
            return Response(data)
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'Avaialbility fetching failed'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])         
@permission_classes([IsAuthenticated])
def availability_team(request):
    if request.method == 'GET': 
        try:
            start = request.GET['start']
            end = request.GET['end']
            team = Employee.objects.all()
            team_serializer = EmployeeSerializer(team, many=True,context={'start':start,'end':end})
            return Response(team_serializer.data)
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'Avaialbility fetching failed'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])         
@permission_classes([IsAuthenticated])
def availability_vehicle(request):
    if request.method == 'GET': 
        try:
            start = request.GET['start']
            end = request.GET['end']
            vehicles = Vehicle.objects.all()
            vehicle_serializer = VehicleSerializer(vehicles, many=True,context={'start':start,'end':end})
            return Response(vehicle_serializer.data)
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'Avaialbility fetching failed'}, status=status.HTTP_400_BAD_REQUEST)
#Availabity api by jithin 
      
@api_view(['POST', 'DELETE', 'PUT'])         
@permission_classes([IsAuthenticated])
def add_to_schedule(request, js_id=''):
    emp = Employee.objects.get(user=request.user)
    if request.method == 'POST': 
       
        try:
            job = Job.objects.get(id=request.data['id'])
            sc_existing = Schedule.objects.filter(job=job)
            if not sc_existing:
                try:
                    sc = Schedule()
                    sc.tab_type=job.tab_type
                    sc.job=job
                    sc.start_date=datetime.strptime(request.data['start_date'], '%Y-%m-%d').date() 
                    sc.start_time=datetime.strptime(request.data['start_time'], '%H:%M:%S').time() 
                    sc.end_time=datetime.strptime(request.data['end_time'], '%H:%M:%S').time()
                    try:
                        sc.end_date=request.data['end_date']
                    except:
                        pass    
                    sc.status = "pending"
                    sc.save()
                    try:
                        
                        message =str(emp.name) + " Scheduled a job "
                        LoggingInfo.objects.create(message=message,quote=job.quote)
                    except:
                        pass 
                    job.schedule_status=True
                    job.save()
                   
                    try:
                        AdditionalVehicles.objects.create(schedule=sc)
                    except:
                        pass    
                    serializer=ScheduleGetSerializer(sc)
                    return Response(serializer.data)
                except Exception as E:
                    return Response({'dev_data': str(E), 'app_data': 'Schedule adding failed'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'app_data': 'Job already scheduled'}, status=status.HTTP_400_BAD_REQUEST)         
        except Exception as E:
            return Response({'dev_data': str(E), 'app_data': 'Schedule adding failed'}, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        try:
            schdeule = Schedule.objects.get(id=js_id)
            job = schdeule.job
            job.schedule_status=False
            job.save()
            schdeule.delete()
            try:
                        
                message =str(emp.name) + " deleted a Scheduled job "
                LoggingInfo.objects.create(message=message,quote=job.quote)
            except:
                pass 
            try:
                push_notifier("Schedule alert"," scheduled job  deleted")
            except Exception as E:
                print(str(E))
                pass
            return Response({'app_data': "Schedule Deleted Successfully"})
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'Schedule deleting failed'}, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "PUT":
        try:
            sc = Schedule.objects.get(id=request.data['id'])
            sc.status = request.data['status']
            sc.save()
            serializer=ScheduleGetSerializer(sc, data=request.data)
            if serializer.is_valid():
                serializer.save()
                try:  
                    message =str(emp.name) + " Updated the scheduled job "
                    LoggingInfo.objects.create(message=message,quote=sc.job.quote)
                except:
                    pass 
                try:
                    push_notifier("Scheduled status changed",str(emp.name) +  " changed schedule status",'accounts-staff')
                    push_notifier("Scheduled status changed",str(emp.name) +  " changed schedule status",'accounts-manager')
                except Exception as E:
                    print(str(E))
                    pass
            return Response(serializer.data)
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'Schedule editing failed'}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST', 'DELETE'])         
@permission_classes([IsAuthenticated])
def add_team_to_schedule(request):
    emp = Employee.objects.get(user=request.user)
    if request.method == 'POST': 
        try:
            try:
                request.data._mutable = True
            except:
                pass
            team_list = []
            sc = Schedule.objects.get(id=request.data['id'])
            if 'members' in request.data:
                members_to_add = list(map(int, request.data.pop('members')))
                sc.team_employees.clear()
                for member in members_to_add:
                    this_employee = Employee.objects.get(id=member)
                    if this_employee in sc.team_employees.all():
                        pass
                    else:
                        sc.team_employees.add(this_employee)
                        team_list.append(this_employee)
                try:  
                    message =str(emp.name) + " added new members to schedule "
                    LoggingInfo.objects.create(message=message,quote=sc.job.quote)
                except:
                    pass         
                try:
                    request.data._mutable = False
                except:
                    pass
                try:
                    team_list = Employee.objects.filter(user_type = "managers")
                    push_notifier_for_team("job Scheduled",str(emp.name) +  " Scheduled a job",team_list)
                except Exception as E:
                    print(str(E))
                    pass

            else:
                sc.team_employees.clear()

            serializer = ScheduleGetSerializer(sc)
            return Response(serializer.data)

        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'Schedule member adding failed'}, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        try:
            try:
                request.data._mutable = True
            except:
                pass

            sc = Schedule.objects.get(id=request.data['id'])
            members_to_add = list(map(int, request.data.pop('members')))
            print(members_to_add)
            for member in members_to_add:
                this_employee = Employee.objects.get(id=member)
                if this_employee in sc.team_employees.all():
                    sc.team_employees.remove(this_employee)
                else:
                    pass
            try:  
                message =str(emp.name) + " deleted team members from schedule "
                LoggingInfo.objects.create(message=message,quote=sc.job.quote)
            except:
                pass         
            try:
                request.data._mutable = False
            except:
                pass

            serializer = ScheduleGetSerializer(sc)
            return Response(serializer.data)
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'Schedule deleting failed'}, status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST', 'DELETE'])         
@permission_classes([IsAuthenticated])
def add_vehicle_to_schedule(request):
    emp = Employee.objects.get(user=request.user)
    if request.method == 'POST': 
        try:
            sc = Schedule.objects.get(id=request.data['id'])
            vehicle = Vehicle.objects.get(id=request.data['vehicle'])
            sc.vehicle = vehicle
            sc.save()
            serializer = ScheduleGetSerializer(sc)
            try:  
                message =str(emp.name) + " added  to schedule "
                LoggingInfo.objects.create(message=message,quote=sc.job.quote)
            except:
                pass    
            return Response(serializer.data)
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'Schedule vehicle adding failed'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST', 'DELETE'])         
@permission_classes([IsAuthenticated])
def add_images_to_schedule(request,file_id=0):
    user = User.objects.get(id=request.user.id)
    logined_employee = Employee.objects.get(user=user)
    if request.method == 'POST': 
        try:
            try:
                request.data._mutable = True
            except:
                pass

            sc = Schedule.objects.get(id=request.data['id'])
            attach_image =request.FILES.getlist('image')
            job_folder = DriveFolder.objects.get(job_images=True)
            print(job_folder)
            for attach_file in attach_image:
                file_obj =Files.objects.create(folder=job_folder,file=attach_file,created_by=logined_employee)
                sc.gallery.add(file_obj)
            try:
                request.data._mutable = False
            except:
                pass
            try:  
                message =str(logined_employee.name) + " added  images schedule "
                LoggingInfo.objects.create(message=message,quote=sc.job.quote)
            except:
                pass  
            serializer = ScheduleGetSerializer(sc)
            return Response(serializer.data)
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'Schedule images adding failed'}, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == "DELETE": 
        try:
            sc = Schedule.objects.get(id=request.data['id'])
            file_obj = Files.objects.get(id=file_id)
            if file_obj.created_by == logined_employee:
                file_obj.delete()
                try:  
                    message =str(logined_employee.name) + " deleted  images from schedule "
                    LoggingInfo.objects.create(message=message,quote=sc.job.quote)
                except:
                    pass
                serializer = ScheduleGetSerializer(sc)
                return Response({"Success":serializer.data,'app_data':'file deleted'})
            else:
                return Response({"app_data":"created by someone else or none","Error":"You have no privilege to delete this file"},status=status.HTTP_400_BAD_REQUEST)   
        except Exception as E:
            return Response({"Error":str(E),'app_data':"No action performed"})    

@api_view(['POST', 'DELETE'])         
@permission_classes([IsAuthenticated])
def add_signature_to_schedule(request):
    emp = Employee.objects.get(user=request.user)
    from django.core.files.images import ImageFile
    if request.method == 'POST': 
        try:
            try:
                request.data._mutable = True
            except:
                pass
            signature = request.FILES['image']
            sc = Schedule.objects.get(id=request.data['id'])
            sc.image=signature
            sc.save()
            try:  
                message =str(emp.name) + " added  signature to schedule "
                LoggingInfo.objects.create(message=message,quote=sc.job.quote)
            except:
                pass
    
            serializer = ScheduleGetSerializer(sc)
            return Response(serializer.data)
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'Schedule signature adding failed'}, status=status.HTTP_400_BAD_REQUEST)     

@api_view(['GET','POST',"PATCH","DELETE"])         
@permission_classes([IsAuthenticated])
def schedule_commentAPI(request,comment_id=0):
    emp = Employee.objects.get(user=request.user)
    if request.method == 'POST':
        user=User.objects.get(id=request.user.id)
        login_employee = Employee.objects.get(user=user)
        try:
            user =request.user
            employee=Employee.objects.get(user=user)
            try:
                request.data._mutable = True
            except:
                pass
            request.data.update({"employee":employee.id})
            try:
                request.data._mutable = False
            except:
                pass
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                try:

                    comment_obj =serializer.save()
                    schedule =Schedule.objects.get(id=request.POST['schedule_id'])
                    schedule.comments.add(comment_obj)
                    schedule.save()
                    try:  
                        message =str(emp.name) + " added  comments to schedule "
                        LoggingInfo.objects.create(message=message,quote=schedule.job.quote)
                    except:
                        pass
                    data ={"id":comment_obj.id,"author":True,"created_by":login_employee.name,'comment':request.POST['comment']}
                
                    return Response({'Success': 'comment uploaded','comment': data}, status.HTTP_201_CREATED)
                except Exception as E:
                    return Response({'Error': str(E), 'app_data': 'Add valid input '}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as E:
                return Response({'Error': str(E), 'app_data': 'comment adding failed'}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        try:
            user=User.objects.get(id=request.user.id)
            login_employee = Employee.objects.get(user=user)

            comment_obj = Schedule_comment.objects.all()
            serializer = CommentGetSerializer(comment_obj,many=True,context={"member":login_employee.id})
            return Response (serializer.data)  
        except Exception as E:
            return Response ({'Error': str(E), 'app_data': 'comments are not available'}, status=status.HTTP_400_BAD_REQUEST)       
    if request.method == 'PATCH':
        try:

            comment_obj = Schedule_comment.objects.get(id=comment_id)
            serializer = CommentGetSerializer(comment_obj,data=request.data,partial =True)
            if serializer.is_valid():
                serializer.save()          
        
                return Response (serializer.data)  
        except Exception as E:
            return Response ({'Error': str(E), 'app_data': 'comments are not available'}, status=status.HTTP_400_BAD_REQUEST)       
    if request.method == 'DELETE':
        try:
            comment_obj = Schedule_comment.objects.get(id=comment_id)
            comment_obj.delete()
            return Response ({'Success': 'comment deleted','app_data':'comment deleted'})
        except Exception as E:
            return Response ({'Error': str(E), 'app_data': 'comments are not available'}, status=status.HTTP_400_BAD_REQUEST)   


@api_view(['GET'])         
@permission_classes([IsAuthenticated])
def schedule_get_details(request,job_id):   
    if request.method =='GET':
        try:

            user=User.objects.get(id=request.user.id)
            login_employee = Employee.objects.get(user=user)
            
            this_job = Job.objects.get(id=job_id)
           
            serializer = JobSingleGetSerializer(this_job,many=False,context={"member":login_employee.id})
            return Response (serializer.data)
            # else:
            #     this_job = Job.objects.get(id=job_id)
            #     serializer =JobGe   tSerializer(this_job,many=False)
            #     return Response (serializer.data)
        except Exception as E:
            return Response ({'Error': str(E), 'app_data': 'jobs are not available'}, status=status.HTTP_400_BAD_REQUEST) 

#incomplete schedule with paginations.

@api_view(['GET'])         
@permission_classes([IsAuthenticated])
def incomplete_schedule_view(request,api_type,page=1):
    if request.method == 'GET':
        user=User.objects.get(id=request.user.id)
        login_employee = Employee.objects.get(user=user)
        if api_type == 'waste':
            try:                     
                all_schedule = Schedule.objects.filter(tab_type='waste',status='pending')
            except Exception as E:
                return Response({'Error': str(E), 'app_data': 'Schedule fetching failed'}, status=status.HTTP_400_BAD_REQUEST)
        
        elif api_type == 'hills':
            try:                     
                all_schedule = Schedule.objects.filter(tab_type='hills',status='pending')
            except Exception as E:
                return Response({'Error': str(E), 'app_data': 'Schedule fetching failed'}, status=status.HTTP_400_BAD_REQUEST)
        
        elif api_type == 'pumps':
            try:                     
                all_schedule = Schedule.objects.filter(tab_type='pumps',status='pending')
            except Exception as E:
                return Response({'Error': str(E), 'app_data': 'Schedule fetching failed'}, status=status.HTTP_400_BAD_REQUEST)
        
        elif api_type == 'destruction':
            try:                     
                all_schedule = Schedule.objects.filter(tab_type='destruction',status='pending')
            except Exception as E:
                return Response({'Error': str(E), 'app_data': 'Schedule fetching failed'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'app_data': 'type should be waste, pumps, hills or destruction'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            page = 1
            limit = 20
            try:
                page = int(request.GET['page'])
                limit = int(request.GET['limit'])
            except:
                pass          
            data =[]
            for sc in all_schedule:
                print(sc)
                serializer =ScheduleGetSerializer(sc,context={"member":login_employee.id})
                data.append(serializer.data)
            paginated_data = paginate(data, page, limit)
            return Response(paginated_data)
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'Schedule fetching failed'}, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['POST','GET','DELETE'])
@permission_classes([IsAuthenticated])
def additional_vehicles(request,schedule_id=0):
    emp = Employee.objects.get(user=request.user)
    if request.method == 'POST':
        try:
            try:
                schedule_obj = Schedule.objects.get(id=int(schedule_id))
            except:
                return Response({"Error":'No schedule exist in this id','app_data': 'Schedule fetching failed'},status=status.HTTP_400_BAD_REQUEST)        
            additional_vehicle_schedule_obj = AdditionalVehicles.objects.get(schedule=schedule_obj)
            new_vehicle_list = []
            existing_vehicle_list = []
            if 'vehicles' in request.data:

                for i in request.POST.getlist('vehicles'):
                    obj = additional_vehicle_schedule_obj.vehicles.add(Vehicle.objects.get(id=int(i)))
                    additional_vehicle_schedule_obj.save(obj)  
                    new_vehicle_list.append(int(i))
                for vehicle in Vehicle.objects.all():
                    existing_vehicle_list.append(int(vehicle.id))
                result_list = (list(list(set(existing_vehicle_list)-set(new_vehicle_list)) + list(set(new_vehicle_list)-set(existing_vehicle_list))))
                for i in result_list:
                    additional_vehicle_schedule_obj.vehicles.remove(Vehicle.objects.get(id=int(i)))     
                return Response({'Success': 'Additional vehicle added','app_data':"Additional vehicle added"}, status.HTTP_201_CREATED)   
                
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'something went wrong'}, status=status.HTTP_400_BAD_REQUEST)
    if request.method =='GET':
        try:
            vehicles_obj = AdditionalVehicles.objects.filter(schedule=schedule_id)
            serializer = AdditionalVehicleGetSerializer(vehicles_obj,many=True) 
            return Response (serializer.data[0])
        except Exception as E:
            return Response ({'Error': str(E), 'app_data': 'jobs are not available'}, status=status.HTTP_400_BAD_REQUEST)   
    if request.method =='DELETE':
        try:

            vehicle_id = request.GET['vehicle_id']
            print("get vehivcle id",vehicle_id)
            vehicles_obj = AdditionalVehicles.objects.get(schedule=schedule_id)
            for vehicle in vehicles_obj.vehicles.all():
                print(vehicle.id)
                if vehicle.id == int(vehicle_id):
                    print("inside")
                    vehicles_obj.vehicles.remove(vehicle)
                    return Response ({'app_data':'vehicle deleted','dev_data':'vehicle removed from the additional vehicles'})
                
            return Response ({'app_data':'No matches found','dev_data':'No vehicle exist in this vehicle id'}, status=status.HTTP_400_BAD_REQUEST)    
        except Exception as E:
            return Response({"Error":str(E),"dev_data":'something went wrong'},status=status.HTTP_400_BAD_REQUEST)
