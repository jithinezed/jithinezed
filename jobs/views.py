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
from jobs.models import Job,JobCard,JobcardInfo,Services
from sales_quotes.models import Quote
from notification.models import Notification_hub

from .serializer import JobGetSerializer,JobCardGetSerializer,CustomJobCardGetSerializer,CustomJobCardSerializer,QuoteCardGetSerializer
from accounts.models import Client
from clients.serializers import ClientGetSerializer
from schedules.models import Schedule
from sales_quotes.permissions import quote_permissions
from sales_quotes.models import LoggingInfo
from  accounts.general import push_notifier_for_team,push_notifier  
from .serializer import JobCardInfoGetSerializer,JobCardInfoSerializer
import json
from oh_and_s.serializers import NotificationSerializer
from oh_and_s.models import Notification

@api_view(['GET'])         
@permission_classes([IsAuthenticated])
def job_view(request,api_type):
    if request.method == 'GET': 
        page = 1
        limit = 20
        try:
            page = int(request.GET['page'])
            limit = int(request.GET['limit'])
        except:
            pass
        if api_type == 'waste':
            try:                     
                all_jobs = Job.objects.all()
            except Exception as E:
                return Response({'Error': str(E), 'app_data': 'Job fetching failed'}, status=status.HTTP_400_BAD_REQUEST)
        elif api_type == 'all':
            try:                     
                all_jobs = Job.objects.all()
            except Exception as E:
                return Response({'Error': str(E), 'app_data': 'Job fetching failed'}, status=status.HTTP_400_BAD_REQUEST)
        elif api_type == 'hills':
            try:                     
                all_jobs = Job.objects.filter(tab_type='hills')
            except Exception as E:
                return Response({'Error': str(E), 'app_data': 'Job fetching failed'}, status=status.HTTP_400_BAD_REQUEST)
        
        elif api_type == 'pumps':
            try:                     
                all_jobs = Job.objects.filter(tab_type='pumps')
            except Exception as E:
                return Response({'Error': str(E), 'app_data': 'Job fetching failed'}, status=status.HTTP_400_BAD_REQUEST)
        
        elif api_type == 'destruction':
            try:                     
                all_jobs = Job.objects.filter(tab_type='destruction')
            except Exception as E:
                return Response({'Error': str(E), 'app_data': 'Job fetching failed'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'app_data': 'type should be waste, pumps, hills or destruction'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            serializer = JobGetSerializer(all_jobs, many=True)
            paginated_jobs = paginate(serializer.data, page, limit)
            return Response(paginated_jobs)
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'Job fetching failed'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])         
@permission_classes([IsAuthenticated])
def job_edit_api(request):
    if request.method == 'PUT':
        emp = Employee.objects.get(user=request.user)
        this_job = Job.objects.get(id=request.data['id'])
        try:
            this_job.amount = request.data['amount']
        except:
            pass
            
        try:
            this_job.paid_amount= request.data['paid_amount']
        except:
            pass
        this_job.save()
        try:
            
            message =str(emp.name) + " edited a job "
            LoggingInfo.objects.create(message=message,quote=this_job.quote)
        except:
            pass 
        serializer = JobGetSerializer(this_job)
        team = Employee.objects.filter(user_type='manager')
        # try:
        #     push_notifier("Job alert","000" + str(this_job.id) + " updated")
        # except Exception as E:
        #     print(str(E))
        #     pass
        notification_hub_obj = Notification_hub.objects.create(type='edited',model_type='job',reference_id=id)
        for employee in team:
            notification_hub_obj.send_to_team.add(employee.id) 
        return Response(serializer.data)

@api_view(['GET','PATCH'])         
@permission_classes([IsAuthenticated])
def job_card_view(request,job_id = 0):
    if request.method == 'GET':
        try:
            this_job = Job.objects.get(id=job_id)
            serializer = JobCardGetSerializer(this_job,many=False,context={'job':job_id})
            
            try:
                cstm_job_card = JobCard.objects.get(custom_job = this_job)
                serializer_cstm = CustomJobCardGetSerializer(cstm_job_card,many=False)
                serializer_list =[serializer.data,serializer_cstm.data]
            except:
                return Response(serializer.data)
                pass

            return Response(serializer_list)
        except Exception as E:
            return Response({"Error":str(E),"app_data":"something went wrong"}) 
@api_view(['GET'])         
@permission_classes([IsAuthenticated])
def get_previous_sale(request,client_id):
    if request.method=='GET':
        try:

            data=[]
            user = request.user
            client = Client.objects.get(id=client_id)
            jobs = Job.objects.filter(client=client,schedule_status=True)
            serializer = JobGetSerializer(jobs,many=True)
        
            return Response(serializer.data)  
        except Exception as E:
            return Response({"Error":str(E),"app_data":"something went wrong"})        
        
          
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def job_search(request,tab_type):
    if request.method == 'POST':
        try:
            key = request.POST['key']
            if(key == ' '):
                job_found = Job.objects.filter(tab_type=tab_type)
                serializer = JobGetSerializer(job_found,many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:

                job_found=Job.objects.filter(Q(uuid__istartswith=key) | Q(created_by__name__istartswith=key) | Q(status__istartswith=key) | Q(schedule_status__istartswith=key) | Q(client__client_name__istartswith=key) | Q(job_type__istartswith=key) |  Q(amount__istartswith=key)).filter(tab_type=tab_type)
                serializer = JobGetSerializer(job_found,many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'No maches found'}, status=status.HTTP_400_BAD_REQUEST) 

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def filterby_price_range(request,tab_type):
    if request.method == 'POST':
        try:
            job_list = []
            start_price = request.POST['start_price']
            end_price = request.POST['end_price']
            for job_obj in Job.objects.filter(tab_type=tab_type):
               if int(job_obj.quote.invoice_amt) >= int(start_price) and int(job_obj.quote.invoice_amt) <=int(end_price):
                   job_list.append(job_obj)
            serializer = JobGetSerializer(job_list,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'No maches found'}, status=status.HTTP_400_BAD_REQUEST) 
  
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def filterby_client_name(request,tab_type,filter_type):
    if request.method == 'POST':
        try:
                limit = request.GET['limit']
                page = request.GET['page']
                if filter_type == "client":
                    client_id = request.POST['client_id']
                    client_obj =Client.objects.get(id=client_id)
                    
                    if tab_type == 'waste' or tab_type == 'all':
                        job_obj = Job.objects.filter(client=client_obj)
                    else:
                        job_obj = Job.objects.filter(tab_type=tab_type,client=client_obj)
                    serializer = JobGetSerializer(job_obj,many=True)    
                    paginate_data = paginate(serializer.data,int(page),int(limit))
                    return Response(paginate_data,status=status.HTTP_200_OK)
                if filter_type == "date":
                    date = request.POST['date']
                    if tab_type == 'waste' or tab_type == 'all':
                        job_found=Job.objects.filter(Q(created_date_time__istartswith=date))
                    else:
                        quote_found=Job.objects.filter(Q(created_date_time__istartswith=date)).filter(tab_type=tab_type)
                    serializer = JobGetSerializer(job_found,many=True)    
                    paginate_data = paginate(serializer.data,int(page),int(limit))
                    return Response(paginate_data,status=status.HTTP_200_OK)    
                
            
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'No maches found'}, status=status.HTTP_400_BAD_REQUEST)           

@api_view(['GET','POST']) 
@permission_classes([IsAuthenticated])
def ready_for_schedule_status(request,schedule_status,job_id):
    if request.method == 'GET':
        emp = Employee.objects.get(user=request.user)
        permissions = quote_permissions(emp)
        
        if permissions['create_quote']:

            if schedule_status  == 'true':
                try:   
                      
                        job_obj = Job.objects.get(id=job_id)
                    
                        if job_obj.ready_for_schedule ==True:
                            return Response({'app_data':'Already in active state'},status=status.HTTP_400_BAD_REQUEST)
                        job_obj.ready_for_schedule = True
                        job_obj.save()
                        try:
                            message =str(emp.name) + " added a job  for scheduling"
                            LoggingInfo.objects.create(message=message,quote=job_obj.quote)
                        except:
                            pass 
                        
                        try:
                            team_list = Employee.objects.filter(user_type="scheduler")
                            push_notifier_for_team("Job scheduled", str(emp.name) +  "added a job  for scheduling",team_list)
                            try:
                                # request.data['created_by']=user.id
                                title="Job is ready for schedule"
                                description = "Job is scheduled by " + str(job_obj.quote.employee.name)
                            except Exception as E:
                                print(str(E))
                                pass
                            notification_obj = Notification.objects.create(title = title,description=description) 
                            
                            managers  = Employee.objects.filter(user_type = "scheduler")
                            for member in managers:
                                notification_obj.members.create(member_id=member)
                            try:
                                request.data._mutable = False
                            except:
                                pass  
                        except Exception as E:
                            print(str(E))
                            pass
                        team = Employee.objects.filter(user_type='manager')
                        notification_hub_obj = Notification_hub.objects.create(type='edited',model_type='job',reference_id=job_obj.id)
                        for employee in team:
                            notification_hub_obj.send_to_team.add(employee.id)
                        return Response({'app_data': 'Job status accepted'},status=status.HTTP_200_OK)    


                except:
                    return Response({'app_data':"Job does not exists"},status=status.HTTP_400_BAD_REQUEST)

            elif schedule_status  == 'false':
                try:   
                   
                            
                        job_obj = Job.objects.get(id=job_id)
                    
                        if job_obj.ready_for_schedule ==False:
                        
                            return Response({'app_data':'Already in active state'},status=status.HTTP_400_BAD_REQUEST)
                        job_obj.ready_for_schedule = False
                        job_obj.save()   
                        qoute_obj = job_obj.quote
                        qoute_obj.sales_team_review = False
                        qoute_obj.save()
                        try:
                            message =str(emp.name) + " Removed a job from ready for scheduling"
                            LoggingInfo.objects.create(message=message,quote=job_obj.quote)
                        except:
                            pass 
                        try:
                            team_list = Employee.objects.filter(user_type="scheduler")
                            push_notifier_for_team(str(emp.name) +  " reviewd  a job  status as reject",'scheduler',team_list)
                           
                            title="Job is rejected "
                            description = "Job is scheduled by " + str(job_obj.quote.employee.name)
                    
                            notification_obj = Notification.objects.create(title = title,description=description) 
                            
                            managers  = Employee.objects.filter(user_type = "scheduler")
                            for member in managers:
                                notification_obj.members.create(member_id=member)
                        except Exception as E:
                            print(str(E))
                            pass
                        team = Employee.objects.filter(user_type='manager')
                        notification_hub_obj = Notification_hub.objects.create(type='edited',model_type='job',reference_id=job_obj.id)
                        for employee in team:
                            notification_hub_obj.send_to_team.add(employee.id)
                        return Response({'app_data': 'Job status rejected'},status=status.HTTP_200_OK)    
                    
                except Exception as E:
                    return Response({'Error':str(E),'app_data':"Job does not exists"},status=status.HTTP_400_BAD_REQUEST)        
        else:
            return Response({'app_data':"You have no permission to do this operation"},status=status.HTTP_400_BAD_REQUEST)        
                    

@api_view(['POST']) 
@permission_classes([IsAuthenticated])
def job_search_by_client_id(request,tab_type):
    if request.method == 'POST':
        try:
            key = request.POST['key']
            try:
                page = int(request.GET['page'])
                limit = int(request.GET['limit'])
            except:
                pass  
            
            if(key == ' '):
                if (tab_type =='waste' or tab_type =='all'):
                    job_found = Job.objects.all()
                else:
                    job_found = Job.objects.filter(tab_type=tab_type)
                serializer = JobGetSerializer(job_found,many=True)
                paginate_data = paginate(serializer.data,page,limit)    
                return Response(paginate_data, status=status.HTTP_200_OK) 
            else:
                if (tab_type =='waste' or tab_type =='all'):
                        job_found =Job.objects.filter(client__client_name__istartswith=key)
                else:
                        job_found = Job.objects.filter(client__client_name__istartswith=key).filter(tab_type=tab_type)
                
                serializer = JobGetSerializer(job_found,many=True)
                paginate_data = paginate(serializer.data,page,limit)    
                return Response(paginate_data, status=status.HTTP_200_OK) 
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'No maches found'}, status=status.HTTP_400_BAD_REQUEST)                      


@api_view(['PATCH','GET','POST']) 
@permission_classes([IsAuthenticated])
def custom_job_card(request,quote_id):
    if request.method =='PATCH':
        emp = Employee.objects.get(user=request.user)
        try:
            if JobCard.objects.filter(custom_quote=request.data['custom_quote']).exists():
                custom_job_card_obj = JobCard.objects.get(custom_quote__id=quote_id)
                serializer = QuoteCardGetSerializer(custom_job_card_obj,data=request.data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    try:
                        quote_obj = Quote.objects.get(id=quote_id)
                        message =str(emp.name) + " updated the job card"
                        LoggingInfo.objects.create(message=message,quote=quote_obj)
                    except:
                        pass 
                    return Response(serializer.data)
                    
                    
                else:
                    return Response(serializer.errors )
            else:

                serializer = CustomJobCardSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    try:
                        quote_obj = Quote.objects.get(id=quote_id)
                        message =str(emp.name) + " Created a custom the job card"
                        LoggingInfo.objects.create(message=message,quote=quote_obj)
                    except:
                        pass 
                    return Response(serializer.data)
                else:
                    return Response({"Error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST )
                        
            

        except Exception as E:    
            return Response({'Error': str(E), 'app_data': 'No maches found'}, status=status.HTTP_400_BAD_REQUEST)
    if request.method =='GET':
        try:
            
               
                this_job = Quote.objects.get(id=quote_id)
                serializer = JobCardGetSerializer(this_job,many=False,context={'quote':quote_id})
                if JobCard.objects.filter(custom_quote=this_job).exists():

                    custom_job_card_obj = JobCard.objects.get(custom_quote=this_job)
                    custom_serializer = CustomJobCardGetSerializer(custom_job_card_obj,many=False)
                   
                    if serializer.data['site_location'] == None:
                        data = custom_serializer.data['custom_site_address']
                        serializer.data['site_location'] = data
                        return Response(serializer.data)
                       
                return Response(serializer.data)
                
               
        
        except Exception as E:
            return Response({"Error":str(E),"app_data":"something went wrong"}, status=status.HTTP_400_BAD_REQUEST)  

@api_view(['GET','POST','PUT','DELETE']) 
@permission_classes([IsAuthenticated])
def create_job_card_info(request,job_card_id =0):
    if request.method =='POST':
        try:
            data = request.data
            serializer = JobCardInfoSerializer(data=request.data)

            if serializer.is_valid():
                new_serializer_object = serializer.save()
              
                
                if "service_list" in request.data: 
                    
                    for service in data["service_list"]:
                        try:
                            request.data._mutable = True
                        except:
                            pass
                        try:
                            number = service['no']
                        except:
                            number = ""
                        try:
                            capacity = service['capacity']
                        except:
                            capacity = ""    
                        try:
                            frequency = service['frequency']
                        except:
                            frequency = ""
                        try:
                            pit_location = service['pit_location']
                        except:
                            pit_location = ""   
                        try:
                            waste_type = service['waste_type']
                        except:
                            waste_type =""

                               

                        data = Services.objects.create(no=number,waste_type=waste_type,pit_location = pit_location,frequency =frequency,capacity=capacity)
                        
                        new_serializer_object.services.add(data.id)
                        new_serializer_object.save()
                        try:
                            request.data._mutable = False
                        except:
                            pass  
                    return Response({"app_data":"job card created","dev_data":"job card created"})       

            else:
                return Response({"Error":serializer.errors,"app_data":"something went wrong"}, status=status.HTTP_400_BAD_REQUEST) 
        except Exception as E:
            return Response({"Error":str(E),"app_data":"something went wrong"}, status=status.HTTP_400_BAD_REQUEST)        

    if request.method =='GET':      
        try:
            job_card_info_obj = JobcardInfo.objects.all()
            serializer = JobCardInfoGetSerializer(job_card_info_obj,many=True)
            return Response (serializer.data)
        except Exception as E:
            return Response({"Error":str(E),"app_data":"something went wrong"}, status=status.HTTP_400_BAD_REQUEST) 
    if request.method =='PUT':      
        try:
            job_card_info = JobcardInfo.objects.get(id=job_card_id)
            print(request.data)
            serializer = JobCardInfoSerializer(job_card_info,data=request.data,partial=True)
            if serializer.is_valid():
                new =serializer.save()     
                print(serializer.data)           
                
                return Response(serializer.data) 
            else:
                return Response({'Error':serializer.errors})      
        except Exception as E:
            return Response({"Error":str(E),"app_data":"something went wrong"}, status=status.HTTP_400_BAD_REQUEST)      

    if request.method =="DELETE":
        try:

            job_card_info = JobcardInfo.objects.get(id=job_card_id)
            job_card_info.delete()

            return Response({"app_data":"job card deleted","dev_data":"job card deleted"})   
        except Exception as E:
            return Response({"Error":str(E),"app_data":"something went wrong"}, status=status.HTTP_400_BAD_REQUEST)   

#job card get api using quote id
@api_view(['GET']) 
@permission_classes([IsAuthenticated])
def get_job_card_by_quote(request,quote_id):    
    if request.method =='GET':
        try:
            quote_obj = Quote.objects.get(id=quote_id)
            job_card_obj =JobcardInfo.objects.get(quote =quote_obj)
            serializer = JobCardInfoGetSerializer(job_card_obj,many=False)
            return Response(serializer.data)
        except Exception as E:
             return Response({'Error':  str(E),'app_data':"Something went wrong"},status= status.HTTP_400_BAD_REQUEST)

#job card get api using client id
@api_view(['GET']) 
@permission_classes([IsAuthenticated])
def get_job_card_by_client(request,client_id):    
    if request.method =='GET':
        try:
            job_card_obj =JobcardInfo.objects.filter(client =client_id)
            serializer = JobCardInfoGetSerializer(job_card_obj,many=True)
            return Response(serializer.data)
        except Exception as E:
             return Response({'Error':  str(E),'app_data':"Something went wrong"},status= status.HTTP_400_BAD_REQUEST)
        

                

                        
