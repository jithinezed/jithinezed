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
from jobs.models import Job
from .serializer import JobGetSerializer,ScheduleGetSerializer
from schedules.models import Schedule
from oh_and_s.serializers import NotificationGetSerializer,NewsGetSerializer
from oh_and_s.models import Notification,News
from accounts_dash.models import Target
from django.contrib.auth.models import User
import requests
from ipstack import GeoLookup
from geopy.geocoders import Nominatim

@api_view(['GET'])         
@permission_classes([IsAuthenticated])
def home_view(request,api_type,year,page_number=1):
    try:
        user = Employee.objects.get(user=request.user)
        if request.method == 'GET': 
            home =[]
            current_date = datetime.now()
            try:
                slots =[]

                if api_type == 'waste':
                    try:                     
                        all_jobs = Job.objects.all()
                    except Exception as E:
                        return Response({'Error': str(E), 'app_data': 'Job fetching failed'}, status=status.HTTP_400_BAD_REQUEST)
                    try:                     
                        all_schedule = Schedule.objects.filter(start_date =current_date)[:4]
                    except Exception as E:
                        return Response({'Error': str(E), 'app_data': 'Schedule fetching failed'}, status=status.HTTP_400_BAD_REQUEST)        
                elif api_type == 'all':
                    try:                     
                        all_jobs = Job.objects.all()
                    except Exception as E:
                        return Response({'Error': str(E), 'app_data': 'Job fetching failed'}, status=status.HTTP_400_BAD_REQUEST)
                    try:                     
                        all_schedule = Schedule.objects.filter(start_date =current_date)[:4]
                    except Exception as E:
                        return Response({'Error': str(E), 'app_data': 'Schedule fetching failed'}, status=status.HTTP_400_BAD_REQUEST)
                elif api_type == 'hills':
                    try:                     
                        all_jobs = Job.objects.filter(tab_type='hills')
                    except Exception as E:
                        return Response({'Error': str(E), 'app_data': 'Job fetching failed'}, status=status.HTTP_400_BAD_REQUEST)
                    try:                     
                        all_schedule = Schedule.objects.filter(tab_type='hills',start_date =current_date)[:4]
                    except Exception as E:
                        return Response({'Error': str(E), 'app_data': 'Schedule fetching failed'}, status=status.HTTP_400_BAD_REQUEST)        
                
                elif api_type == 'pumps':
                    try:                     
                        all_jobs = Job.objects.filter(tab_type='pumps')
                    except Exception as E:
                        return Response({'Error': str(E), 'app_data': 'Job fetching failed'}, status=status.HTTP_400_BAD_REQUEST)
                    try:                     
                        all_schedule = Schedule.objects.filter(tab_type='pumps',start_date =current_date)[:4]
                    except Exception as E:
                        return Response({'Error': str(E), 'app_data': 'Schedule fetching failed'}, status=status.HTTP_400_BAD_REQUEST)        
                
                elif api_type == 'destruction':
                    try:                     
                        all_jobs = Job.objects.filter(tab_type='destruction')
                    except Exception as E:
                        return Response({'Error': str(E), 'app_data': 'Job fetching failed'}, status=status.HTTP_400_BAD_REQUEST)
                    try:                     
                        all_schedule = Schedule.objects.filter(tab_type='destruction',start_date =current_date)[:4]
                    except Exception as E:
                        return Response({'Error': str(E), 'app_data': 'Schedule fetching failed'}, status=status.HTTP_400_BAD_REQUEST)        
                    
                else:
                    return Response({'app_data': 'type should be waste, pumps, hills or destruction'}, status=status.HTTP_400_BAD_REQUEST)
                    
               

                for i in reversed(all_schedule):
                    
                        start = i.start_time.strftime("%I:%M %p")
                        end = i.end_time.strftime("%I:%M %p")
                        slots.append({
                            'slot':'Active',
                            'id':i.id,
                            'start_time':start,
                            'end_time':end,
                            'status':i.status,
                            'name':i.job.created_by.name,
                            'dp':i.job.created_by.dp.url
                        })
            except:
                slots = []     
            
            #News
            try:
                notifications_list =[]
                limit = request.GET['limit']
                obj = News.objects.filter(news_member__member_id = user)
                serializer = NewsGetSerializer(obj,many=True,context={'member':user.id})  
                paginate_data = paginate(serializer.data,page_number,int(limit))
                notifications_list=paginate_data

            except:    
                 notifications_list = notifications_list
            #notification
            try:
                news_list =[]
                limit = request.GET['limit']
                obj = Notification.objects.filter(members__member_id =user.id)
                # Notification.objects.
                serializer = NotificationGetSerializer(obj,many=True,context={'member':user.id})  
                paginate_data = paginate(serializer.data,page_number,int(limit))
                news_list=paginate_data

            except :  
     
                 news_list = [] 


            #Safty data
            try:

                Safty_data = [
                    
                ]
                people = {'LTI':'2','MTIU':'3','FTI':'0'}
                vehicle ={'at_fault':'0','not_fault':"12"}
                Safty_data.append(people)
                Safty_data.append(vehicle)
            except:

                Safty_data =[]
            # job list  
            
            try:
                graph_data=[]
                serializer = JobGetSerializer(all_jobs, many=True)   
                #sales graph
                current_year = year
            
                
               
                peak_target = 0        
                target_obj =Target.objects.filter(date__year =current_year)
                largest=0
                if target_obj:
                    for i in target_obj:
                        if i.target >peak_target:
                            peak_target=i.target
                        if i.date.month == 1:
                            jan_data={'month':'jan','target':i.target}
                        if i.date.month == 2:
                            feb_data={'month':'feb','target':i.target}
                        if i.date.month == 3:
                            mar_data={'month':'mar','target':i.target}

                        if i.date.month == 4:
                            apr_data={'month':'apr','target':i.target}
                        if i.date.month == 5:
                            may_data={'month':'may','target':i.target}

                        if i.date.month == 6:
                            jun_data={'month':'jun','target':i.target}
                        if i.date.month == 7:
                            july_data={'month':'july','target':i.target}
                        if i.date.month == 8:
                            aug_data={'month':'aug','target':i.target}

                        if i.date.month == 9:
                            sep_data={'month':'sep','target':i.target}
                        if i.date.month == 10:
                            oct_data={'month':'octb','target':i.target}

                        if i.date.month == 11:
                            nov_data={'month':'nov','target':i.target}    
                        if i.date.month == 12:
                            dec_data={'month':'dec','target':i.target}
                    largest = peak_target        
                    amount=0
                    if Target.objects.filter(date__month=1).exists() :

                        jan_obj =Job.objects.filter(edited_date_time__year =current_year,edited_date_time__month=1)
                        
                        for i in jan_obj:
                            try:
                                amount = amount+int(i.amount)
                            except:
                                amount = 0
                        jan_data['sale']=amount
                        graph_data.append(jan_data)
                        if amount > largest:
                            largest =amount
                        
                        amount=0
                    
                    else:
                        graph_data.append({"month":"january","target":0,"sale":0})
                        amount=0     
                    if  Target.objects.filter(date__month=2).exists(): 
                        feb_obj =Job.objects.filter(edited_date_time__year =current_year,edited_date_time__month=2)
                        for i in feb_obj:
                            try:
                                amount = amount+int(i.amount)
                            except:
                                amount = 0
                        feb_data['sale']=amount
                        graph_data.append(feb_data)
                        if amount > largest:
                            largest =amount
                        amount=0
                    else:
                        graph_data.append({"month":"february","target":0,"sale":0})  
                        amount=0  
                    if  Target.objects.filter(date__month=3).exists(): 
                        mar_obj =Job.objects.filter(edited_date_time__year =current_year,edited_date_time__month=3)
                        for i in mar_obj:
                            try:
                                amount = amount+int(i.amount)
                            except:
                                amount = 0
                        mar_data['sale']=amount
                        graph_data.append(mar_data)
                        if amount > largest:
                            largest =amount
                        amount=0
                    else:
                        graph_data.append({"month":"march","target":0,"sale":0})   
                        amount=0  
                    if  Target.objects.filter(date__month=4).exists(): 
                        apr_obj =Job.objects.filter(edited_date_time__year =current_year,edited_date_time__month=4)
                        for i in apr_obj:
                            try:
                                amount = amount+int(i.amount)
                            except:
                                amount = 0
                        apr_data['sale']=amount
                        graph_data.append(apr_data)
                        if amount > largest:
                            largest =amount
                        amount=0
                    else:
                        graph_data.append({"month":"april","target":0,"sale":0})  
                        amount=0   
                    if  Target.objects.filter(date__month=5).exists(): 

                        may_obj =Job.objects.filter(edited_date_time__year =current_year,edited_date_time__month=5)
                        for i in may_obj:
                            try:
                                amount = amount+int(i.amount)
                            except:
                                amount = 0
                        may_data['sale']=amount
                        graph_data.append(may_data)
                        if amount > largest:
                            largest =amount
                        amount=0
                    else:
                        graph_data.append({"month":"may","target":0,"sale":0})   
                        amount=0  
                    if  Target.objects.filter(date__month=6).exists(): 

                        jun_obj =Job.objects.filter(edited_date_time__year =current_year,edited_date_time__month=6)
                        for i in jun_obj:
                            try:
                                amount = amount+int(i.amount)
                            except:
                                amount = 0
                        jun_data['sale']=amount
                        graph_data.append(jun_data)
                        if amount > largest:
                            largest =amount
                        amount=0 
                    else:
                        graph_data.append({"month":"june","target":0,"sale":0})     
                        amount=0
                    if  Target.objects.filter(date__month=7).exists(): 

                        july_obj =Job.objects.filter(edited_date_time__year =current_year,edited_date_time__month=7)
                        for i in july_obj:
                            try:
                                amount = amount+int(i.amount)
                            except:
                                amount = 0
                        july_data['sale']=amount
                        graph_data.append(july_data)
                        if amount > largest:
                            largest =amount
                    else:
                        graph_data.append({"month":"july","target":0,"sale":0})   
                        amount=0
                    if  Target.objects.filter(date__month=8).exists(): 
                        amount=0
                        aug_obj =Job.objects.filter(edited_date_time__year =current_year,edited_date_time__month=8)
                        for i in aug_obj:
                            try:
                                amount = amount+int(i.amount)
                            except:
                                amount = 0
                        aug_data['sale']=amount
                        graph_data.append(aug_data)
                        if amount > largest:
                            largest =amount
                        amount=0
                    else:
                        graph_data.append({"month":"august","target":0,"sale":0}) 
                        amount=0    
                    if  Target.objects.filter(date__month=9).exists(): 
                        sep_obj =Job.objects.filter(edited_date_time__year =current_year,edited_date_time__month=9)
                        for i in sep_obj:
                            try:
                                amount = amount+int(i.amount)
                            except:
                                amount = 0
                        sep_data['sale']=amount
                        graph_data.append(sep_data)
                        if amount > largest:
                            largest =amount
                        amount=0
                    else:
                        graph_data.append({"month":"september","target":0,"sale":0})    
                        amount=0  
                    if  Target.objects.filter(date__month=10).exists(): 

                        oct_obj =Job.objects.filter(edited_date_time__year =current_year,edited_date_time__month=10)
                        for i in oct_obj:
                            try:
                                amount = amount+int(i.amount)
                            except:
                                amount = 0
                        oct_data['sale']=amount
                        graph_data.append(oct_data)
                        if amount > largest:
                            largest =amount
                        amount=0
                    else:
                        graph_data.append({"month":"october","target":0,"sale":0})
                        amount=0     
                    if  Target.objects.filter(date__month=11).exists(): 

                        nov_obj =Job.objects.filter(edited_date_time__year =current_year,edited_date_time__month=11)
                        for i in nov_obj:
                            try:
                                amount = amount+int(i.amount)
                            except:
                                amount = 0
                        nov_data['sale']=amount
                        graph_data.append(nov_data)
                        if amount > largest:
                            largest =amount
                        amount=0
                    else:
                        graph_data.append({"month":"november","target":0,"sale":0})    
                        amount=0 
                    if  Target.objects.filter(date__month=12).exists(): 

                        dec_obj =Job.objects.filter(edited_date_time__year =current_year,edited_date_time__month=12)
                        for i in dec_obj:
                            try:
                                amount = amount+int(i.amount)
                            except:
                                amount = 0    
                        dec_data['sale']=amount
                        graph_data.append(dec_data)
                        if amount > largest:
                            largest =amount
                            
                        amount=0  
                    else:
                        graph_data.append({"month":"december","target":0,"sale":0})  
                        amount=0   

                
                    print(largest)
            except:
                graph_data=[]
            return Response({"graph_peak":largest,"graph_data":graph_data,'job_list':serializer.data,"schedule_of_the_day":slots,"Notifications":news_list,"news":notifications_list,"saftey_data":Safty_data})
        

    except Exception as E:
        return Response({'Error': str(E), 'app_data': 'Data fetching failed'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])         
@permission_classes([IsAuthenticated])
def weather_report(request):
    if request.method =="GET":
        try:
            geolocator = Nominatim(user_agent="geoapiExercises")
            Latitude = request.GET['lat']
            Longitude = request.GET['lon']
            location = geolocator.reverse(Latitude+","+Longitude)

            loc=(str(location))
            x = loc.split(", ")
            region = x[0]
        except:
            region ="sidney"
        try:
            
            r = requests.get("http://api.openweathermap.org/data/2.5/forecast/?q=" + region +"&cnt=7&units=metric&APPID=e6b31078b3ff77d20d9f5a9fbd459e91")
            return Response(r.json())
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'No maches found'}, status=status.HTTP_400_BAD_REQUEST)
