from functools import partial
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


from accounts.models import Client,Employee,SiteDetails
from .serializers import (ClientSerializer, 
ClientGetSerializer,ClientImagesSerializer,
ClientImagesGetSerializer,ClientFolderSerializer,
ClientFolderGetSerializer,SiteDetailSerializer)      
from django.db.models import Q
from .models import ClientImages,PostImage,ClientFolder
from notification.models import Notification_hub
from accounts.models import PushNotification
from accounts.general import push_notifier
from vehicles.general import paginate

# from Enviro.clients import serializers



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getClientAPI(request, client_id):
    if request.method == 'GET':

        try:  
            client = Client.objects.get(id=client_id)        
            serializer = ClientGetSerializer(client,many=False)   
            # use = User.objects.get(username=client.user)  
                 
            return Response(serializer.data)
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'No such a Client found '}, status=status.HTTP_400_BAD_REQUEST)    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def clientGetAllAPI(request,tab_type="waste"):
    if request.method == 'GET':
        try:  
            if tab_type =="all":
                client = Client.objects.filter(active_status=True,client_type ="Permenant")
            else:    
                client = Client.objects.filter(active_status=True,client_type ="Permenant",tab_type=tab_type)          
            serializer = ClientGetSerializer(client,many=True)                   
            return Response(serializer.data)
        except Exception as E:
            return Response({'Error':str(E), 'app_data': 'No such Client found '}, status=status.HTTP_400_BAD_REQUEST)    

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def clientDeleteAPI(request, client_id,tab_type="waste"):
    if request.method == 'DELETE':
        try:  
            client = Client.objects.get(id=client_id)
            client.active_status=False
            client.save()    
            team = Employee.objects.filter(user_type='manager',tab_type=tab_type)
            notification_hub_obj = Notification_hub.objects.create(type='deleted',model_type='client',reference_id=client.id)
            for employee in team:
                notification_hub_obj.send_to_team.add(employee.id) 
         
            return Response({'Success': 'Client Deleted', 'app_data': 'Client deleted suucessfully'})
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'No such Client found '}, status=status.HTTP_400_BAD_REQUEST)    


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def clientEditAPI(request,client_id):
    if request.method == 'PATCH':
        try:
            client = Client.objects.get(id=client_id)
            serializer = ClientSerializer(client, data=request.data,partial=True)   
            if serializer.is_valid():
                serializer.save()   
                return Response(serializer.data)    
            else:
                return Response({"Error":serializer.errors, 'app_data': 'No such Client found '}, status=status.HTTP_400_BAD_REQUEST)


            # team = Employee.objects.filter(user_type='manager')
            # notification_hub_obj = Notification_hub.objects.create(type='edited',model_type='client',reference_id=client.id)
            # for employee in team:
            #     notification_hub_obj.send_to_team.add(employee.id) 
                     
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'No such Client found '}, status=status.HTTP_400_BAD_REQUEST)    



@api_view(['POST'])
def createClientAPI(request):
    if request.method == 'POST':
        try: 
            serializer = ClientSerializer(data=request.data)

            if serializer.is_valid():
                client_obj  = serializer.save()
                team = Employee.objects.filter(user_type='manager')
                notification_hub_obj = Notification_hub.objects.create(type='added',model_type='client',reference_id=client_obj.id)
                for employee in team:
                    notification_hub_obj.send_to_team.add(employee.id)
                return Response({'Success': 'Client Created','app_data': 'Client Created '}, status.HTTP_201_CREATED)   
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as E:
            return Response({'Error': str(E),'app_data': 'Error Creating Client '}, status=status.HTTP_400_BAD_REQUEST) 

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def searchClient(request,tab_type ="waste"):
    if request.method == 'POST':
        try:
            key = request.POST['key']
            if(key == ' '):
                client_found = Client.objects.filter(active_status = True,tab_type=tab_type,client_type="Permenant")
                serializer = ClientGetSerializer(client_found,many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:

                client_found=Client.objects.filter(client_name__istartswith=key).filter(active_status=True,tab_type=tab_type,client_type="Permenant")
                serializer = ClientGetSerializer(client_found,many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'No maches found'}, status=status.HTTP_400_BAD_REQUEST) 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sortedClientList(request,sort_by,tab_type="waste"):
    if request.method == 'GET':

        try:  
            if('alpha_asc' == sort_by):
                try:
                    client = Client.objects.filter(active_status=True,client_type ="Permenant",tab_type=tab_type).order_by('client_name')     
                    serializer = ClientGetSerializer(client,many=True)  
                    return Response(serializer.data)
                except Exception as E:
                    return Response({'Error': str(E), 'app_data': 'invalid_client_name'}, status=status.HTTP_400_BAD_REQUEST)

            if('alpha_dsc' == sort_by):
                try:
                    client = Client.objects.filter(active_status=True,client_type ="Permenant",tab_type=tab_type).order_by('-client_name')     
                    serializer = ClientGetSerializer(client,many=True)  
                    return Response(serializer.data)
                except Exception as E:
                    return Response({'Error': str(E), 'app_data': 'invalid client_name'}, status=status.HTTP_400_BAD_REQUEST)

            if('date_asc' == sort_by):
                try:
                    client = Client.objects.filter(active_status=True,client_type ="Permenant",tab_type=tab_type).order_by('date_joined')
                    serializer = ClientGetSerializer(client,many=True)  
                    return Response(serializer.data)
                except Exception as E:
                    return Response({'Error': str(E), 'app_data': 'invalid date'}, status=status.HTTP_400_BAD_REQUEST) 
            
            if('date_dsc' == sort_by):
                try:
                    client = Client.objects.filter(active_status=True,client_type ="Permenant",tab_type=tab_type).order_by('-date_joined')     
                    serializer = ClientGetSerializer(client,many=True)  
                    return Response(serializer.data)
                except Exception as E:
                    return Response({'Error': str(E), 'app_data': 'invalid date'}, status=status.HTTP_400_BAD_REQUEST)                       
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'No such Client found '}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def emailIdAvailability(request):
    try: 
        if (Client.objects.filter(client_email = request.POST['email']).exists()):
            return Response({'app_data': 'Email is already exist'}, status=status.HTTP_200_OK)
    except Exception as E:
        return Response({'Error': str(E)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def clientIdAvailability(request):
    try: 
        if (Client.objects.filter(id = request.POST['client_id']).exists()):
            return Response({'Error': 'Client Id is already exist', 'app_data': 'Client Id is already exist'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'Success': 'Client Id not exists', 'app_data': 'Valid Client Id'})    
    except Exception as E:
        return Response({'Error': str(E)}, status=status.HTTP_400_BAD_REQUEST)

#_________________________________folders__________________________#

@api_view(['POST','GET'])
@permission_classes([IsAuthenticated])
def files_list(request,client_id=0):
    if request.method == 'POST':
        try:
            client = Client.objects.get(id=client_id)
            try:
                request.data._mutable = True
            except:
                pass
            request.data.update({"client": client.id})
            try:
                request.data._mutable = False
            except:
                pass
            serializer = ClientImagesSerializer(data=request.data)
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
                                file_upload_errors = {'error_status': False, 'error': 'No errors', 'dev_data': 'Fsiles uploaded'}
                                new_serializer_object.attachments.create(file=attachment)
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
                        return Response({'error_status': True, 'error': 'Attachments upload was not successful', 'dev_data': str(E)})
        except Exception as E:
                        return Response({'error_status': True, 'error': 'Attachments upload was not successful', 'dev_data': str(E)})
                
    if request.method =='GET':
        try:
            
            folders = ClientFolder.objects.all()
            client =Client.objects.get(id=client_id)
            data = []
            for folder in folders:
                obj = ClientImages.objects.filter(client=client,folder=folder)
                serializer = ClientImagesGetSerializer(obj,many=True)  
                in_dict = {'folder_id':folder.id,'folder_name':folder.name, 'files':serializer.data}
                data.append(in_dict)

           

            return Response(data)
        except Exception as E:
            return Response ({'Error':str(E),'app_data': 'No folder exist'}, status=status.HTTP_400_BAD_REQUEST)  
            
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def get_all_ClientFolders(request):
    if request.method == 'GET':
        try:
            folder = ClientFolder.objects.all()  
            serializer = ClientFolderGetSerializer(folder,many=True)                   
            return Response(serializer.data)                         
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'No folder exist'}, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'POST':
        try:
            serializer = ClientFolderSerializer(data = request.data)  
            if serializer.is_valid():
                serializer.save()
                return Response({'Success': 'folder created','app_data': 'folder Created '}, status.HTTP_201_CREATED)                        
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'upload failed '}, status=status.HTTP_400_BAD_REQUEST) 



#temporary client

@api_view(['GET','POST','PATCH','DELETE'])
@permission_classes([IsAuthenticated])
def temporary_client(request, client_id=0):
    if request.method == 'GET':

        try:  
            client = Client.objects.filter(client_type ="Temporary").filter(id=client_id)      
            serializer = ClientGetSerializer(client,many=False)       
            return Response(serializer.data)
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'No such a Client found '}, status=status.HTTP_400_BAD_REQUEST)    
      
    if request.method == 'DELETE':
        try:  
            client = Client.objects.get(id=client_id)
            client.active_status=False
            client.save()               
            return Response({'Success': 'Client Deleted', 'app_data': 'Client deleted suucessfully'})
        except:
            return Response({'Error': 'No such Client found', 'app_data': 'No such Client found '}, status=status.HTTP_400_BAD_REQUEST)    

    if request.method == 'PATCH':
        try:  
            client = Client.objects.get(id=client_id)
            serializer = ClientGetSerializer(client, data=request.data, partial=True)   
            if serializer.is_valid():
                serializer.save()                
            return Response(serializer.data)            
        except:
            return Response({'Error': 'No such Client found', 'app_data': 'No such Client found '}, status=status.HTTP_400_BAD_REQUEST)    

    if request.method == 'POST':

        try:
            try:
                request.data._mutable = True
            except:
                pass
            request.data.update({"client_type": "Temporary"})
            try:
                request.data._mutable = False
            except:
                pass
            serializer = ClientSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'Success': 'Client Created','app_data': 'Client Created '}, status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as E:
            return Response({'Error':str(E),'app_data': 'Error Creating Client '}, status=status.HTTP_400_BAD_REQUEST) 


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getAllTemporary_client(request,order_by="alpha_asc",tab_type="waste"):
    if request.method == 'GET':
        try:
            if order_by == "alpha_asc":
                clients=Client.objects.filter(active_status=True,client_type = "Temporary").order_by('client_name') 
                print(clients)
            if order_by == "alpha_dsc":
                clients=Client.objects.filter(active_status=True,client_type = "Temporary").order_by('-client_name')   
            if order_by == "date_dsc":
                clients=Client.objects.filter(active_status=True,client_type = "Temporary").order_by('date_joined')    
            if order_by == "date_asc":
                clients=Client.objects.filter(active_status=True,client_type = "Temporary").order_by('date_joined')         
            if tab_type  == 'all':
                client = clients.filter(active_status=True,client_type = "Temporary")  
            else:
                client = clients.filter(tab_type=tab_type)
          
      

            serializer = ClientGetSerializer(client,many=True)                   
            return Response(serializer.data)
        except:
            return Response({'Error': 'No such Client found', 'app_data': 'No such Client found '}, status=status.HTTP_400_BAD_REQUEST)    

            

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def searchTemporary_client(request,tab_type='waste'):
    if request.method == 'POST':
        try:
            key = request.POST['key']
            if(key == ' '):
                client_found = Client.objects.filter(active_status = True,client_type = "Temporary",tab_type=tab_type)
                serializer = ClientGetSerializer(client_found,many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                client_found=Client.objects.filter(client_name__istartswith=key).filter(active_status=True,client_type = "Temporary",tab_type=tab_type)
                serializer = ClientGetSerializer(client_found,many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'Error': 'No item present', 'app_data': 'No maches found'}, status=status.HTTP_400_BAD_REQUEST) 

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sortedTemporaryClientList(request,sort_by,tab_type="waste"):
    if request.method == 'GET':
        try:  
            if('alpha_asc' == sort_by):
                try:
                    client = Client.objects.filter(active_status=True,client_type = "Temporary").order_by('client_name')     
                    serializer = ClientGetSerializer(client,many=True)  
                    return Response(serializer.data)
                except:
                    return Response({'Error': 'No such a client found', 'app_data': 'invalid_client_name'}, status=status.HTTP_400_BAD_REQUEST)

            if('alpha_dsc' == sort_by):
                try:
                    client = Client.objects.filter(active_status=True,client_type = "Temporary").order_by('-client_name')     
                    serializer = ClientGetSerializer(client,many=True)  
                    return Response(serializer.data)
                except:
                    return Response({'Error': 'No such a client found', 'app_data': 'invalid client_name'}, status=status.HTTP_400_BAD_REQUEST)

            if('date_asc' == sort_by):
                try:
                    client = Client.objects.filter(active_status=True,client_type = "Temporary").order_by('date_joined')
                    serializer = ClientGetSerializer(client,many=True)  
                    return Response(serializer.data)
                except:
                    return Response({'Error': 'No such a client found', 'app_data': 'invalid date'}, status=status.HTTP_400_BAD_REQUEST) 
            
            if('date_dsc' == sort_by):
                try:
                    client = Client.objects.filter(active_status=True,client_type = "Temporary").order_by('-date_joined')     
                    serializer = ClientGetSerializer(client,many=True)  
                    return Response(serializer.data)
                except:
                    return Response({'Error': 'No such a client found', 'app_data': 'invalid date'}, status=status.HTTP_400_BAD_REQUEST)                       
        except:
            return Response({'Error': 'No such Client found', 'app_data': 'No such Client found '}, status=status.HTTP_400_BAD_REQUEST)



# client single file delete

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_client_files(request,file_id):
    if request.method == 'DELETE':   
        try:

            delete_file = PostImage.objects.get(id=file_id)
            delete_file.delete()

            return Response({'Success': 'File Deleted', 'app_data': 'File  deleted'})
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'file  error '}, status=status.HTTP_400_BAD_REQUEST)    

@api_view(['POST',"GET","DELETE","PUT"])
@permission_classes([IsAuthenticated])
def Site_details(request, sited_id=''):
    if request.method == 'POST':
        try:
            serializer = SiteDetailSerializer(data=request.data)   
            if serializer.is_valid():
                serializer.save()    
                return Response({"app_data":"attachement added",'dev_data':"added"})   
               
            else:
                return Response({'Error': serializer.errors, 'app_data': 'somethig went wrong'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'somethig went wrong'}, status=status.HTTP_400_BAD_REQUEST) 
    if request.method == 'GET':
        try:
            page = int(request.GET['page'])
        except Exception as E:
            print(E)
            page = 1
            
        # looking for limit 
        try:
            limit = int(request.GET['limit'])
        except Exception as E:
            
            limit = 10

            # if there is a search key seach should work else usual view should work
        try:
            site = Client.objects.get(id = int(sited_id))
            sited_obj =SiteDetails.objects.filter(active_status=True,site_details=site)
            serializer = SiteDetailSerializer(sited_obj,many=True)    
            result = paginate(serializer.data, page, limit)
            return Response(result)            
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'somethig went wrong'}, status=status.HTTP_400_BAD_REQUEST) 
    if request.method == 'PUT':
        try:
            sited_obj =SiteDetails.objects.get(active_status=True,id=int(sited_id))
            serializer = SiteDetailSerializer(sited_obj,data=request.data)    
            if serializer.is_valid():
                serializer.save()    
                return Response(serializer.data) 
            else:
                return Response({'Error': serializer.errors, 'app_data': 'somethig went wrong'}, status=status.HTTP_400_BAD_REQUEST)
                      
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'somethig went wrong'}, status=status.HTTP_400_BAD_REQUEST)        
    if request.method == 'DELETE':
        try:
            sited_obj =SiteDetails.objects.get(active_status=True,id=sited_id)
            sited_obj.active_status = False
            sited_obj.save()
            return Response({'app_data':"site detaile delelted","dev_data":'Deleted'} )

        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'somethig went wrong'}, status=status.HTTP_400_BAD_REQUEST)                     