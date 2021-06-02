import os
import datetime
from django.shortcuts import render, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework import status
from django.contrib.auth.models import User 
from .models import Vehicle,Fleet,TruckMaintananceReport,FuelExpense,ForkliftMaintananceReport,PreInspectionCheck,VehicleFile,VehicleFolder,VehicleImages,PostImage,CarMaintananceReport
from .serializers import (VehicleSerializer, VehicleGetSerializer,
FleetGetSerializer,FleetSerializer,TruckMaintananceReportSerializer,
TruckMaintananceReportGetSerializer,FuelExpenseSerializer,FuelExpenseGetSerializer,VehicleIdGetSerializer,
ForkliftMaintananceReportSerializer,ForkliftMaintananceReportGetSerializer,PreInspectionCheckSerializer,
PreInspectionCheckGetSerializer,VehicleFileSerializer,VehicleFileGetSerializer,VehicleFolderGetSerializer,VehicleFolderSerializer,VehicleImagesSerializer,VehicleImagesGetSerializer,CarMaintananceReportSerializer)
from .general import paginate
from django.db.models import Q
from django.http import JsonResponse
import json
from .models import VehicleFolder,VehicleImage

from accounts.models import Employee
from notification.models import Notification_hub

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getAllVehicleAPI(request,v_type,page_number=0):
    if request.method == 'GET':
        try:  
            if (v_type=='truck'):
                vehicle = Vehicle.objects.filter( vehicle_type='truck').filter(active_status=True)         
                serializer = VehicleGetSerializer(vehicle,many=True)  
                if(page_number == 0):
                    return Response(serializer.data)

                paginated_data = paginate(serializer.data,page_number,8)
                return Response(paginated_data)
            if (v_type=='car'):
                vehicle = Vehicle.objects.filter( vehicle_type='car').filter(active_status=True)         
                serializer = VehicleGetSerializer(vehicle,many=True)  
                if(page_number == 0):
                    return Response(serializer.data)                 
                paginated_data = paginate(serializer.data,page_number,8)
                return Response(paginated_data)
            if (v_type=='fork-lift'):
                vehicle = Vehicle.objects.filter( vehicle_type='fork-lift').filter(active_status=True)         
                serializer = VehicleGetSerializer(vehicle,many=True)
                if(page_number == 0):
                    return Response(serializer.data)                   
                paginated_data = paginate(serializer.data,page_number,8)
                return Response(paginated_data)        
        except:
            return Response({'Error': 'Error in vehicle type', 'app_data': 'Vehicle type is not found'}, status=status.HTTP_400_BAD_REQUEST)    

@api_view(['POST'])
def vehicleCreateAPI(request):
    if request.method == 'POST':
        try:
            serializer = VehicleSerializer(data=request.data)

            if serializer.is_valid():
                vehicle_data = serializer.save() 
                try:
                    request.POST._mutable = True
                except:
                    pass
                if 'images' in request.data:
                    try:
                        file_attachment_list =[]
                        uploaded_images = request.data.pop('images')
                        print(uploaded_images)
                        image_obj = Vehicle.objects.get(id=vehicle_data.id)
                        if not uploaded_images == ['']:  
                            for attachment in uploaded_images:  
                                thiss=vehicle_data.images.create(image_file=attachment)
                    except Exception as E:
                        return Response({'Error': str(E),'app_data': 'something went wrong'}, status=status.HTTP_400_BAD_REQUEST)            

                team = Employee.objects.filter(user_type='manager',active_status=True)
                notification_hub_obj = Notification_hub.objects.create(type='added ',model_type='vehicle',reference_id=serializer.data['id'])
                for employee in team:
                    notification_hub_obj.send_to_team.add(employee.id)                
                return Response({'Success': 'Vehicle Added','app_data': 'Vehicle Added '}, status.HTTP_201_CREATED)
            else:
                return Response({'Error':serializer.errors,'app_data':"something went wrong"},status=status.HTTP_400_BAD_REQUEST)    
        except Exception as E:
            return Response({'Error': str(E),'app_data': 'Vehicle Registration failed'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def vehicleDeleteAPI(request, vehicle_id):
    if request.method == 'DELETE':
        try:  
            
            vehicle = Vehicle.objects.get(id=vehicle_id)
            if vehicle.active_status == False:
                return Response({'Error': 'No such a vehicle found', 'app_data': 'No such a Vehicle found '}, status=status.HTTP_400_BAD_REQUEST)
            vehicle.active_status=False
            vehicle.save()  
            team = Employee.objects.filter(user_type='manager',active_status=True)
            notification_hub_obj = Notification_hub.objects.create(type='deleted',model_type='vehicle',reference_id=vehicle.id)
            for employee in team:
                notification_hub_obj.send_to_team.add(employee.id)              
            return Response({'Success': 'Vehicle Deleted', 'app_data': 'Vehicle deleted sucessfully'})
        except:
            return Response({'Error': 'No such a vehicle found', 'app_data': 'No such a Vehicle found '}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def vehicleEditAPI(request, vehicle_id):
    if request.method == 'PATCH':
        try: 
            try:
                if (request.data['year'] =="null"):
                    try:
                        request.data._mutable=True
                    except:
                        pass
                    request.data['year'] =None  
            except:
                try:
                    request.data._mutable=True
                except:
                    pass
                request.data['year'] =None 
            try:    
                if (request.data['previous_rego'] =="null"):
                    try:
                        request.data._mutable=True
                    except:
                        pass
                    print("None")    
                    request.data['previous_rego'] =None         
            except:
                try:
                    request.data._mutable=True
                except:
                    pass
                request.data['previous_rego'] =None


            vehicle = Vehicle.objects.get(id=vehicle_id)
            serializer = VehicleSerializer(vehicle, data=request.data, partial=True)   
           
            if serializer.is_valid():
                vehicle_data= serializer.save()  
                if 'images' in request.data:
                    file_attachment_list =[]
                    uploaded_images = request.data.pop('images')
                    image_obj = Vehicle.objects.get(id=vehicle_data.id)
                    if not uploaded_images == ['']:  
                        for attachment in uploaded_images:  
                            thiss=vehicle_data.images.create(image_file=attachment)
                team = Employee.objects.filter(user_type='manager',active_status=True)
                notification_hub_obj = Notification_hub.objects.create(type='edited',model_type='vehicle',reference_id=vehicle.id)
                print(notification_hub_obj)
                for employee in team:
                    notification_hub_obj.send_to_team.add(employee.id)    
            else:
                return Response({'Error': serializer.errors, 'app_data': 'serializer.errors'}, status=status.HTTP_400_BAD_REQUEST)     
            try:
                request.data._mutable=False
            except:
                pass      
            serializer2 = VehicleGetSerializer(vehicle,many=False)                  
            return Response(serializer2.data)            
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'No such vehicle found '}, status=status.HTTP_400_BAD_REQUEST)    

#Fleet apis

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getAllFleet(request,vehicle_id,page_number=1):
    if request.method == 'GET':
        try:  
            fleet = Fleet.objects.filter(active_status=True).filter(vehicle=vehicle_id)         
            serializer = FleetGetSerializer(fleet,many=True)                   
            
            paginated_data = paginate(serializer.data,page_number,8)
            return Response(paginated_data)
        except:
            return Response({'Error': 'No such fleet found', 'app_data': 'No fleet  found '}, status=status.HTTP_400_BAD_REQUEST)    

@api_view(['POST'])
def fleetCreateAPI(request):
    if request.method == 'POST':
        try:
            vid = request.POST['vehicle_id']
            make = request.POST['make']
            rego_due = request.POST['rego_due']
            location = request.POST['location']
            contact = request.POST['contact']
            rms_booking_by = request.POST['rms_booking_by']
            booked_date = request.POST['booked_date']
            completed = request.POST['completed']
            next_due = request.POST['next_due']     
            try:
                fleet = Fleet.objects.create(vehicle_id=vid,make=make,rego_due=rego_due,
                location=location,contact=contact,rms_booking_by=rms_booking_by,
                booked_date=booked_date,completed=completed,next_due=next_due)
                fleet.save()
                return Response({'Success': 'Fleet Added','app_data': 'Fleet Added '}, status.HTTP_201_CREATED)
            except:
                return Response({'Error': 'Fleet not saved ',
                'app_data': 'Invalid data, check your fields'}, status=status.HTTP_400_BAD_REQUEST)

        except:
            return Response({'Error': 'Error in fleetCreateAPI ',
                'app_data': 'Fleet registration failed'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def fleetDeleteAPI(request, fleet_id):
    if request.method == 'DELETE':
        try:  
            fleet = Fleet.objects.get(id=fleet_id)
            fleet.active_status=False
            fleet.save()               
            return Response({'Success': 'fleet Deleted', 'app_data': 'fleet deleted sucessfully'})
        except:
            return Response({'Error': 'No such a fleet found', 'app_data': 'No such a fleet found '}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def fleetEditAPI(request, fleet_id):
    if request.method == 'PATCH':
        try:  
            fleet = Fleet.objects.get(id=fleet_id)
            serializer = FleetGetSerializer(fleet, data=request.data, partial=True)   
            if serializer.is_valid():
                serializer.save()                
            return Response(serializer.data)            
        except:
            return Response({'Error': 'No such a fleet found', 'app_data': 'No such fleet found '}, status=status.HTTP_400_BAD_REQUEST)            

#############Forklift maintenance report#######################
@api_view(['POST'])
def forkLiftMaintananceReportCreateAPI(request):
    if request.method == 'POST':
        try:
            serializer = ForkliftMaintananceReportSerializer(data=request.data)
            data={}
            if serializer.is_valid():
                datas = serializer.save()
                team = Employee.objects.filter(user_type='manager',active_status=True)
                notification_hub_obj = Notification_hub.objects.create(type='added',model_type='fork_lift_report',reference_id=serializer.data['id'])
                for employee in team:
                    notification_hub_obj.send_to_team.add(employee.id)  
                return Response({'Success': 'Fork-lift maintanance report Registered','app_data': 'Fork-lift maintanance report Registered '}, status.HTTP_201_CREATED)
            else:
                return Response({'Error': serializer.errors,'app_data': 'maintanance report creation failed'}, status=status.HTTP_400_BAD_REQUEST)     
        except Exception as E:
            return Response({'Error': str(E),
                'app_data': 'maintanance report creation failed'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getForkliftMaintananceReports(request,page_number=1):
    if request.method == 'GET':
        try:  
                report = ForkliftMaintananceReport.objects.filter(active_status=True)
                serializer = ForkliftMaintananceReportGetSerializer(report,many=True) 
                paginated_data = paginate(serializer.data,page_number,8)                  
                return Response(paginated_data)
        except:
            return Response({'Error': 'No such Report found', 'app_data': 'No Reports  found '}, status=status.HTTP_400_BAD_REQUEST)    


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def ForlliftReportEditAPI(request, reportId):
    if request.method == 'PATCH':
        try:  
            report = ForkliftMaintananceReport.objects.get(id=reportId)
            serializer = ForkliftMaintananceReportGetSerializer(report, data=request.data, partial=True)   
            if serializer.is_valid():
                serializer.save()  
                team = Employee.objects.filter(user_type='manager',active_status=True)
                notification_hub_obj = Notification_hub.objects.create(type='edited',model_type='fork_lift_report',reference_id=report.id)
                for employee in team:
                    notification_hub_obj.send_to_team.add(employee.id)   
            else:
                return Response({'Error': serializer.errors, 'app_data': 'No such Report found '}, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data)            
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'No such Report found '}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def ForkliftMaintananceReportDelete(request,report_id):
    if request.method == 'DELETE':
        try:  
            report = ForkliftMaintananceReport.objects.get(id=report_id)
            report.active_status=False
            report.save()  
            team = Employee.objects.filter(user_type='manager',active_status=True)
            notification_hub_obj = Notification_hub.objects.create(type='deleted',model_type='fork_lift_report',reference_id=report.id)
            for employee in team:
                notification_hub_obj.send_to_team.add(employee.id)          
            return Response({'Success': 'Report Deleted', 'app_data': 'Report deleted sucessfully'})
        except:
            return Response({'Error': 'No such a report found', 'app_data': 'No such a report found '}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST','GET'])
@permission_classes([IsAuthenticated])
def forkliftSearchReport(request,page_number=1):
    if request.method == 'POST':
        try:
                key = request.POST['key']
                if key == ' ':
                    report_found=ForkliftMaintananceReport.objects.filter(active_status=True )
                    serializer = ForkliftMaintananceReportGetSerializer(report_found,many=True) 
                    paginate_data = paginate(serializer.data,page_number,8)
                    return Response(paginate_data, status=status.HTTP_200_OK)
                else:

                    report_found=ForkliftMaintananceReport.objects.filter(Q(vehicle__registration__istartswith=key) | 
                    Q(invoice_number__istartswith=key)).filter(vehicle__vehicle_type='fork-lift')
                    serializer = ForkliftMaintananceReportGetSerializer(report_found,many=True) 
                    paginate_data = paginate(serializer.data,page_number,8)
                    return Response(paginate_data, status=status.HTTP_200_OK)
            
        except:
            return Response({'Error': 'No searchReport present', 'app_data': 'No maches found'}, status=status.HTTP_400_BAD_REQUEST) 
            
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def lift_maintanance_search_by(request,filter_type):
    if request.method == 'POST':

        try:
            if(filter_type == 'vehicle'):
                inspection = ForkliftMaintananceReport.objects.filter(vehicle__registration= request.POST['registration']).filter(active_status=True)
                serializer = ForkliftMaintananceReportGetSerializer(inspection,many=True)                   
                # paginated_data = paginate(serializer.data,page_number,8)
                return Response(serializer.data)
            if(filter_type == 'day'):
                inspection = ForkliftMaintananceReport.objects.filter(rego_expiry_date = request.POST['date_time']).filter(active_status=True)
                serializer = ForkliftMaintananceReportGetSerializer(inspection,many=True)                   
                # paginated_data = paginate(serializer.data,page_number,8)
                return Response(serializer.data)    

        except:
            return Response({'Error': 'No Maintanance report  found', 'app_data': 'No such a Maintanance report added.'}, status=status.HTTP_400_BAD_REQUEST)
#------------------Car maintanance Report APIs-----------------------#

@permission_classes([IsAuthenticated])
@api_view(['POST'])
def carmaintananceReportCreateAPI(request):
    if request.method == 'POST':
        try:
            serializer = CarMaintananceReportSerializer(data=request.data)
            data={}
            if serializer.is_valid():
                datas = serializer.save()
                team = Employee.objects.filter(user_type='manager',active_status=True)
                notification_hub_obj = Notification_hub.objects.create(type='added',model_type='car_report',reference_id=serializer.data['id'])
                for employee in team:
                    notification_hub_obj.send_to_team.add(employee.id) 
                return Response({'Success': 'maintanance report Registered','app_data': 'maintanance report Registered '}, status.HTTP_201_CREATED)
            else:
                return Response ({'Error':serializer.errors,'app_data': 'maintanance report creation failed'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as E:
            return Response({'Error':  str(E),
                'app_data': 'maintanance report creation failed'}, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET','PATCH',"DELETE"])
@permission_classes([IsAuthenticated])
def getCarMaintananceReports(request,reportId='',page_number=1):
    if request.method == 'GET':
        # try:  
                report = CarMaintananceReport.objects.filter(active_status=True)  
                serializer = CarMaintananceReportSerializer(report,many=True) 
                paginated_data = paginate(serializer.data,page_number,8)                  
                return Response(paginated_data)
            # if (v_type == 'fork-lift'):  
            #     report = MaintananceReport.objects.filter(active_status=True).filter(vehicle__vehicle_type='fork-lift')
            #     serializer = MaintananceReportGetSerializer(report,many=True)                   
            #     paginated_data = paginate(serializer.data,page_number,7)                  
        #     #     return Response(paginated_data)
        # except:
        #     return Response({'Error': 'No such Report found', 'app_data': 'No Reports  found '}, status=status.HTTP_400_BAD_REQUEST)   
    if request.method == 'PATCH':
        try:  
            report = CarMaintananceReport.objects.get(id=reportId)
            serializer = CarMaintananceReportSerializer(report, data=request.data, partial=True)   
            if serializer.is_valid():
                serializer.save()  
                team = Employee.objects.filter(user_type='manager',active_status=True)
                notification_hub_obj = Notification_hub.objects.create(type='edited',model_type='truck_report',reference_id=serializer.data['id'])
                for employee in team:
                    notification_hub_obj.send_to_team.add(employee.id)               
                return Response(serializer.data)  
            else:
                return Response({'Error': serializer.errors, 'app_data': 'No such Report found '}, status=status.HTTP_400_BAD_REQUEST)       
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'No such Report found '}, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        try:  
            report = CarMaintananceReport.objects.get(id=reportId)
            report.active_status=False
            report.save()   
            team = Employee.objects.filter(user_type='manager',active_status=True)
            notification_hub_obj = Notification_hub.objects.create(type='deleted',model_type='truck_report',reference_id=report.id)
            for employee in team:
                notification_hub_obj.send_to_team.add(employee.id)             
            return Response({'Success': 'Report Deleted', 'app_data': 'Report deleted sucessfully'})
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'No such a report found '}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST','GET'])
@permission_classes([IsAuthenticated])
def car_searchReport(request,page_number=1):
    if request.method == 'POST':
        try:
                key = request.POST['key']
                report_found=CarMaintananceReport.objects.filter(Q(vehicle__registration__istartswith=key) | 
                Q(invoice_number__istartswith=key)).filter(vehicle__vehicle_type='car')
                serializer = CarMaintananceReportSerializer(report_found, many=True) 
                paginated_data = paginate(serializer.data,page_number,8)
                return Response(paginated_data, status=status.HTTP_200_OK)
        except:
            return Response({'Error': 'No searchReport present', 'app_data': 'No maches found'}, status=status.HTTP_400_BAD_REQUEST) 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def car_maintanance_search_by(request,filter_type):
    if request.method == 'POST':
        v_type = request.POST['vehicle_type']

        try:
            if(filter_type == 'vehicle'):
                inspection = CarMaintananceReport.objects.filter(vehicle__registration= request.POST['registration']).filter(active_status=True)
                serializer = CarMaintananceReportSerializer(inspection,many=True)                   
                # paginated_data = paginate(serializer.data,page_number,8)
                return Response(serializer.data)
            if(filter_type == 'day'):
                inspection = CarMaintananceReport.objects.filter(active_status=True,vehicle_type=v_type).filter(service_date = request.POST['date_time'])
                serializer = CarMaintananceReportSerializer(inspection,many=True)                   
                # paginated_data = paginate(serializer.data,page_number,8)
                return Response(serializer.data)    

        except:
            return Response({'Error': 'No Maintanance report  found', 'app_data': 'No such a Maintanance report added.'}, status=status.HTTP_400_BAD_REQUEST)






#------------------Truck maintanance Report APIs-----------------------#

@permission_classes([IsAuthenticated])
@api_view(['POST'])
def maintananceReportCreateAPI(request):
    if request.method == 'POST':
        try:
            serializer = TruckMaintananceReportSerializer(data=request.data)
            data={}
            if serializer.is_valid():
                datas = serializer.save()
                team = Employee.objects.filter(user_type='manager',active_status=True)
                notification_hub_obj = Notification_hub.objects.create(type='added',model_type='truck_report',reference_id=serializer.data['id'])
                for employee in team:
                    notification_hub_obj.send_to_team.add(employee.id) 
                return Response({'Success': 'maintanance report Registered','app_data': 'maintanance report Registered '}, status.HTTP_201_CREATED)
            else:
                return Response ({'Error':serializer.errors,'app_data': 'maintanance report creation failed'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as E:
            return Response({'Error':  str(E),
                'app_data': 'maintanance report creation failed'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMaintananceReports(request,page_number=1):
    if request.method == 'GET':
        try:  
                report = TruckMaintananceReport.objects.filter(active_status=True)  
                serializer = TruckMaintananceReportGetSerializer(report,many=True) 
                paginated_data = paginate(serializer.data,page_number,8)                  
                return Response(paginated_data)
            # if (v_type == 'fork-lift'):  
            #     report = MaintananceReport.objects.filter(active_status=True).filter(vehicle__vehicle_type='fork-lift')
            #     serializer = MaintananceReportGetSerializer(report,many=True)                   
            #     paginated_data = paginate(serializer.data,page_number,7)                  
            #     return Response(paginated_data)
        except:
            return Response({'Error': 'No such Report found', 'app_data': 'No Reports  found '}, status=status.HTTP_400_BAD_REQUEST)    















                  


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def ReportEditAPI(request, reportId):
    if request.method == 'PATCH':
        try:  
            report = TruckMaintananceReport.objects.get(id=reportId)
            serializer = TruckMaintananceReportGetSerializer(report, data=request.data, partial=True)   
            if serializer.is_valid():
                serializer.save()  
                team = Employee.objects.filter(user_type='manager',active_status=True)
                notification_hub_obj = Notification_hub.objects.create(type='edited',model_type='truck_report',reference_id=serializer.data['id'])
                for employee in team:
                    notification_hub_obj.send_to_team.add(employee.id)               
                return Response(serializer.data)  
            else:
                return Response({'Error': serializer.errors, 'app_data': 'No such Report found '}, status=status.HTTP_400_BAD_REQUEST)       
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'No such Report found '}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def MaintananceReportDelete(request, report_id):
    if request.method == 'DELETE':
        try:  
            report = TruckMaintananceReport.objects.get(id=report_id)
            report.active_status=False
            report.save()   
            team = Employee.objects.filter(user_type='manager',active_status=True)
            notification_hub_obj = Notification_hub.objects.create(type='deleted',model_type='truck_report',reference_id=report.id)
            for employee in team:
                notification_hub_obj.send_to_team.add(employee.id)             
            return Response({'Success': 'Report Deleted', 'app_data': 'Report deleted sucessfully'})
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'No such a report found '}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST','GET'])
@permission_classes([IsAuthenticated])
def searchReport(request,page_number=1):
    if request.method == 'POST':
        try:
                key = request.POST['key']
                report_found=TruckMaintananceReport.objects.filter(Q(vehicle__registration__istartswith=key) | 
                Q(invoice_number__istartswith=key)).filter(vehicle__vehicle_type='truck')
                serializer = TruckMaintananceReportGetSerializer(report_found, many=True) 
                paginated_data = paginate(serializer.data,page_number,8)
                return Response(paginated_data, status=status.HTTP_200_OK)
        except:
            return Response({'Error': 'No searchReport present', 'app_data': 'No maches found'}, status=status.HTTP_400_BAD_REQUEST) 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def truck_maintanance_search_by(request,filter_type):
    if request.method == 'POST':

        try:
            if(filter_type == 'vehicle'):
                inspection = TruckMaintananceReport.objects.filter(vehicle__registration= request.POST['registration']).filter(active_status=True)
                serializer = TruckMaintananceReportGetSerializer(inspection,many=True)                   
                # paginated_data = paginate(serializer.data,page_number,8)
                return Response(serializer.data)
            if(filter_type == 'day'):
                inspection = TruckMaintananceReport.objects.filter(service_date = request.POST['date_time']).filter(active_status=True)
                serializer = TruckMaintananceReportGetSerializer(inspection,many=True)                   
                # paginated_data = paginate(serializer.data,page_number,8)
                return Response(serializer.data)    

        except:
            return Response({'Error': 'No Maintanance report  found', 'app_data': 'No such a Maintanance report added.'}, status=status.HTTP_400_BAD_REQUEST)



#______________________Fuel expense_______________________#

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addFuelExpense(request):
    if request.method == 'POST':
        try:
            serializer = FuelExpenseSerializer(data=request.data)
            data={}
            if serializer.is_valid():
                datas = serializer.save()
                return Response({'Success': 'Fuel expense Added','app_data': 'Fuel expense Added'}, status.HTTP_201_CREATED)
        except:
            return Response({'Error': 'Error in addFuelExpense ',
                'app_data': 'Fuel expense adding failed'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getFuelExpense(request,v_type="truck",page_number=1):
    if request.method == 'GET':
        try:  
            fuel = FuelExpense.objects.filter(active_status=True,vehicle_type=v_type)
            serializer = FuelExpenseGetSerializer(fuel,many=True)   
            paginated_data = paginate(serializer.data,page_number,8)                
            return Response(paginated_data)                
        except:
            return Response({'Error': 'No  Fuel expense added yet!', 'app_data': 'No Fuel expense added yet!'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def FuelExpenseDelete(request, fuelEXP_id):
    if request.method == 'DELETE':
        try:  
            fuelexp = FuelExpense.objects.get(id=fuelEXP_id)
            fuelexp.active_status=False
            fuelexp.save()               
            return Response({'Success': 'Fuel expense Deleted', 'app_data': 'Fuel expense deleted sucessfully'})
        except:
            return Response({'Error': 'No Fuel expense  found', 'app_data': 'No such a Fuel expense added.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def fuelExpenseEditAPI(request, fuelEXP_id):
    if request.method == 'PATCH':
        try:  
            fuelEXP = FuelExpense.objects.get(id=fuelEXP_id)
            serializer = FuelExpenseGetSerializer(fuelEXP, data=request.data, partial=True)   
            if serializer.is_valid():
                serializer.save()                
            return Response(serializer.data)            
        except:
            return Response({'Error': 'No such a Fuel Expense data found', 'app_data': 'No Fuel Expense data exists'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getAllvehicleId(request,v_type):
    if request.method == 'GET':
        try: 
            
             if (v_type == 'truck'):
                vehicle = Vehicle.objects.filter(active_status=True).filter(vehicle_type='truck')  
                serializer = VehicleIdGetSerializer(vehicle,many=True)                    
                return Response(serializer.data)
             if (v_type == 'fork-lift'):  
                 vehicle = Vehicle.objects.filter(active_status=True).filter(vehicle_type='fork-lift')  
                 serializer = VehicleIdGetSerializer(vehicle,many=True)                      
                 return Response(serializer.data) 
             if (v_type == 'car'):  
                 vehicle = Vehicle.objects.filter(active_status=True).filter(vehicle_type='car')  
                 serializer = VehicleIdGetSerializer(vehicle,many=True)                      
                 return Response(serializer.data)      
        except:
            return Response({'Error': 'No such Vehicle', 'app_data': 'No vehicle  found '}, status=status.HTTP_400_BAD_REQUEST)    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def fuel_expns_search_by(request,filter_type):
    if request.method == 'POST':
        try:
            v_type = request.POST['vehicle_type']
        except:
            return Response({'Error': 'enter a valid vehicle type ', 'app_data': 'No such a vehicle exists.'}, status=status.HTTP_400_BAD_REQUEST) 

        try:
            if(filter_type == 'vehicle'):
                inspection = FuelExpense.objects.filter(vehicle__registration= request.POST['registration']).filter(active_status=True,vehicle_type=v_type)
                serializer = FuelExpenseGetSerializer(inspection,many=True)                   
                # paginated_data = paginate(serializer.data,page_number,8)
                return Response(serializer.data)
            if(filter_type == 'day'):
                date_time = request.POST['date_time']
                # year = date_time[:4]
                # month = date_time[5:7]
                # day = date_time[8:10]
                
                inspection = FuelExpense.objects.filter(active_status=True,vehicle_type=v_type).filter(date=date_time)
                serializer = FuelExpenseGetSerializer(inspection,many=True)                   
                # paginated_data = paginate(serializer.data,page_number,8)
                return Response(serializer.data)    

        except:
            return Response({'Error': 'No fuel expense  found', 'app_data': 'No such a fuel expense  added.'}, status=status.HTTP_400_BAD_REQUEST)


  #_____________________________Pre inspection Check______________________________#

  
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def getAllPreInspection(request,v_type,page_number=1):
    if request.method == 'GET':  
        try:
            
            if (v_type=='truck'):
                vehicle = PreInspectionCheck.objects.filter(vehicle__vehicle_type='truck',vehicle_type='truck').filter(active_status=True)         
                serializer = PreInspectionCheckGetSerializer(vehicle,many=True)        
                paginated_data = paginate(serializer.data,page_number,8)
                return Response(paginated_data)
            if (v_type=='fork-lift'):
                vehicle = PreInspectionCheck.objects.filter(vehicle__vehicle_type='fork-lift',vehicle_type='fork-lift').filter(active_status=True)         
                serializer = PreInspectionCheckGetSerializer(vehicle,many=True)                   
                paginated_data = paginate(serializer.data,page_number,8)
                return Response(paginated_data)
            if (v_type=='car'):
                vehicle = PreInspectionCheck.objects.filter(vehicle__vehicle_type='car',vehicle_type='car').filter(active_status=True)         
                serializer = PreInspectionCheckGetSerializer(vehicle,many=True)                   
                paginated_data = paginate(serializer.data,page_number,8)
                return Response(paginated_data)        
        except:
            return Response({'Error': 'No  pre-inspection added yet!', 'app_data': 'No Pre-inspection checks available!'}, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'POST':
        try:
            user = request.user
            employee = Employee.objects.get(user=user)
            try:
                request.data._mutable = True
            except:
                pass
            request.data.update({"driver_name": employee.id})
            request.data.update({"name": str(employee.name)})
            try:
                request.data._mutable = False
            except:
                pass
            serializer = PreInspectionCheckSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                team = Employee.objects.filter(user_type='manager',active_status=True)
                notification_hub_obj = Notification_hub.objects.create(type='added',model_type='pre_inspection',reference_id=serializer.data['id'])
                for employee in team:
                    notification_hub_obj.send_to_team.add(employee.id)             
                return Response({'Success': 'Pre-inspectionCheck Added','app_data': 'Pre-inspection check Added'}, status.HTTP_201_CREATED)
            else:
                return Response({'Error':serializer.errors,'app_data': 'Pre-inspection check adding failed'}, status=status.HTTP_400_BAD_REQUEST)    
        except Exception as E:
            return Response({'Error':str(E),'app_data': 'Pre-inspection check adding failed'}, status=status.HTTP_400_BAD_REQUEST)
@api_view(['PATCH','DELETE'])
@permission_classes([IsAuthenticated])
def PreInspectionEidt(request,check_id):
    if request.method == 'PATCH':
        try:  
            user = request.user
            employee = Employee.objects.get(user=user)
            try:
                request.data._mutable = True
            except:
                pass
            request.data.update({"driver_name": employee.id})
            request.data.update({"name": str(employee.name)})
            try:
                request.data._mutable = False
            except:
                pass
            insp = PreInspectionCheck.objects.get(id=check_id)
            serializer = PreInspectionCheckGetSerializer(insp, data=request.data, partial=True)   
            if serializer.is_valid():
                serializer.save()    
                team = Employee.objects.filter(user_type='manager',active_status=True)
                notification_hub_obj = Notification_hub.objects.create(type='edited',model_type='pre_inspection',reference_id=check_id)
                for employee in team:
                    notification_hub_obj.send_to_team.add(employee.id)               
                return Response(serializer.data)   
                
            else:
                return Response({'Error': serializer.errors, 'app_data': 'No inspection check data exists'}, status=status.HTTP_400_BAD_REQUEST)             
        except:
            return Response({'Error': 'No inspection exist', 'app_data': 'No inspection check exist'}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        try:  
            insp = PreInspectionCheck.objects.get(id=check_id)
            insp.active_status=False
            insp.save()       
            team = Employee.objects.filter(user_type='manager',active_status=True)
            notification_hub_obj = Notification_hub.objects.create(type='deleted',model_type='pre_inspection',reference_id=check_id)
            for employee in team:
                notification_hub_obj.send_to_team.add(employee.id)            
            return Response({'Success': 'Inspection check Deleted', 'app_data': 'Inspection check deleted sucessfully'})
        except:
            return Response({'Error': 'No Inspection check  found', 'app_data': 'No such a Inspection check added.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getPreInspectionById(request,v_type,check_id,page_number=1):
    if request.method == 'GET':
        try:
            if(v_type == 'truck'):
                inspection = PreInspectionCheck.objects.filter(vehicle__registration = check_id,vehicle__vehicle_type='truck').filter(active_status=True)
                serializer = PreInspectionCheckGetSerializer(inspection,many=True)                   
                paginated_data = paginate(serializer.data,page_number,8)
                return Response(paginated_data)
            if(v_type == 'fork-lift'):
                inspection = PreInspectionCheck.objects.filter(vehicle__registration = check_id).filter(active_status=True)
                serializer = PreInspectionCheckGetSerializer(inspection,many=True)                   
                paginated_data = paginate(serializer.data,page_number,8)
                return Response(paginated_data)    
            if(v_type == 'car'):
                inspection = PreInspectionCheck.objects.filter(vehicle__registration = check_id).filter(active_status=True)
                serializer = PreInspectionCheckGetSerializer(inspection,many=True)                   
                paginated_data = paginate(serializer.data,page_number,8)
                return Response(paginated_data)    

        except:
            return Response({'Error': 'No Inspection check  found', 'app_data': 'No such a Inspection check added.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def pre_ins_search_by(request,filter_type):
    if request.method == 'POST':
        v_type = request.POST['vehicle_type']

        try:
            if(filter_type == 'vehicle'):
                inspection = PreInspectionCheck.objects.filter(vehicle__registration= request.POST['registration']).filter(active_status=True,vehicle_type=v_type)
                serializer = PreInspectionCheckGetSerializer(inspection,many=True)                   
                # paginated_data = paginate(serializer.data,page_number,8)
                return Response(serializer.data)
            if(filter_type == 'day'):
                date_time = request.POST['date_time']
                year = date_time[:4]
                month = date_time[5:7]
                day = date_time[8:10]
                inspection = PreInspectionCheck.objects.filter(active_status=True,vehicle_type=v_type).filter(date_time__contains=datetime.date(int(year),int(month), int(day)))
                serializer = PreInspectionCheckGetSerializer(inspection,many=True)                   
                # paginated_data = paginate(serializer.data,pa  ge_number,8)
                return Response(serializer.data)    

        except:
            return Response({'Error': 'No Inspection check  found', 'app_data': 'No such a Inspection check added.'}, status=status.HTTP_400_BAD_REQUEST)

#____________________________Folders____________________________#

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def folders(request,vehicle_id=0):

    if request.method == 'POST':
        vehicle = Vehicle.objects.get(id=vehicle_id)
        try:
            request.data._mutable = True
        except:
            pass
        request.data.update({"vehicle": vehicle.id})
        try:
            request.data._mutable = False
        except:
            pass
        serializer = VehicleImagesSerializer(data=request.data)
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
                        for attachment in uploaded_files:  
                            file_upload_errors = {'error_status': False, 'error': 'No errors', 'dev_data': 'Files uploaded'}
                            new_serializer_object.attachments.create(file=attachment)


                        attachment_list =[]
                        base = "https://deep.envirowasteadmin.com.au/"
                        for attachment in new_serializer_object.attachments.all():
                               attachment_list.append({'id':attachment.id,'url':base + str(attachment.file.url),'name': os.path.basename(attachment.file.url)})
                                
                        return Response({'Success': 'files uploaded','app_data': attachment_list}, status.HTTP_201_CREATED)    

                except Exception as E:
                    file_upload_errors = {'error_status': True, 'error': 'Attachments upload was not successful', 'dev_data': str(E)}
            
            try:
                request.data._mutable = False
            except:
                pass
            

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def getVehicleFolders(request,vehicle_id=0):
    if request.method == 'GET':
        print("heloo")
        try:
            vehicle=Vehicle.objects.get(id=vehicle_id)
            folders = VehicleFolder.objects.all()
            data = []
            for folder in folders:
                obj = VehicleImages.objects.filter(vehicle=vehicle,folder=folder)
                serializer = VehicleImagesGetSerializer(obj,many=True)  
                in_dict = {'folder_id':folder.id, 'folder_name':folder.name,'files':serializer.data}
                data.append(in_dict)
                
            return Response(data)
        except Exception as E:
            return Response({'Error': str(E), 'app_data':'Something went wrong while fetching files'}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def vehicle_search(request,page_number=1):
    if request.method == 'POST':
        try:
                key = request.POST['key']
                types = request.POST['types']
                if key== ' ':
                    v_found=Vehicle.objects.filter(vehicle_type=types)
                    serializer = VehicleGetSerializer(v_found,many=True) 
                    paginate_data = paginate(serializer.data,page_number,8)
                    return Response(paginate_data, status=status.HTTP_200_OK)
                else:

                    v_found=Vehicle.objects.filter(Q(registration__istartswith=key)).filter(vehicle_type=types)
                    serializer = VehicleGetSerializer(v_found,many=True) 
                    paginate_data = paginate(serializer.data,page_number,8)
                    return Response(paginate_data, status=status.HTTP_200_OK)
                
        except:
            return Response({'Error': 'No vehicle present', 'app_data': 'No maches found'}, status=status.HTTP_400_BAD_REQUEST) 

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def get_all_VehicleFolders(request):
    if request.method == 'GET':
        try:
            folder = VehicleFolder.objects.all()  
            serializer = VehicleFolderGetSerializer(folder,many=True)                   
            return Response(serializer.data)                         
        except:
            return Response({'Error': 'No folder exist', 'app_data': 'No folder exist'}, status=status.HTTP_400_BAD_REQUEST)    
    

    
    if request.method == 'POST':
        try:
            serializer = VehicleFolderSerializer(data = request.data)  
            if serializer.is_valid():
                serializer.save()
                return Response({'Success': 'folder created','app_data': 'folder Created '}, status.HTTP_201_CREATED)                        
        except:
            return Response({'Error': 'Failed upload', 'app_data': 'upload failed '}, status=status.HTTP_400_BAD_REQUEST) 





@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_vehicle_files(request,file_id):
    if request.method == 'DELETE':   
        try:

            delete_file = PostImage.objects.get(id=file_id)
            delete_file.delete()

            return Response({'Success': 'File Deleted', 'app_data': 'File  deleted'})
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'file  error '}, status=status.HTTP_400_BAD_REQUEST)  

@api_view(['GET','DELETE','POST','PATCH'])
@permission_classes([IsAuthenticated])
def update_team_folder(request,f_type,f_id=0):
    if request.method == 'DELETE':
        try:
            if f_type =="folder":
                folders = VehicleFolder.objects.get(id =f_id)
                
                folders.delete()
            if f_type =="file":    
                file_obj = VehicleFile.objects.get(id=f_id)
                file_obj.delete()
            return Response({"app_data":'deleted','dev_data':'deleted succssefully'})

        except Exception as E:
            return Response({'Error': str(E), 'app_data':'Something went wrong while fetching files'}, status=status.HTTP_400_BAD_REQUEST) 
    if request.method == 'PATCH':
        try:
            if f_type =="folder":
                folders = VehicleFolder.objects.get(id =f_id)
                serializer = VehicleFolderGetSerializer(folders,data=request.data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
            if f_type =='file':
                file_obj = VehicleFile.objects.get(id=f_id)
                serializer = VehicleFileGetSerializer(file_obj,data=request.data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
        except Exception as E:
            return Response({'Error': str(E),'app_data':'Something went wrong while fetching files'}, status=status.HTTP_400_BAD_REQUEST)  
    if request.method == 'POST':
        try:
            if f_type=='folder':
                serializer = VehicleFolderSerializer(data=request.data)
            if f_type=='file': 
                serializer = VehicleFileSerializer(data=request.data)   
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        except Exception as E:
            return Response({'Error': str(E), 'app_data':'Something went wrong while fetching files'}, status=status.HTTP_400_BAD_REQUEST)            



@api_view(['POST','GET','DELETE'])
@permission_classes([IsAuthenticated])
def vehicle_multiple_images_update(request,vehicle_id=0):
    # emp = Employee.objects.get(user=request.user)
    if request.method == 'POST':
            
        try:
            try:
                vehicle_obj = Vehicle.objects.get(id=vehicle_id)
            except:
                return Response({"Error":'No schedule exist in this id','app_data': 'Schedule fetching failed'},status=status.HTTP_400_BAD_REQUEST)    
            try:
                request.POST._mutable = True
            except:
                pass
            if 'images' in request.data:
                for i in vehicle_obj.images.all():
                    vehicle_obj.images.remove(i)
                file_attachment_list = []
                uploaded_files = request.data.pop('images')
                print(uploaded_files)
                if not uploaded_files == ['']:
                    for attachment in uploaded_files:  
                        print("atta",attachment)
                        file_obj =VehicleImage.objects.create(image_file=attachment)
                        file_attachment_list.append(file_obj)
                print(file_attachment_list) 
                new_vehicle_list = []
                existing_vehicle_list = []
                for i in file_attachment_list:
                    print(i)
                    add_images = vehicle_obj.images.add(i)    
                    
            try:
                request.POST._mutable = False
            except:
                pass 
            else:
                for i in vehicle_obj.images.all():
                    vehicle_obj.images.remove(i)

            if 'existing_images' in request.data:
                for i in request.POST.getlist('existing_images'):
                            obj = vehicle_obj.images.add(VehicleImage.objects.get(id=i))
                            vehicle_obj.save(obj)

               
                
            return Response ({'app_data':"updated images successfully",'dev_data':'updated images successfully'})    
        except Exception as E:
            return Response({"Error":str(E),"dev_data":'something went wrong'},status=status.HTTP_400_BAD_REQUEST)
