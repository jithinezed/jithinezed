import os
import arrow
import datetime
from django.db.models import Sum
from django.shortcuts import render, HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework import status
from django.contrib.auth.models import User
import calendar 
from .models import Roaster
from .serializers import (RoasterSerializer,RoasterGetSerializer,
RoasterGetReportSerializer)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getRoaster(request,date):
    if request.method == 'GET':
        try:
            roaster = Roaster.objects.filter(active_status=True).filter(day=date)
            serializer = RoasterGetSerializer(roaster,many=True)
            return Response(serializer.data)
        except:
            return Response({'Error': 'No such Roster found', 'app_data': 'No such a Roster found '}, status=status.HTTP_400_BAD_REQUEST)    
    

@api_view(['GET','PATCH','DELETE'])
@permission_classes([IsAuthenticated])
def getRoasterById(request,roaster_id,date):
    if request.method == 'GET':
        try:
            roaster = Roaster.objects.filter(active_status=True,id=roaster_id).filter(day=date)
            serializer = RoasterGetSerializer(roaster,many=True)
            return Response(serializer.data)
        except:
            return Response({'Error': 'No such Roster found', 'app_data': 'No such a Roster found '}, status=status.HTTP_400_BAD_REQUEST)   
    if request.method == 'PATCH':
        try:
            roaster = Roaster.objects.get(id=roaster_id)
            serializer = RoasterSerializer(roaster,data=request.data,partial=True)
            if (serializer.is_valid()):
                serializer.save()
                return Response(serializer.data)
            else:
                 return Response({'Errors': serializer.errors, 'app_data': 'No such a Roster found '}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'Errors': 'No such Roster found', 'app_data': 'No such a Roster found '}, status=status.HTTP_400_BAD_REQUEST)    
    if request.method == 'DELETE':
        try:  
            roaster = Roaster.objects.get(id=roaster_id)
            roaster.active_status=False
            roaster.save()               
            return Response({'Success': 'Roaster Deleted', 'app_data': 'Roaster deleted sucessfully'})
        except:
            return Response({'Error': 'No such a roaster found', 'app_data': 'No such a roaster found '}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createRoaster(request):
    if request.method == 'POST':
        try:
            roast_date = request.POST['day']
            roaster = Roaster.objects.filter(active_status=True).filter(day=roast_date).count()
            if(roaster >= 4):
                return Response({'Error': 'slots are full', 'app_data': 'No slots are available'}, status=status.HTTP_400_BAD_REQUEST)    
            else:
                    serializer = RoasterSerializer(data=request.data)
                    if serializer.is_valid():
                        serializer.save()                
                        return Response({'Success': 'Roster added','app_data': 'Roster added'}, status.HTTP_201_CREATED)
                    else:    
                       return Response({'Errors': serializer.errors, 'app_data': 'No such a Roster found '}, status=status.HTTP_400_BAD_REQUEST)          
        except:
            return Response({'Errors': 'No such Roster found', 'app_data': 'No such a Roster found '}, status=status.HTTP_400_BAD_REQUEST)    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def weaklyReport(request,date):
    if request.method == 'GET':
        list1={}
        given_date = datetime.datetime.strptime(date, '%Y-%m-%d')
        start_date = given_date - datetime.timedelta(days=given_date.weekday())
        week = datetime.timedelta(days=7)
        end_of_week = start_date + week
        day_delta = datetime.timedelta(days=1)
        for i in range((end_of_week - start_date).days):
            date1 = start_date + i*day_delta
            dlt=slice(0,10)
            typecast =str(date1)
            ad=typecast[dlt]
            weak_day = datetime.datetime.strptime(ad, '%Y-%m-%d').weekday() 
            day = calendar.day_name[weak_day]
            graph_data =Roaster.objects.filter(day=date1).filter(active_status=True).values_list('slot',flat=True)
            list1[day] = graph_data 
        roaster_count=Roaster.objects.filter(active_status=True).count() 
        revenue=Roaster.objects.filter(active_status=True).aggregate(Sum('amount')) 
        list1['total_revenue'] =revenue
        list1['roaster_count'] =roaster_count

        return Response({'app_data':list1})