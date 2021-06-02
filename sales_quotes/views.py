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
from django.contrib.auth.models import User
from archive_intranets.models import IntranetArchiveFiles,IntranetArchiveFolders,IntranetFolderFiles,IntranetFolders
from accounts.models import Client
from .models import (
    Quote,SalesFolderFiles,SalesFolders,EmailBcc,EmailCc,Products,UserQuoteTemplate,
    TemplateDraft,UserSafetyData,MailSignature,QuoteAttachTemplates,TypeOfWaste,
    LoggingInfo,ClientQuoteAttachmentResponses
)

from .serializer import(
    QuoteGetSerializer,JobGetSerializer,JobDetailsGetSerializer,
    JobImagesGetSerializer,JobImagesSerializer,DummyTemplateGetSerializer,
    ProductsGetSerializer,ProductsSerializer,UserQuoteTemplateGetSerializer,
    SingleUserQuoteTemplateGetSerializer,TemplateDraftGetSerializer,
    TemplateDraftSerializer,SingleTemplateDraftSerializer,SingleUserSafetyDataGetSerializer,UserSafetyDataGetSerializer,QuoteAttachTemplatesGetSerializer,
    TemplateDraftGetAllSerializer,TypeOfWasteGetSerializer,TypeOfWasteSerializer,
    LoggingInfoGetSerializer,LoggingInfoSerializer,ClientQuoteAttachmentResponsesGetSerializer

)
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from accounts.models import Employee
from datetime import datetime
from vehicles.general import paginate
from clients.serializers import ClientImagesGetSerializer
from team.serializers import EmployeeGetSerializer
from schedules.models import Schedule
from clients.models import ClientImages
from .permissions import quote_permissions
import uuid
import pdfkit
from jobs.models import Job,JobcardInfo
from drive.models import DriveFolder,Files
from django.db.models import Avg, Max, Min, Sum
from django.db import models
from notification.models import Notification_hub
from django.views.decorators.csrf import csrf_exempt
from django.db.models import IntegerField
from django.db.models.functions import Cast
from django.template.loader import render_to_string, get_template
from clients.serializers import ClientGetSerializer
from accounts.general import push_notifier,push_notifier_accounts_team,push_notifier_for_team

from schedules.models import AdditionalVehicles
from drive.models import DriveFolder
from drive.serializers import DriveFolderSerializer
from oh_and_s.models import Notification,NotificationMembers
from oh_and_s.serializers import NotificationSerializer
from oh_and_s.models import Notification
 
@api_view(['GET','POST']) 
def client_quote_status(request,status,quote_id):
    if request.method == 'GET':
            
            if status  == 'accepted':
                try:
                    quote_obj = Quote.objects.get(uuid=quote_id)
                
                    if quote_obj.status =='accepted':
                    
                        return Response({'message':'Requested quote already in accepted status','status':400})
                    quote_obj.status = 'accepted'
                    quote_obj.won_reject_date = datetime.now()
                    quote_obj.save()
                    temp_client_to_Permenant_client = Client.objects.filter(id=quote_obj.client.id).update(client_type="Permenant")
                    try:
                        job_exist = Job.objects.filter(quote=quote_obj)
                    except:
                        job_obj =Job.objects.create(tab_type=quote_obj.tab_type,created_by=quote_obj.employee,client=quote_obj.client,quote=quote_obj,amount=quote_obj.amount,paid_amount='0',reoccurring=quote_obj.reoccurring,status='accepted',schedule_status=False,job_type=quote_obj.job_type)
                    
                    try:
                        team_list = Employee.objects.filter(Q(user_type ="manager") | Q(user_type="sales-staff"))

                        push_notifier_for_team("Quote alert" ,"Quote accepted by " + str(quote_obj.client.client_name),team_list)
                        # user = Employee.objects.get(user=request.user)
                   
                            
                            # request.data['created_by']=user.id
                        title="quote status approved"
                        description= "qoute approved by client"

                        notification_obj = Notification.objects.create(title = title,description=description) 
                        
                        managers  = Employee.objects.filter(Q(user_type = "manager") | Q (user_type = "sales-staff"))
                        for member in managers:
                            notification_obj.members.create(member_id=member)
                    except Exception as E:
                        print(str(E))
                        pass
                    team = Employee.objects.filter(user_type='manager')
                    notification_hub_obj = Notification_hub.objects.create(type='accepted',model_type='quote',reference_id=quote_obj.id)
                    for employee in team:
                        notification_hub_obj.send_to_team.add(employee.id)
                    return Response({'message': 'Quote status accepted','status':200})
                except:
                    return Response({'message':"Quote does not exists",'status':400})
        
            if status  == 'rejected':
                try:
                        quote_obj = Quote.objects.get(uuid=quote_id)
                        if quote_obj.status =='rejected':
                
                            return Response({'message':'Requested quote already in rejected status','status':400})
                                
                        quote_obj.status = 'rejected'
                        quote_obj.won_reject_date = datetime.now()
                        quote_obj.save()
                        try:
                            job_obj = Job.objects.get(quote=quote_obj)
                            job_obj.status ='rejected'
                            job_obj.schedule_status =False
                            job_obj.ready_for_schedule =False
                            job_obj.save()
                        except:
                            pass
                        try:
                            team_list = Employee.objects.filter(Q(user_type ="manager") | Q(user_type="sales-staff"))
                            push_notifier_accounts_team("Quote alert", "Quote rejected by " + str(quote_obj.client.client_name),team_list)
                            # user = Employee.objects.get(user=request.user)
                    
                            title="quote status rejected"
                            description= "qoute rejected by client"
                            notification_obj = Notification.objects.create(title = title,description=description) 
                    
                            managers  = Employee.objects.filter(Q(user_type = "manager") | Q (user_type = "sales-staff"))
                            for member in managers:
                                notification_obj.members.create(member_id=member)
                        except Exception as E:
                            print(str(E))
                            pass
                        team = Employee.objects.filter(user_type='manager')
                        notification_hub_obj = Notification_hub.objects.create(type='rejected',model_type='quote',reference_id=quote_obj.id)
                        for employee in team:
                            notification_hub_obj.send_to_team.add(employee.id)
                        return Response({'message': 'Quote status rejected','status':200}) 
                except:
                    return Response({'message':'Quote does not exists','status':400})

    # this api was previously get method, now I am (Ejas) is adding a post method for client to fill the template
    if request.method == 'POST':
        if status  == 'accepted':
                try:   
                    quote_obj = Quote.objects.get(uuid=quote_id)

                    if quote_obj.status =='accepted':
                        return Response({'message':'Requested quote already in accepted status','status':400})

                    quote_obj.status = 'accepted'

                    try:
                        template=request.POST['template']
                        quote_obj.template_html_receive = template
                        file_name ='quote_file_' +str(uuid.uuid4()) + '.pdf'
                        options={'page-size':'A4', 'dpi':400, 'disable-smart-shrinking': ''}
                        a =pdfkit.from_string(template,file_name, options=options)
                        file =open(file_name)
                        Path(file_name).rename("media/quote/archive/"+file_name)
                        quote_obj.template_receive = "/quote/archive/"+file_name
                    
                    except:
                        pass
                    quote_obj.won_reject_date = datetime.now()
                    quote_obj.save()
                    try:
                        message =str(emp.name) + "Accepted a quote"
                        LoggingInfo.objects.create(message=message,quote=quote_obj)
                    except:
                        pass    
                    temp_client_to_Permenant_client = Client.objects.filter(id=quote_obj.client.id).update(client_type="Permenant")
                    if Job.objects.filter(quote=quote_obj).count() ==0:
                        job_obj =Job.objects.create(tab_type=quote_obj.tab_type,created_by=quote_obj.employee,client=quote_obj.client,quote=quote_obj,amount=quote_obj.amount,paid_amount='0',reoccurring=quote_obj.reoccurring,status='accepted',schedule_status=False,job_type=quote_obj.job_type)
                    else:
                        pass
                    try:
                        team_list = Employee.objects.filter(Q(user_type ="manager") | Q(user_type="sales-staff"))
                        push_notifier_accounts_team("Quote alert","Quote accepted by " + str(quote_obj.client.client_name ),team_list)
                        # user = Employee.objects.get(user=request.user)
                        
                        title="quote status approved"
                        description = "qoute approved by client"
                        notification_obj = Notification.objects.create(title = title,description=description)

                        managers  = Employee.objects.filter(Q(user_type = "manager") | Q (user_type = "sales-staff"))
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
                    notification_hub_obj = Notification_hub.objects.create(type='accepted',model_type='quote',reference_id=quote_obj.id)
                    for employee in team:
                        notification_hub_obj.send_to_team.add(employee.id)
                    return Response({'message': 'Quote status accepted','status':200})    

                except:
                    return Response({'message':"Quote does not exists",'status':400})

        elif status  == 'rejected':
                try:
                        quote_obj = Quote.objects.get(uuid=quote_id)
                        if quote_obj.status =='rejected':
                
                            return Response({'message':'Requested quote already in rejected status','status':400})
                                
                        quote_obj.status = 'rejected'
                        quote_obj.won_reject_date = datetime.now()
                        quote_obj.save()
                        team = Employee.objects.filter(user_type='manager')
                        try:
                            team_list = Employee.objects.filter(Q(user_type ="manager") | Q(user_type="sales-staff"))
                            push_notifier_accounts_team("Quote alert","Quote Rejected by " + str(quote_obj.client.client_name ),team_list)
                            # user = Employee.objects.get(user=request.user)
                            
                            title="quote status rejected"
                            description = "qoute rejected by client"
                            notification_obj = Notification.objects.create(title = title,description=description)
                        
                            managers  = Employee.objects.filter(Q(user_type = "manager") | Q (user_type = "sales-staff"))
                            for member in managers:
                                notification_obj.members.create(member_id=member)
                         
                        except Exception as E:
                            print(str(E))
                            pass
                        notification_hub_obj = Notification_hub.objects.create(type='rejected',model_type='quote',reference_id=quote_obj.id)
                        for employee in team:
                            notification_hub_obj.send_to_team.add(employee.id)
                        return Response({'message': 'Quote status rejected','status':200}) 
                except:
                    return Response({'message':'Quote does not exists','status':400})

@api_view(['GET','POST']) 
def quote_status_change(request,status_change,quote_id):
    if request.method == 'GET':
        
            if status_change  == 'accepted':
                try:
                        
                        quote_obj = Quote.objects.get(id=quote_id)
                        if quote_obj.status =='accepted':
                            return Response({'app_data':'Requested quote already in accepted status'},status=status.HTTP_400_BAD_REQUEST)
                        quote_obj.status = 'accepted'
                        quote_obj.won_reject_date = datetime.now()
                        quote_obj.save()
                        temp_client_to_Permenant_client = Client.objects.filter(id=quote_obj.client.id).update(client_type="Permenant")
                        if Job.objects.filter(quote=quote_obj).count()==0:
                            job_obj =Job.objects.create(tab_type=quote_obj.tab_type,created_by=quote_obj.employee,client=quote_obj.client,quote=quote_obj,amount=quote_obj.amount,paid_amount='0',reoccurring=quote_obj.reoccurring,status='accepted',schedule_status=False,job_type=quote_obj.job_type)
                        else:
                            pass
                           
                        try:
                            team_list = Employee.objects.filter(Q(user_type ="manager") | Q(user_type="sales-staff"))
                            push_notifier_accounts_team("Quote status changed","Quote accepted by " + str(quote_obj.client.client_name),team_list)
                            # user = Employee.objects.get(user=request.user)
                            
                            title="quote status accepted"
                            description= "qoute accepted by client"
                            notification_obj = Notification.objects.create(title = title,description=description)
                        
                            managers  = Employee.objects.filter(Q(user_type = "manager") | Q (user_type = "sales-staff"))
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
                        notification_hub_obj = Notification_hub.objects.create(type='accepted',model_type='quote',reference_id=quote_obj.id)
                        for employee in team:
                            notification_hub_obj.send_to_team.add(employee.id)
                        return Response({'app_data': 'Quote status accepted'},status=status.HTTP_200_OK)
                except:
                    return Response({'app_data':"Quote does not exists"},status=status.HTTP_400_BAD_REQUEST)
        
            if status_change  == 'rejected':
                try:
                        quote_obj = Quote.objects.get(id=quote_id)
                        if quote_obj.status =='rejected':
                
                            return Response({'app_data':'Requested quote already in rejected status'},status=status.HTTP_400_BAD_REQUEST)
                        if Schedule.objects.filter(job__quote=quote_obj).exists():
                            return Response({'app_data':'Requsted quote is in scheduled state'},status=status.HTTP_400_BAD_REQUEST)

                        quote_obj.status = 'rejected'
                        quote_obj.won_reject_date = datetime.now()
                        quote_obj.save()
                        try:
                            job_obj = Job.objects.get(quote=quote_obj)
                            job_obj.status ='rejected'
                            job_obj.schedule_status =False
                            job_obj.ready_for_schedule =False
                            job_obj.save()
                        except:
                            pass


                        try:
                            team_list = Employee.objects.filter(Q(user_type ="manager") | Q(user_type="sales-staff"))
                            push_notifier_accounts_team("Quote status changed","Quote rejected by " + str(quote_obj.client.client_name),team_list)
                     
                            title="quote status rejected"
                            description = "qoute rejected by client"
                            notification_obj = Notification.objects.create(title = title,description=description)    
                            managers  = Employee.objects.filter(Q(user_type = "manager") | Q (user_type = "sales-staff"))
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
                        notification_hub_obj = Notification_hub.objects.create(type='rejected',model_type='quote',reference_id=quote_obj.id)
                        for employee in team:
                            notification_hub_obj.send_to_team.add(employee.id)
                        return Response({'app_data': 'Quote status rejected'},status=status.HTTP_200_OK) 
                except:
                    return Response({'app_data':'Quote does not exists'},status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET']) 
def client_view_quote(request,quote_id):
    if request.method == 'GET':
        try:
            # works with both uuid and id
            
            quote_only = False
            try:
                uuid.UUID(quote_id)
                q = Quote.objects.get(uuid=quote_id)
                quote_only = True
            except:
                q = Quote.objects.get(id=int(quote_id))
                

            quote_data = {}
            job_data = {}
            schedule_data = {}
            data = {}
            attached_files = []
            response_template = []
            try:
                if quote_only:
                    clients_response = ClientQuoteAttachmentResponses.objects.filter(quote_data__uuid=q.uuid)
                else:
                    clients_response = ClientQuoteAttachmentResponses.objects.filter(quote_data__id=q.id)

                serializer = ClientQuoteAttachmentResponsesGetSerializer(clients_response,many=True)
                response_template.append(serializer.data)
            except:
                pass    
                


            for obj in q.quote_attach_files_in.all():
                attached_files.append({
                    'id':obj.id,
                    'url':obj.file.url,
                    'type': (obj.file.url).split('.')[-1],
                    'name': os.path.basename(obj.file.url),
                    'template_html': obj.template_html

                })
            quote_data = {
                'id': q.id,
                'sales_team_review': q.sales_team_review,
                'client': {
                    'id': q.client.id,
                    'name': q.client.client_name,
                    'type': q.client.client_type,
                    
                },
                'template': q.template_html_send,
                'template_receive': q.template_html_receive,
                'template_response':serializer.data,
                'quote_file':  q.template.url if q.template else '',
                'received_file':  q.template_receive.url if q.template_receive else '',
                'created_on': q.created_date_time.strftime('%d-%m-%Y %H:%M:%S'),
                'reoccurring': q.reoccurring,
                'status': q.status,
                'tab_type': q.tab_type,
                'created_by': {
                    'name': q.employee.name,
                    'dp': q.employee.dp.url if q.employee.dp else '',
                    'user_type': q.employee.user_type,
                    'contact_number': q.employee.contact_number
                },
                'invoice_amount': q.amount,
                'attached_files': attached_files
            }

            if quote_only == True:
                return Response({'data': quote_data,'status':200}) 

            try:
                job = Job.objects.get(quote=q)
                job_data = {
                    'id':job.id,
                    'created_on':job.created_date_time.strftime('%d-%m-%Y %H:%M:%S'),
                    'type': job.job_type,
                    'tab_type': job.tab_type,
                    'schedule_status': job.schedule_status,
                    'error': False
                }
            except Exception as E:
                job_data = {
                    'id':'',
                    'created_on':'',
                    'type': '',
                    'tab_type': '',
                    'schedule_status': '',
                    'error': True,
                    'dev':str(E),
                }
            
            try:
                sc = Schedule.objects.get(job=job)
                team_data = []
                try:
                    for member in sc.team_employees.all():
                        team_data.append({
                            'id':member.id,
                            'member_id':member.employee_id,
                            'name':member.name,
                            'designation': member.user_type,
                            'dp': member.dp.url if member.dp else ''
                        })
                except:
                    pass
                
                comments_data = []
                try:
                    for comment in sc.comments.all():
                        comments_data.append({
                            'id': comment.id,
                            'comment': comment.comment,
                            'employee': comment.employee.name,
                            'employee_dp': comment.employee.dp.url if comment.employee.dp else '',
                            'employee_designation': comment.employee.user_type
                        })
                except:
                    pass
                
                images_data = []
                try:
                    for image in sc.gallery.all():
                        images_data.append({
                            'image': image.file.url
                        })
                except:
                    pass
                try:
                    vehicle_data =[]
                    additional_vehicle_obj = AdditionalVehicles.objects.get(schedule=sc)
                    for vehicle in additional_vehicle_obj.vehicles.all():
                        vehicle_data.append({
                            'id':vehicle.id,
                            'registration':vehicle.registration,
                            'type':vehicle.types,
                            'image': vehicle.image1.url,
                            
                        })
                except Exception as E:
                    return Response ({"Error":str(E)})
                    vehicle_data =[]
                    pass

                schedule_data = {
                    'id': sc.id,
                    'status': sc.status,
                    'start_date': sc.start_date,
                    'start_time': sc.start_time,
                    'end_date': sc.end_date,
                    'end_time': sc.end_time,
                    'additional_vehicle':vehicle_data,
                    'vehicle': {
                        'id': sc.vehicle.id if sc.vehicle else '',
                        'registration': sc.vehicle.registration,
                        'type': sc.vehicle.vehicle_type,
                        'image': sc.vehicle.image1.url if sc.vehicle.image1 else ''
                    },
                    'team':team_data,
                    'comments': comments_data,
                    'gallery': images_data,
                    'error':False
                }
            except Exception as E:
                schedule_data = {
                    'id': '',
                    'status': '',
                    'start_date': '',
                    'start_time': '',
                    'end_date': '',
                    'end_time': '',
                    'vehicle': {
                        'id': '',
                        'registration': '',
                        'type': ''
                    },
                    'team':[],
                    'comments': [],
                    'images': [],
                    'error':True,
                    'dev_data':str(E)
                }
            data = {
                'quote':quote_data,
                'job':job_data,
                'schedule':schedule_data
            }
            return Response({'data': data,'status':200})    
        except Exception as E:
            return Response({'message':"Quote does not exists",'dev_data':str(E), 'status':400})
        
            
#end sales



#to reduce line of codes

@api_view(['POST','GET'])         
@permission_classes([IsAuthenticated])
def send_quote(request,tab_type,page =1):
    if request.method == 'POST': 
        try:                     
            emp = Employee.objects.get(user=request.user)
            permissions = quote_permissions(emp)
            
            if permissions['create_quote']:
                
                client = Client.objects.get(id= request.POST['client'])

                #job_card info part
                try:

                    job_card = request.POST["job_card_id"]
                    print(job_card)
                    job_card_obj = JobcardInfo.objects.get(id = job_card)
                    print(job_card_obj)
                except:
                    job_card_obj = None
                    pass
                if job_card_obj != None:
                    if job_card_obj.quote !=None:
                        print("perfect okay")
                        return Response ({'app_data':'Job card is already connected',"dev_data":"Job card is already connected"},status=status.HTTP_400_BAD_REQUEST)  
                else:
                        try:
                            request.POST._mutable = True
                        except:
                            pass
                        
                        job_card_id = " "    
                #for safety data  
                if 'safety_data' in request.data:
                    try:
                        safety_data=request.POST['safety_data']
                        safety_file_name ='safety_data_file_' +str(uuid.uuid4()) + '.pdf'
                        options={'page-size':'A4', 'dpi':400, 'disable-smart-shrinking': ''}
                        a =pdfkit.from_string(safety_data,safety_file_name, options=options)
                        file =open(safety_file_name)
                        Path(safety_file_name).rename("media/quote/archive/"+safety_file_name)
                        safety_data_url = "/quote/archive/"+safety_file_name
                    except:
                        try:
                            request.POST._mutable = True
                        except:
                            pass
                        request.POST['safety_data'] = ' '   
                        safety_data_url = " "    
                else:
                    safety_data_url = " " 
                #for safety data model
                if 'safety_data' in request.data:

                    try:
                        user_safety_data = UserSafetyData.objects.create(send_by =emp,send_to=client,safety_data=safety_data,safety_data_url=safety_data_url,tab_type=tab_type)
                        user_safety_data.save()
                    except: 
                        pass    
                try:
                    mail_subject = request.POST['mail_subject']
                except:     
                    try:
                        request.POST._mutable = True
                    except:
                        pass
                    mail_subject =" "
                # try:  
                # mail_signature_obj = MailSignature.objects.get(name=emp)    
                # mail_signature = mail_signature_obj.signature
                # try:

                profile_pic= "https://deep.envirowasteadmin.com.au" + emp.dp.url
                employee_data = {
                
                'name': emp.name,
                'profile_pic':profile_pic,
                'title':emp.user_type,
                'employee_mobile':emp.contact_number,
                'mobile':emp.contact_number,
                'website':'beta.envirowasteadmin.com.au',
                'email':emp.email,
                'address':emp.address,
                'address2':'lemon street,EWI45',
                'linkedin_link':emp.linkedin_link,
                'instagram_link':emp.instagram_link,
                'facebook_link':emp.facebook_link,


                }
                message1 = get_template('enquiry.html').render(employee_data) 
                # except:
                #     mail_signature ="" 

                try:
                    mail_body = request.POST['mail_body']
                except:     
                    try:
                        request.POST._mutable = True
                    except:
                        pass
                    mail_body =" " 
                    
                if 'safety_data' in request.data:

                    quote_obj = Quote.objects.create(template=template_url,reoccurring=request.POST['reoccurring'],
                    auto_create=request.POST['auto_create'],status = request.POST['status'],url = request.POST['url'],
                    client = client,employee=emp,tab_type=tab_type,job_type=request.POST['job_type'],
                    invoice_amt=request.POST['invoice_amt'],company_name=request.POST['company_name'],amount=request.POST['amount'],
                    template_html_send=request.POST['template'],mail_body=mail_body,mail_subject=mail_subject,safety_data=safety_data_url,safety_data_html_send=request.POST['safety_data'])
                    quote_obj.save()
                else:
                    quote_obj = Quote.objects.create(reoccurring=request.POST['reoccurring'],
                    auto_create=request.POST['auto_create'],status = request.POST['status'],url = request.POST['url'],
                    client = client,employee=emp,tab_type=tab_type,job_type=request.POST['job_type'],
                    invoice_amt=request.POST['invoice_amt'],company_name=request.POST['company_name'],amount=request.POST['amount'],
                    mail_body=mail_body,mail_subject=mail_subject,safety_data=safety_data_url)
                    quote_obj.save()    

                    try:
                        date = datetime.now().date()
                        base_template=request.POST['template']
                        temp1 = base_template.replace("<!-- QUOTESPLIT -->",str(quote_obj.id))
                        temp2 = temp1.replace("<!-- DATESPLIT -->",str(date))
                        template = temp2.replace("<!-- EXESPLIT -->",str(emp.name))

                        file_name ='quote_file_' +str(uuid.uuid4()) + '.pdf'
                        options={'page-size':'A4', 'dpi':400, 'disable-smart-shrinking': ''}
                        a =pdfkit.from_string(template,file_name, options=options)
                        file =open(file_name)
                        Path(file_name).rename("media/quote/archive/"+file_name)
                        template_url = "/quote/archive/"+file_name
                    except:
                        try:
                            request.POST._mutable = True
                            
                        except:
                            pass
                        request.POST['template'] = ' '   
                        template_url = " "
                    quote_obj.template_html_send=template  
                    quote_obj.template = template_url
                    quote_obj.save()
                    #UserQuoteTemplate
                    if 'template' in request.data:
                        try:
                            user_template = UserQuoteTemplate.objects.create(send_by =emp,send_to=client,template=template,template_url=template_url,tab_type=tab_type)
                            user_template.save()
                        except: 
                            pass    


                try:
                    request.POST._mutable = False
                except:
                    pass
                if 'mail_bcc' in request.data:
                    for i in request.POST.getlist('mail_bcc'):
                        bcc =EmailBcc.objects.create(bcc=i)
                        obj = quote_obj.mail_bcc.add(bcc)
                        quote_obj.save(obj)
                if 'mail_cc' in request.data:
                    for i in request.POST.getlist('mail_cc'):
                        cc =EmailCc.objects.create(cc=i)
                        obj = quote_obj.mail_cc.add(cc)
                        quote_obj.save(obj)        
                client_email = []
                client_email.append(client.client_email)  
                try:
                    subject = request.POST['mail_subject']
                except:
                    subject = "Enviro quotation"

                message =[]
                base = "https://deep.envirowasteadmin.com.au/"
                recipient_list =[]
                email_from = settings.EMAIL_HOST_USER
                quote = Quote.objects.get(id=quote_obj.id)
                quote_uuid = quote.uuid
                url = "https://quote.envirowasteadmin.com.au/" + str(quote_uuid)

                mail_body= quote.mail_body
                background_img = "https://deep.envirowasteadmin.com.au/media/mail/signature/email.png"
                if quote.tab_type =="hills":
                    logo = "https://deep.envirowasteadmin.com.au/media/enviro/company/Enviro_Hills.png"
                if quote.tab_type =="pumps":
                    logo = "https://deep.envirowasteadmin.com.au/media/enviro/company/Enviro_Pump__services.png"   
                if quote.tab_type =="destruction":
                    logo = "https://deep.envirowasteadmin.com.au/media/enviro/company/Enviro_Product_Destruction.png" 
                if quote.tab_type =="waste":
                    logo = "https://deep.envirowasteadmin.com.au/media/enviro/company/Enviro_Waste_Services.png"    

                

                quote_url = {'actions_url':url,'bg_img':background_img,'logo':logo,'mail_body':mail_body}
                action_url = get_template('button.html').render(quote_url)
                    
                temp_client = Client.objects.filter(active_status =True,id = quote.client.id)
                message_content ="" 
                try:
                    message_content =request.POST['mail_body']
                except:
                    pass

                list_message='\n'.join(map(str, message))
                body = ""
                try:
                    body = '\n'  +'\n' + '\n' + action_url + '\n' + list_message + '\n' + '\n' + message1                              
                except:
                    pass

                try:
                    bcc = request.POST.getlist('mail_bcc')
                except:
                    bcc =[]
                
                try:
                    cc = request.POST.getlist('mail_cc')     
                except:
                    cc =[]
                mail = EmailMessage(subject,body, email_from, client_email, bcc=bcc, cc=cc)
                mail.content_subtype = "html"
                if 'quote_attachment' in request.data: 
                        for i in request.POST.getlist('quote_attachment'):
                            obj = quote_obj.quote_attach_files_in.add(Files.objects.get(id=i))
                            quote_obj.save(obj)
                            drive_file_archive_obj =Files.objects.filter(id=i)
                            for attachments in drive_file_archive_obj:  
                                mail.attach_file("media/uploads/drive/file-archive/"+os.path.basename(attachments.file.url))
                if 'attachments_list' in request.data:
                            file_attachment_list =[]
                            uploaded_files = request.data.pop('attachments_list')
                            folder_obj = SalesFolders.objects.get(tab_type='waste',Sales_folder_list='others')
                            if not uploaded_files == ['']:  
                                for attachment in uploaded_files:  
                                    file_obj =SalesFolderFiles.objects.create(folder=folder_obj,attachment=attachment,quote=quote_obj)
                                    file_attachment_list.append(file_obj)
                                for attachments in file_attachment_list:
                                    mail.attach_file("media/uploads/sales/file-archive/"+os.path.basename(attachments.attachment.url))  
                                            
                if 'template'  in request.data and template!=' ':

                    file_template = quote_obj.template
                    file_temp= str(file_template)
                    file_safety_data = quote_obj.template
                    file_safety_temp= str(file_safety_data)
                    mail.attach_file("media/quote/archive/"+file_name) 
                if 'safety_data'  in request.data:
                    mail.attach_file("media/quote/archive/"+safety_file_name)   
                try:
                    message =str(emp.name) + " generated a quote"
                    LoggingInfo.objects.create(message=message,quote=quote_obj)
                except:
                    pass 
                #job_card_connection   
                try:
                    job_card_obj.quote = quote_obj
                    job_card_obj.save()
                except:
                    pass
                mail.send() 
                
                # try:
                #     job_exist = Job.objects.get(quote=quote_obj)
                # except:
                #     job_obj = Job.objects.create(tab_type=tab_type,created_by=emp,client = client,quote=quote,amount=request.POST['amount'],paid_amount = '0',reoccurring=request.POST['reoccurring'],
                #     status = request.POST['status'],job_type=request.POST['job_type'],schedule_status=False)
                #     job_obj.save()
        
                return Response({'Success':'Quote register','app_data':'Quote generated'},status.HTTP_201_CREATED)    
        except Exception as E:
            return Response({'Error':str(E),'app_data':'Quote generation failed'},status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'GET': 
        try:
            if tab_type =="all" or tab_type =='waste':
                limit = request.GET['limit']
                quote = Quote.objects.all()
                serializer = QuoteGetSerializer(quote,many=True)
                paginate_data = paginate(serializer.data,page,int(limit))
                return Response(paginate_data)          
            else:   
                limit = request.GET['limit']
                quote = Quote.objects.filter(tab_type = tab_type)
                serializer = QuoteGetSerializer(quote,many=True)
                paginate_data = paginate(serializer.data,page,int(limit))
                return Response(paginate_data)                         
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'No such quotation found '}, status=status.HTTP_400_BAD_REQUEST)  
@api_view(['POST','GET'])         
@permission_classes([IsAuthenticated])
def quote_search_date_site_client(request,tab_type,search_key,page=1):            
    if request.method == 'POST': 
        try:
            key = request.POST['key']
            if search_key == "datetime":
                if tab_type == "waste" or tab_type =="all":
                    limit = request.GET['limit']
                    quote_found=Quote.objects.filter(Q(date__istartswith=key))
                    serializer = QuoteGetSerializer(quote_found,many=True)
                    paginate_data = paginate(serializer.data,page,int(limit))
                    return Response(paginate_data)
                    
                else:
                    limit = request.GET['limit']
                    quote_found=Quote.objects.filter(Q(date__istartswith=key)).filter(tab_type=tab_type) 
                    serializer = QuoteGetSerializer(quote_found,many=True)
                    paginate_data = paginate(serializer.data,page,int(limit))
                    return Response(paginate_data)    
          
       
            if search_key == "site":
                if tab_type == "waste" or tab_type=="all":
                    client_id = key
                    limit = request.GET['limit']
                    quote_found=Quote.objects.filter(client__client_name =key)
                    print(quote_found)
                    serializer = QuoteGetSerializer(quote_found,many=True)
                    paginate_data = paginate(serializer.data,page,int(limit))
                    return Response(paginate_data)  
                else:
                    limit = request.GET['limit']
                    quote_found=Quote.objects.filter(client__client_name =key).filter(tab_type=tab_type) 
                    serializer = QuoteGetSerializer(quote_found,many=True)
                    paginate_data = paginate(serializer.data,page,int(limit))
                    return Response(paginate_data)                 
                          
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'No such quotation found '}, status=status.HTTP_400_BAD_REQUEST) 
            
            
            
            

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def resent_quote_mail(request,tab_type,quote_id): 
    if request.method =="GET":
        # try:
            emp = Employee.objects.get(user=request.user)
            permissions = quote_permissions(emp)
            if permissions['create_quote']:
            
                latest_quote = Quote.objects.get(id =quote_id)
                client_email = []
                client_email.append(latest_quote.client.client_email)
                if latest_quote.mail_subject == " ":
                    subject = "Enviro quotation"
                else:
                    subject =latest_quote.mail_subject         
                message =[]
                base = "https://deep.envirowasteadmin.com.au/"
                recipient_list =[]
                email_from = settings.EMAIL_HOST_USER
                quote = Quote.objects.get(id=latest_quote.id)
                quote_uuid = quote.uuid
                url = "http://quote.envirowasteadmin.com.au/" + str(quote_uuid) + "/"
                temp_client = Client.objects.filter(active_status =True,id = quote.client.id)
                message_content =""
                try:
                    message_content =latest_quote.mail_body
                except:
                    pass
                profile_pic= "https://deep.envirowasteadmin.com.au" + emp.dp.url
                employee_data = {
                
                'name': emp,
                'profile_pic':profile_pic,
                'title':emp.user_type,
                'employee_mobile':emp.contact_number,
                'mobile':"364587436578",
                'website':'beta.envirowasteadmin.com.au',
                'email':'envirowaste.official@gmail.com',
                'address1':"sidney",
                'address2':'lemon street,EWI45'

                }
                message1 = get_template('enquiry.html').render(employee_data) 


                message =[]
                base = "https://deep.envirowasteadmin.com.au/"
                recipient_list =[]
                email_from = settings.EMAIL_HOST_USER
                quote = Quote.objects.get(id=quote_id)
                quote_uuid = quote.uuid
                url = "http://quote.envirowasteadmin.com.au/" + str(quote_uuid) + "/"
                quote_url = {'actions_url':url}
                action_url = get_template('button.html').render(quote_url)
                temp_client = Client.objects.filter(active_status =True,id = quote.client.id)
                message_content ="" 
                try:
                    message_content =""
                except:
                    pass

                list_message='\n'.join(map(str, message))
                body = ""
                try:
                    body = message_content + '\n' + 'PFA' +'\n' + '\n' + action_url + '\n' + list_message + '\n' + '\n' + message1                              
                except:
                    pass
                file_template = latest_quote.template
                file_temp= str(file_template)
                
                try:
                    bcc=[]
                    for mail in latest_quote.mail_bcc.all():
                        bcc.append(mail.bcc)    
                except:
                    bcc =[]
                
                try:
                    cc=[]
                    for mail in latest_quote.mail_cc.all():
                        cc.append(mail.cc)
                except:
                    cc =[]
                mail = EmailMessage(subject, body, email_from, client_email, bcc=bcc, cc=cc)
                mail.content_subtype = "html"
                if latest_quote.quote_attach_files_in:
                    for i in latest_quote.quote_attach_files_in.all():
                        drive_file_archive_obj =Files.objects.filter(id=i.id)
                        for attachments in drive_file_archive_obj:
                            mail.attach_file("media/uploads/drive/file-archive/"+os.path.basename(attachments.file.url))       
                if SalesFolderFiles.objects.filter(quote = latest_quote).exists():
                        file_attachment_list =[]
                        # uploaded_files = request.data.pop('attachments_list')
                        quote_attach_file = SalesFolderFiles.objects.filter(quote = latest_quote)
                        for attachment in quote_attach_file:
                            file_attachment_list.append(attachment)
                        for attachments in file_attachment_list:
                            mail.attach_file("media/uploads/sales/file-archive/"+os.path.basename(attachments.attachment.url))    
                if latest_quote.template !=None:
                    mail.attach_file("media/quote/archive/"+os.path.basename(latest_quote.template.url))
                try:
                    message =str(emp.name) + " Resent a Quote mail"
                    LoggingInfo.objects.create(message=message,quote=quote_obj)
                except:
                    pass     
                mail.send()
                return Response({'Success':'Mail resent successfully','app_data':'Mail resent successfully'},status.HTTP_201_CREATED)
        # except Exception as E:
        #         return Response({'Error':str(E),'app_data':'senting mail failed'},status=status.HTTP_400_BAD_REQUEST)    


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def re_sale_performance(request,tab_type):
    if request.method =="GET":
        try:
            manager_id =Employee.objects.filter(user_type = "manager",active_status=True)
            for j in manager_id:
                names = {}
                data = []
            for i in manager_id:
                if tab_type =='waste' or tab_type=="all":
                    won_count = Quote.objects.filter(status = "accepted",employee__id = i.id).count()
                    lost_count = Quote.objects.filter(status = "rejected",employee__id = i.id).count()
                    pending_count = Quote.objects.filter(status = "pending",employee__id = i.id).count()
                else:
                    won_count = Quote.objects.filter(status = "accepted",employee__id = i.id,tab_type=tab_type).count()
                    lost_count = Quote.objects.filter(status = "rejected",employee__id = i.id,tab_type=tab_type).count()
                    pending_count = Quote.objects.filter(status = "pending",employee__id = i.id,tab_type=tab_type).count()
                serializer = EmployeeGetSerializer(i,many=False)
                employee=serializer.data
                dp= Employee.objects.get(id=i.id)
            

                image =str(dp.dp)
                start ="/media/"
                res = "".join((start, image)) 

                names['name'] =i.name 
                names['won'] = won_count
                names['lost'] = lost_count
                names['pending'] = pending_count
                names['total'] =lost_count + won_count + pending_count
                names['profile'] = res
                names['id'] = i.id
                data.append(names.copy())
            return Response({'Success': 'sale_perfomance','app_data': data})        
        except Exception as E:
            return Response ({"Error":str(E),'app_data':'something went wrong'})
        
         

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def re_performance_filter(request,tab_type,year = 0,month= 0):
    if request.method =="GET":
        try:
            manager_id =Employee.objects.filter(user_type = "manager")
            for j in manager_id:
                names = {}
                data = []
            for i in manager_id:
                try:
                    if tab_type =='waste' or tab_type =='all':
                        if( year >= 2000 and month ==0):
                            won_count = Quote.objects.filter(status = "accepted",employee__id = i.id).filter(date__year=year).count()
                            lost_count = Quote.objects.filter(status = "rejected",employee__id = i.id).filter(date__year=year).count()
                            pending_count = Quote.objects.filter(status = "pending",employee__id = i.id).filter(date__year=year).count()
                        
                        if( month >0<13 and year >=2000):
                            won_count = Quote.objects.filter(status = "accepted",employee__id = i.id).filter(date__year=year,date__month=month).count()
                            lost_count = Quote.objects.filter(status = "rejected",employee__id = i.id).filter(date__year=year,date__month=month).count()
                            pending_count = Quote.objects.filter(status = "pending",employee__id = i.id).filter(date__year=year,date__month=month).count()

                    else:


                        if( year >= 2000 and month ==0):
                            won_count = Quote.objects.filter(status = "accepted",employee__id = i.id,tab_type=tab_type).filter(date__year=year).count()
                            lost_count = Quote.objects.filter(status = "rejected",employee__id = i.id,tab_type=tab_type).filter(date__year=year).count()
                            pending_count = Quote.objects.filter(status = "pending",employee__id = i.id,tab_type=tab_type).filter(date__year=year).count()
                        
                        if( month >0<13 and year >=2000):
                            won_count = Quote.objects.filter(status = "accepted",employee__id = i.id,tab_type=tab_type).filter(date__year=year,date__month=month).count()
                            lost_count = Quote.objects.filter(status = "rejected",employee__id = i.id,tab_type=tab_type).filter(date__year=year,date__month=month).count()
                            pending_count = Quote.objects.filter(status = "pending",employee__id = i.id,tab_type=tab_type).filter(date__year=year,date__month=month).count()
                    serializer = EmployeeGetSerializer(i,many=False)
                    employee=serializer.data
                    dp= Employee.objects.get(id=i.id)
                    image =str(dp.dp)
                    start ="/media/"
                    res = "".join((start, image)) 
                    names['name'] =i.name
                    names['won'] = won_count
                    names['lost'] = lost_count
                    names['pending'] = pending_count
                    names['total'] =lost_count + won_count + pending_count
                    names['profile'] = res
                    names['id'] = i.id
                    data.append(names.copy())
                except Exception as E:
                    return Response ({'Error':str(E),'app_data':'Enter a valid date range'})
        except Exception as E:
            return Response ({'Error':str(E),'app_data':'failed to access sales performance'})     
        return Response({'Success': 'sale_perfomance','app_data': data})    


@api_view(['GET'])         
@permission_classes([IsAuthenticated]) 
def re_generated_jobs(request,tab_type,page_number=1):
    if request.method == 'GET': 
        try:
            if (tab_type =='waste' or tab_type =='all'):
                limit = request.GET['limit']
                accepted_jobs = Job.objects.filter(status='accepted',quote__sales_team_review = True)
                serializer = JobGetSerializer(accepted_jobs,many=True)
                paginate_data = paginate(serializer.data,page_number,int(limit))
                return Response(paginate_data)
            else:
                limit = request.GET['limit']
                accepted_jobs = Job.objects.filter(status='accepted',tab_type=tab_type,quote__sales_team_review = True)
                serializer = JobGetSerializer(accepted_jobs,many=True)
                paginate_data = paginate(serializer.data,page_number,int(limit))
                return Response(paginate_data)  
            
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'No such job found '}, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])         
@permission_classes([IsAuthenticated])
def re_all_job_filter_byPayment(request,tab_type,page_number=1):
    if request.method == 'GET': 
        try:
            if (tab_type =='waste' or tab_type =='all'):
                accepted_jobs=Job.objects.filter(amount=models.F('paid_amount'))
            else:
                accepted_jobs=Job.objects.filter(tab_type=tab_type,amount=models.F('paid_amount'))
            serializer = JobGetSerializer(accepted_jobs,many=True)

            paginate_data = paginate(serializer.data,page_number,8)
            return Response(paginate_data)                      
        except:
            return Response({'Error': 'No such quotation found', 'app_data': 'No such quotation found '}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])         
@permission_classes([IsAuthenticated])
def re_get_job_details(request,tab_type,job_id):
    if request.method == 'GET': 
        try:        
            if (tab_type =='waste' or tab_type =='all'):
                accepted_jobs = Quote.objects.filter(id= job_id)
            else:
                accepted_jobs = Quote.objects.filter(id= job_id,tab_type=tab_type)
            files = ClientImages.objects.filter(client= job_id)
            client_details = JobDetailsGetSerializer(accepted_jobs)
            client_images = ClientImagesGetSerializer(files,many=True)
            return Response({"client_details":client_details.data,"images":client_images.data})                         
        except:
            return Response({'Error': 'No such quotation found', 'app_data': 'No such quotation found '}, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET'])         
@permission_classes([IsAuthenticated])
def re_job_filter_byPayment(request,tab_type,payment,page =1):
    if request.method == 'GET':
        try:
            limit = request.GET['limit']
            if payment == 'paid':
                if (tab_type =='waste' or tab_type =='all'):
                    accepted_jobs=Job.objects.filter(amount=models.F('paid_amount'))
                else:    
                    accepted_jobs=Job.objects.filter(tab_type=tab_type,amount=models.F('paid_amount'))
                serializer = JobGetSerializer(accepted_jobs,many=True)
                paginate_data = paginate(serializer.data,page,int(limit))
                return Response(paginate_data)   
            elif payment == 'un-paid':
                if (tab_type =='waste' or tab_type =='all'):
                    accepted_jobs = Job.objects.filter(paid_amount="0")
                else:
                    accepted_jobs = Job.objects.filter(paid_amount="0",tab_type=tab_type)
                serializer = JobGetSerializer(accepted_jobs,many=True)
                paginate_data = paginate(serializer.data,page,int(limit))
                return Response(paginate_data)   
                       
        except:
            return Response({'Error': 'No such quotation found', 'app_data': 'No such quotation found '}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])         
@permission_classes([IsAuthenticated])
def re_manager_quotes(request,tab_type,manager_id,page_number=1):
    if request.method == 'GET': 
        try:
            if (tab_type =='waste' or tab_type =='all'):
                quote = Quote.objects.filter(employee=manager_id)
            else:
                quote = Quote.objects.filter(employee=manager_id,tab_type=tab_type)
            serializer = QuoteGetSerializer(quote,many=True)
            paginate_data = paginate(serializer.data,page_number,8)
            return Response(paginate_data)                         
        except:
            return Response({'Error': 'No such quotation found', 'app_data': 'No such quotation found '}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])         
@permission_classes([IsAuthenticated])
def quote_filter_by_state(request,tab_type,state,manager_id,page_number=1):
    if request.method == 'GET': 
        try:
            if (tab_type =='waste' or tab_type =='all'):
                if state =='accepted':
                    quote = Quote.objects.filter(employee=manager_id,status='accepted')
                elif  state =='rejected':
                    quote = Quote.objects.filter(employee=manager_id,status='rejected')
                elif  state =='pending':
                    quote = Quote.objects.filter(employee=manager_id,status='pending')    

            else:
                quote = Quote.objects.filter(employee=manager_id,tab_type=tab_type)
                if state =='accepted':
                    quote = Quote.objects.filter(employee=manager_id,tab_type=tab_type,status='accepted')
                elif state =='rejected':
                    quote = Quote.objects.filter(employee=manager_id,tab_type=tab_type,status='rejected')
                elif state =='pending':
                    quote = Quote.objects.filter(employee=manager_id,tab_type=tab_type,status='pending')  
            serializer = QuoteGetSerializer(quote,many=True)
            paginate_data = paginate(serializer.data,page_number,8)
            return Response(paginate_data)                            
        except:
            return Response({'Error': 'No such quotation found', 'app_data': 'No such quotation found '}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])         
@permission_classes([IsAuthenticated])
def re_get_sales_folders_and_files(request,sales_archive,folder_id=0):
    if request.method =="GET":
        try:
            if(sales_archive =='marketing'):
            
                try:
                    folders =[]
                   
                    for folder in DriveFolder.objects.filter(id =folder_id):
                        
                        file_list = []  
                        for files in Files.objects.filter(folder=folder).order_by('name'):
                            file_data= {
                                'id': files.id,
                                'name': os.path.basename(files.file.url),
                                'url': files.file.url
                            }
                            file_list.append(file_data)
                        subfolder_list =[]    
                        for subfolder in DriveFolder.objects.filter(parent_folder=folder_id,marketing=True).order_by('name'):
                            subfolder_list.append({'id':subfolder.id,"name":subfolder.name,"type":"marketing"})


                        subfolder_data = {
                            'files': file_list,
                            'folders':subfolder_list,
                            'type':"marketing"
                            }
                        folders.append(subfolder_data)  
                        return Response({"folders":folders})
                        
                except Exception as E:
                    return Response({"app_data": "Something went wrong", "dev_data":str(E)})
    
            if(sales_archive =='description_of_waste'):
                try:
                    folders =[]
                    for folder in DriveFolder.objects.filter(id =folder_id):
                            
                            file_list = []  
                            for files in Files.objects.filter(folder=folder).order_by('name'):
                                file_data= {
                                    'id': files.id,
                                    'name': os.path.basename(files.file.url),
                                    'url': files.file.url
                                }
                                file_list.append(file_data)
                            subfolder_list =[]    
                            for subfolder in DriveFolder.objects.filter(parent_folder=folder_id,description_of_waste=True).order_by('name'):
                                subfolder_list.append({'id':subfolder.id,"name":subfolder.name,'type':"description_of_waste"})


                            subfolder_data = {
                                'files': file_list,
                                'folders':subfolder_list,
                                'type':"description_of_waste"
                                }
                            folders.append(subfolder_data)  
                            return Response({"folders":folders})
        

                except Exception as E:
                    return Response({"app_data": "Something went wrong", "dev_data":str(E)})
            if(sales_archive =='power_point'):
                try:
                    folders =[]
                    for folder in DriveFolder.objects.filter(id =folder_id):
                        
                        file_list = []  
                        for files in Files.objects.filter(folder=folder).order_by('name'):
                            file_data= {
                                'id': files.id,
                                'name': os.path.basename(files.file.url),
                                'url': files.file.url
                            }
                            file_list.append(file_data)
                        subfolder_list =[]    
                        for subfolder in DriveFolder.objects.filter(parent_folder=folder_id,power_point=True).order_by('name'):
                            subfolder_list.append({'id':subfolder.id,"name":subfolder.name,"type":"power_point"})


                        subfolder_data = {
                            'files': file_list,
                            'folders':subfolder_list,
                            "type":"power_point"
                            }
                        folders.append(subfolder_data)  
                        return Response({"folders":folders})
                    

                except Exception as E:
                    return Response({"app_data": "Something went wrong", "dev_data":str(E)})    
                    
            if(sales_archive =='pricing'):
                try:
                    folders =[]
                   
                       
                    for folder in DriveFolder.objects.filter(id =folder_id):
                        
                        file_list = []  
                        for files in Files.objects.filter(folder=folder).order_by('name'):
                            file_data= {
                                'id': files.id,
                                'name': os.path.basename(files.file.url),
                                'url': files.file.url
                            }
                            file_list.append(file_data)
                        subfolder_list =[]    
                        for subfolder in DriveFolder.objects.filter(parent_folder=folder_id,pricing=True).order_by('name'):
                            subfolder_list.append({'id':subfolder.id,"name":subfolder.name,"type":"pricing"})


                        subfolder_data = {
                            'files': file_list,
                            'folders':subfolder_list,
                            "type":"pricing"
                            }
                        folders.append(subfolder_data)  
                        return Response({"folders":folders})
                except Exception as E:
                    return Response({"app_data": "Something went wrong", "dev_data":str(E)})   
                
                     
            if(sales_archive =='tender'):
                try:
                    folders =[]
                   
                    for folder in DriveFolder.objects.filter(id =folder_id):
                            
                        file_list = []  
                        for files in Files.objects.filter(folder=folder).order_by('name'):
                            file_data= {
                                'id': files.id,
                                'name': os.path.basename(files.file.url),
                                'url': files.file.url
                            }
                            file_list.append(file_data)
                        subfolder_list =[]    
                        for subfolder in DriveFolder.objects.filter(parent_folder=folder_id,tender=True).order_by('name'):
                            subfolder_list.append({'id':subfolder.id,"name":subfolder.name,"type":"tender"})


                        subfolder_data = {
                            'files': file_list,
                            'folders':subfolder_list,
                            "type":"tender"
                            }
                        folders.append(subfolder_data)  
                        return Response({"folders":folders})  
                except Exception as E:
                    return Response({"app_data": "Something went wrong", "dev_data":str(E)})             
        except Exception as E:
            return Response({"app_data": "Something went wrong", "dev_data":str(E)})      

@api_view(['GET'])         
@permission_classes([IsAuthenticated])
def re_get_generate_quote_folder_list(request,tab_type):
    if request.method == 'GET':   
        try:
            folders =[]
            for folder in DriveFolder.objects.filter(parent_folder = 0):
                files_list = []  
                for files in Files.objects.filter(folder=folder):
                    file_data= {
                        'id': files.id,
                        'name': os.path.basename(files.file.url),
                        'url': files.file.url
                    }
                    files_list.append(file_data)
                subfolders3_list =[]    
                for subfolder in DriveFolder.objects.filter(parent_folder=folder.id,generate_quote=True,tab_type=tab_type):      
                    subfolder_files_list = []
                    for subfolderfile in Files.objects.filter(folder=subfolder):
                        subfolderfile_data = {
                            'id': subfolderfile.id,
                            'name': os.path.basename(subfolderfile.file.url),
                            'url': subfolderfile.file.url
                        }
                        subfolder_files_list.append(subfolderfile_data)
                    s_subfolder_list = []
                    for s_subfolder in DriveFolder.objects.filter(parent_folder=subfolder.id,generate_quote=True,tab_type=tab_type):
                        s_subfolder_files_list = []
                        for s_subfolderfile in Files.objects.filter(folder=s_subfolder):
                            s_subfolderfile_data = {
                                'id': s_subfolderfile.id,
                                'name': os.path.basename(s_subfolderfile.file.url),
                                'url': s_subfolderfile.file.url
                            }
                            s_subfolder_files_list.append(s_subfolderfile_data)
                        ss_subfolder_list = []    
                        for ss_subfolder in DriveFolder.objects.filter(parent_folder=s_subfolder.id,generate_quote=True,tab_type=tab_type):
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
            return Response({"app_data": "Something went wrong", "dev_data":str(E)},status=status.HTTP_400_BAD_REQUEST)                      
@api_view(['GET'])         
@permission_classes([IsAuthenticated])
def re_get_generate_quote_folder_attachment(request,tab_type):
    if request.method == 'GET':   
        try:
            folders =[]
            for folder in DriveFolder.objects.filter(parent_folder = 0):
                files_list = []  
                for files in Files.objects.filter(folder=folder):
                    file_data= {
                        'id': files.id,
                        'name': os.path.basename(files.file.url),
                        'url': files.file.url
                    }
                    files_list.append(file_data)
                subfolders3_list =[]    
                for subfolder in DriveFolder.objects.filter(parent_folder=folder.id,attach_quote=True,tab_type=tab_type):      
                    subfolder_files_list = []
                    for subfolderfile in Files.objects.filter(folder=subfolder):
                        subfolderfile_data = {
                            'id': subfolderfile.id,
                            'name': os.path.basename(subfolderfile.file.url),
                            'url': subfolderfile.file.url
                        }
                        subfolder_files_list.append(subfolderfile_data)
                    s_subfolder_list = []
                    for s_subfolder in DriveFolder.objects.filter(parent_folder=subfolder.id,attach_quote=True,tab_type=tab_type):
                        s_subfolder_files_list = []
                        for s_subfolderfile in Files.objects.filter(folder=s_subfolder):
                            s_subfolderfile_data = {
                                'id': s_subfolderfile.id,
                                'name': os.path.basename(s_subfolderfile.file.url),
                                'url': s_subfolderfile.file.url
                            }
                            s_subfolder_files_list.append(s_subfolderfile_data)
                        ss_subfolder_list = []    
                        for ss_subfolder in DriveFolder.objects.filter(parent_folder=s_subfolder.id,attach_quote=True,tab_type=tab_type):
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
            return Response({"app_data": "Something went wrong", "dev_data":str(E)},status=status.HTTP_400_BAD_REQUEST)	


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def quote_search(request,tab_type):
    if request.method == 'POST':
        try:
            key = request.POST['key']
            if(key == ' '):
                quote_found = Quote.objects.filter(tab_type=tab_type)
                serializer = QuoteGetSerializer(quote_found,many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:

                quote_found=Quote.objects.filter(Q(uuid__istartswith=key) | Q(employee__name__istartswith=key) |  Q(won_reject_date__istartswith=key) | Q(client__client_name__istartswith=key) | Q(amount__istartswith=key) | Q(company_name__istartswith=key) | Q(reoccurring__istartswith=key) | Q(status__istartswith=key) | Q(auto_create__istartswith=key) | Q(paid_status__istartswith=key)| Q(job_type__istartswith=key) | Q(invoice_amt__istartswith=key) ).filter(tab_type=tab_type)
                serializer = QuoteGetSerializer(quote_found,many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'No maches found'}, status=status.HTTP_400_BAD_REQUEST) 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def quote_search_by_client_id(request,tab_type):
    if request.method == 'POST':
        try:
            key = request.POST['key']
            page = 1
            limit = 8
            try:
                page = int(request.GET['page'])
                limit = int(request.GET['limit'])
            except:
                pass  
            
            if(key == ' '):
                    if (tab_type =='waste' or tab_type =='all'):
                        quote_found = Quote.objects.all()
                    else:
                        quote_found = Quote.objects.filter(tab_type=tab_type)
                    
                    serializer = QuoteGetSerializer(quote_found,many=True)
                    paginate_data = paginate(serializer.data,page,limit)    
                    return Response(paginate_data, status=status.HTTP_200_OK)
            else:
                if (tab_type =='waste' or tab_type =='all'):
                        quote_found = Quote.objects.filter(client__client_name__istartswith=key)
                else:
                        quote_found = Quote.objects.filter(client__client_name__istartswith=key).filter(tab_type=tab_type)
                serializer = QuoteGetSerializer(quote_found,many=True)
                paginate_data = paginate(serializer.data,page,limit)    
                return Response(paginate_data, status=status.HTTP_200_OK)
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'No maches found'}, status=status.HTTP_400_BAD_REQUEST)             

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def filterby_price_range(request,tab_type):
    if request.method == 'POST':
        try:
            quote_list = []
            start_price = request.POST['start_price']
            end_price = request.POST['end_price']
            for quote in Quote.objects.filter(tab_type=tab_type):
               if int(quote.amount) >= int(start_price) and int(quote.amount) <=int(end_price):
                   quote_list.append(quote)
            serializer = QuoteGetSerializer(quote_list,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'No maches found'}, status=status.HTTP_400_BAD_REQUEST) 

@api_view(['POST','GET','DELETE'])
@permission_classes([IsAuthenticated])
def products(request,product_id=0):
    if request.method == 'POST':
        try:
            serializer = ProductsSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'product adding failed'}, status=status.HTTP_400_BAD_REQUEST)  
    if request.method == 'GET':
        try:
            products = Products.objects.all()
            serializer = ProductsGetSerializer(products,many=True)   
            return Response(serializer.data, status=status.HTTP_200_OK)  
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'products not available'}, status=status.HTTP_400_BAD_REQUEST)     
    if request.method == 'DELETE':
        try:
            product = Products.objects.get(id=product_id)
            product.delete()
            return Response({'app_data':"product deleted",'dev_data':"product deleted"},status=status.HTTP_200_OK)  
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'products not available'}, status=status.HTTP_400_BAD_REQUEST) 


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_qoute_template(request,tab_type):
    
    if request.method == 'GET':
        try:
            user_template = UserQuoteTemplate.objects.filter(tab_type=tab_type)
            serializer = UserQuoteTemplateGetSerializer(user_template,many=True)   
            return Response(serializer.data, status=status.HTTP_200_OK)  
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'Template not available'}, status=status.HTTP_400_BAD_REQUEST)
         
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def single_user_qoute_template(request,template_id):
    if request.method == 'GET':
        try:
            user_template = UserQuoteTemplate.objects.get(id=template_id)
            serializer = SingleUserQuoteTemplateGetSerializer(user_template,many=False)   
            return Response(serializer.data, status=status.HTTP_200_OK)  
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'Template not available'}, status=status.HTTP_400_BAD_REQUEST) 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_draft_template(request,tab_type):
    if request.method == 'GET':
            try:
                draft_template = TemplateDraft.objects.filter(tab_type=tab_type)
                serializer = TemplateDraftGetAllSerializer(draft_template,many=True)   
                return Response(serializer.data, status=status.HTTP_200_OK)  
            except Exception as E:
                return Response({'Error': str(E), 'app_data': 'Template not available'}, status=status.HTTP_400_BAD_REQUEST)             

@api_view(['GET','POST','PATCH'])
@permission_classes([IsAuthenticated])
def draft_template(request,tab_type,client_id=0):
    if request.method == 'POST':
        emp = Employee.objects.get(user=request.user)
        try:
            try:
                request.POST._mutable = True
            except:
                pass
            request.POST['created_by'] = emp.id   
            serializer = TemplateDraftSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   
            try:
                request.POST._mutable = False
            except:
                pass    
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'Template not saved'}, status=status.HTTP_400_BAD_REQUEST)  
    if request.method == 'GET':
        try:
            draft_template = TemplateDraft.objects.filter(client=Client.objects.get(id=client_id),tab_type=tab_type)
            serializer = TemplateDraftGetSerializer(draft_template,many=True)   
            return Response(serializer.data, status=status.HTTP_200_OK)  
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'Template not available'}, status=status.HTTP_400_BAD_REQUEST) 
           
            
@api_view(['GET','PATCH','DELETE'])
@permission_classes([IsAuthenticated])
def single_draft_template(request,draft_id):
    if request.method == 'GET':
        try:
            user_template = TemplateDraft.objects.get(id=draft_id)
            serializer = SingleTemplateDraftSerializer(user_template,many=False)   
            return Response(serializer.data, status=status.HTTP_200_OK)  
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'Template not available'}, status=status.HTTP_400_BAD_REQUEST)             
    if request.method == 'PATCH':
        emp = Employee.objects.get(user=request.user)
        try:
            try:
                request.POST._mutable = True
            except:
                pass
            request.POST['created_by'] = emp.id
            draft_template = TemplateDraft.objects.get(id=draft_id)
            serializer = TemplateGetDraftSerializer(draft_template, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   
            try:
                request.POST._mutable = False
            except:
                pass     
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'Template not saved'}, status=status.HTTP_400_BAD_REQUEST) 

    if request.method == 'DELETE':
        try:
            draft_template = TemplateDraft.objects.get(id=draft_id)
            draft_template.delete()
            return Response({'app_data':"draft cleared",'dev_data':"deleted successfully"}, status=status.HTTP_200_OK)  
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'Template not saved'}, status=status.HTTP_400_BAD_REQUEST)        


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_safety_data(request,tab_type,employee_id):
    if request.method == 'GET':
        try:
            user_safety_data = UserSafetyData.objects.filter(tab_type=tab_type,send_by=employee_id)
            serializer = UserSafetyDataGetSerializer(user_safety_data,many=True)   
            return Response(serializer.data, status=status.HTTP_200_OK)  
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'Safety data not available'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def single_user_safety_data(request,safety_data_id):
    if request.method == 'GET':
        try:
            user_safety_data = UserSafetyData.objects.get(id=safety_data_id)
            serializer = SingleUserSafetyDataGetSerializer(user_safety_data,many=False)   
            return Response(serializer.data, status=status.HTTP_200_OK)  
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'Safety data not available'}, status=status.HTTP_400_BAD_REQUEST) 


@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def quote_attach_templates(request,tab_type,template_id=0):
    emp = Employee.objects.get(user=request.user)
    if request.method == 'GET':
        
        try:
            data = []

            if template_id >=1:
                    user_template = QuoteAttachTemplates.objects.get(id=template_id)
                    return Response({"template":user_template.template}, status=status.HTTP_200_OK)
            user_template = QuoteAttachTemplates.objects.filter(tab_type=tab_type,editable = True)

            file1 = Files.objects.get(name= "credit_application")
            file2 = Files.objects.get(name="credit_card_autharisation")
            immutable_file1={'id':file1.id,'name':file1.name,'editable':False}
            immutable_file2={'id':file2.id,'name':file2.name,'editable':False}
            data.append(immutable_file1)
            data.append(immutable_file2)

            serializer = QuoteAttachTemplatesGetSerializer(user_template,many=True) 
            for i in user_template:
                data.append({'id':i.id,'name':i.name,'editable':i.editable,})
            
            
            return Response(data, status=status.HTTP_200_OK)
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'Safety data not available'}, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'POST':
        try:   
            try:
                template_id=request.POST['template_id']
                template=request.POST['quote_attach_template']
                template_obj = QuoteAttachTemplates.objects.get(id=template_id)
                template_name=template_obj.name
                file_name =template_name +'_' +str(uuid.uuid4()) + '.pdf'
                options={'page-size':'A4', 'dpi':400, 'disable-smart-shrinking': ''}
                a =pdfkit.from_string(template,file_name, options=options)
                file =open(file_name)
                Path(file_name).rename("media/uploads/drive/file-archive/"+file_name)
                template_url = "/uploads/drive/file-archive/"+file_name
            except:
                try:
                    request.POST._mutable = True
                except:
                    pass
                request.POST['quote_attach_template'] = ' '   
                template_url = " "    
            template_folder = DriveFolder.objects.get(name='templates',template=True)               
            user_template = Files.objects.create(folder=template_folder,created_by=emp,file=template_url,template_html=template)
            template_obj = user_template.save()
            
            return Response({"template_id":user_template.id,'name':file_name,"dev_data":"added scuccesfully"}, status=status.HTTP_200_OK)  
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'Template not available'}, status=status.HTTP_400_BAD_REQUEST)      



@api_view(['GET','PATCH','POST',"DELETE"])
@permission_classes([IsAuthenticated])
def type_of_waste(request,w_id=0):
    if request.method == 'GET':
        try:
            waste_type = TypeOfWaste.objects.all()
            serializer = TypeOfWasteGetSerializer(waste_type,many=True)   
            return Response(serializer.data, status=status.HTTP_200_OK)  
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'Waste type not available'}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'POST':
        try:
            serializer = TypeOfWasteSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)       
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'Waste type not available'}, status=status.HTTP_400_BAD_REQUEST)        
    if request.method == 'DELETE':
        try:
            waste_type = TypeOfWaste.objects.get(id=w_id)
            waste_type.delete()      
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'Waste type not available'}, status=status.HTTP_400_BAD_REQUEST)   

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Quote_client_search(request):
    if request.method == 'POST':
        try:
            key = request.POST['key']
            if(key == ' '):
                client_found = Client.objects.filter(active_status = True,client_type = "Temporary")
                serializer = ClientGetSerializer(client_found,many=True)
                temporary_client = serializer.data
                client_found1 = Client.objects.filter(active_status = True,client_type = "Permenent")
                serializer = ClientGetSerializer(client_found1,many=True)
                permenent_client=serializer.data

                return Response({'temporary_client':temporary_client,'permenent':permenent_client}, status=status.HTTP_200_OK)
                
            else:
               
                client_found=Client.objects.filter(client_name__istartswith=key).filter(active_status=True,client_type = "Temporary")
                serializer = ClientGetSerializer(client_found,many=True)
                temporary_client = serializer.data

                client_found1 = Client.objects.filter(client_name__istartswith=key).filter(active_status=True,client_type = "Permenant")
                serializer = ClientGetSerializer(client_found1,many=True)
                permenent_client=serializer.data

                return Response({'temporary_client':temporary_client,'permenent':permenent_client}, status=status.HTTP_200_OK)
                
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'search not available'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])         
@permission_classes([IsAuthenticated]) 
def Ready_for_scheduled_jobs(request,tab_type,page_number=1):
    if request.method == 'GET': 
        try:
            if (tab_type =='waste' or tab_type =='all'):
                limit = request.GET['limit']
                accepted_jobs = Job.objects.filter(status='accepted',ready_for_schedule=True)
                print(accepted_jobs)
                serializer = JobGetSerializer(accepted_jobs,many=True)
                paginate_data = paginate(serializer.data,page_number,int(limit))
                return Response(paginate_data)
            else:
                limit = request.GET['limit']
                accepted_jobs = Job.objects.filter(status='accepted',tab_type=tab_type,ready_for_schedule=True)
                serializer = JobGetSerializer(accepted_jobs,many=True)
                paginate_data = paginate(serializer.data,page_number,int(limit))
                return Response(paginate_data)  
            
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'No such job found '}, status=status.HTTP_400_BAD_REQUEST)            

@api_view(['GET','POST']) 
@permission_classes([IsAuthenticated]) 
def sales_team_review_status(request,status,quote_id):
    if request.method == 'GET':
            emp = Employee.objects.get(user=request.user)
            
        
            if status  == 'accepted':
                try:   
                      
                        quote_obj = Quote.objects.get(id=quote_id)  
                
                        if quote_obj.sales_team_review ==True:
                            return Response({'message':'Requested quote already in accepted status','status':400,'app_data':"Requested quote already in accepted status"})
                        quote_obj.sales_team_review = True
                        quote_obj.won_reject_date = datetime.now()
                        quote_obj.save()
                        
                        try:
                            message =str(emp.name) + " is reviewed status as accepted "
                            LoggingInfo.objects.create(message=message,quote=quote_obj)
                        except:
                            pass 
                        temp_client_to_Permenant_client = Client.objects.filter(id=quote_obj.client.id).update(client_type="Permenant")
                        if Job.objects.filter(quote=quote_obj).count()==0:
                           
                            job_obj =Job.objects.create(tab_type=quote_obj.tab_type,created_by=quote_obj.employee,client=quote_obj.client,quote=quote_obj,amount=quote_obj.amount,paid_amount='0',reoccurring=quote_obj.reoccurring,status='accepted',schedule_status=False,job_type=quote_obj.job_type)
                            
                        else:
                            pass
                        if Job.objects.filter(quote=quote_obj).count()==1:
                            job_obj = Job.objects.get(quote=quote_obj)
                            job_obj.status="accepted"
                            job_obj.save()

                            
                        try:
                            team1 = Employee.objects.filter(user_type="accounts-staff")
                            team2 = Employee.objects.filter(user_type="accounts-manager")
                            team_list = team1 | team2
                            push_notifier_for_team("sales team reviewed a Quote",str(quote_obj.employee.name) + "approved a quote",team_list)

                            title="quote reviewed by sales team"
                            description = "qoute approved by " + str(quote_obj.employee.name)
                            notification_obj = Notification.objects.create(title = title,description=description)    
                            team1 = Employee.objects.filter(user_type="accounts-staff")
                            team2 = Employee.objects.filter(user_type="accounts-manager")
                            managers  = team1 | team2
                            print(managers)
                            for member in managers:
                                notification_obj.members.create(member_id=member)
                        except Exception as E:
                            print(str(E))
                            pass
                        team = Employee.objects.filter(user_type='manager')
                        notification_hub_obj = Notification_hub.objects.create(type='accepted',model_type='quote',reference_id=quote_obj.id)
                        for employee in team:
                            notification_hub_obj.send_to_team.add(employee.id)
                        return Response({'message': 'Quote status accepted','status':200})
                except Exception as E:
                    return Response({'message':str(E),'status':400})
        
            if status  == 'rejected':
                try:
                        quote_obj = Quote.objects.get(id=quote_id)
                        if quote_obj.sales_team_review ==False:
                
                            return Response({'message':'Requested quote already in rejected status','status':400})
                                
                        quote_obj.sales_team_review = False
                        quote_obj.won_reject_date = datetime.now()
                        quote_obj.save()
                       
                        
                        try:
                            message =str(emp.name) + " is reviewed status as rejected "
                            LoggingInfo.objects.create(message=message,quote=quote_obj,tab_type=quote_obj.tab_type)
                        except:
                            pass 
                        if Job.objects.filter(quote=quote_obj).count()==0:
                           
                            job_obj =Job.objects.create(tab_type=quote_obj.tab_type,created_by=quote_obj.employee,client=quote_obj.client,quote=quote_obj,amount=quote_obj.amount,paid_amount='0',reoccurring=quote_obj.reoccurring,status='pending',schedule_status=False,job_type=quote_obj.job_type)
                            
                        else:
                            pass
                        if Job.objects.filter(quote=quote_obj).count()==1:
                            job_obj = Job.objects.get(quote=quote_obj)
                            job_obj.status="pending"
                            job_obj.save()
                        try:
                            team_list = Employee.objects.filter(Q(user_type="accounts-staff") | Q(user_type = "accounts-manage") )
                            push_notifier_for_team("Quote status changed",str(quote_obj.employee.name) + "rejected a quote",team_list)
                            title="quote reviewed by sales team"
                            description= "qoute rejected by " + str(quote_obj.employee.name)
                            notification_obj = Notification.objects.create(title = title,description=description)    
                            managers  = Employee.objects.filter(Q(user_type = "accounts-staff") | Q (user_type = "accounts-manager"))
                            for member in managers:
                                notification_obj.members.create(member_id=member)
                             
                        except Exception as E:
                            print(str(E))
                            pass
                        team = Employee.objects.filter(user_type='manager')
                        notification_hub_obj = Notification_hub.objects.create(type='rejected',model_type='quote',reference_id=quote_obj.id)
                        for employee in team:
                            notification_hub_obj.send_to_team.add(employee.id)
                        return Response({'message': 'Quote status rejected','status':200}) 
                except Exception as E:
                    return Response({'message':str(E),'status':400})

@api_view(['GET'])         
@permission_classes([IsAuthenticated]) 
def Logging_details(request,quote_id):
    if request.method == 'GET': 
        try:
            qoute_obj = Quote.objects.get(id=quote_id)
            logging_data = LoggingInfo.objects.filter(quote=qoute_obj)
            serializer = LoggingInfoGetSerializer(logging_data,many=True)
            
            return Response(serializer.data)
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'No such info found '}, status=status.HTTP_400_BAD_REQUEST)                      
@api_view(['GET','POST']) 
def client_quote_attachment_response(request,quote_id):
    if request.method == 'POST':
                try:
                    quote_obj = Quote.objects.get(uuid=quote_id)
                    template_content=request.POST['template_content']
                    quote_attach_template_response=request.POST['template_id']
                    file_obj =Files.objects.get(id=int(quote_attach_template_response))
                    file_name_taken = str(file_obj.file.url)
                    temp =file_name_taken.rsplit('/', 1)[-1]
                    # removed_str =".pdf"
                    # get_file_name = temp.replace(removed_str, ' ')
                    file_name =temp
                    

                    options={'page-size':'A4', 'dpi':400, 'disable-smart-shrinking': ''}
                    a =pdfkit.from_string(template_content,file_name, options=options)
                    file =open(file_name)
                    Path(file_name).rename("media/quote/archive/"+file_name)
                    template_receive_response = "/quote/archive/"+file_name
                   
                    
                    response_obj = ClientQuoteAttachmentResponses.objects.create(quote_data=quote_obj,template_content=template_content,template_receive_response=template_receive_response,quote_attach_template_response=file_obj)
                    return Response({'quote':quote_obj.id,'template_content':template_content,'response_file':response_obj.template_receive_response.url,'quote_attach_template_id':file_obj.id})
                except:
                    return Response({'message':'Quote does not exists','status':400})
    if request.method == 'GET':  
        clients_response = ClientQuoteAttachmentResponses.objects.filter(quote_data__uuid=quote_id)
        print(clients_response)
        serializer = ClientQuoteAttachmentResponsesGetSerializer(clients_response,many=True)
        return Response(serializer.data)

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
@api_view(['POST'])         
@permission_classes([IsAuthenticated])
def sales_folder_update(request,sales_tab):
    if(request.method =='POST'):
        try:
            try:
                request.POST._mutable = True
            except:
                pass
            request.POST[sales_tab] = True
            serializer = DriveFolderSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                try:
                    request.POST._mutable = False
                except:
                    pass
                return Response({"folders":"added"})
            else:
                return Response({'Error':serializer.errors,'app_data': 'folder creation failed'}, status=status.HTTP_400_BAD_REQUEST)    
            
        except Exception as E:
            return Response({"app_data": "Something went wrong", "dev_data":str(E)})    

                

@api_view(['GET','POST',"DELETE"]) 
def debug_query_for_testing(request):
    if request.method == 'GET':
        try:
            try:
                li=[]
                template_folder = DriveFolder.objects.filter(vehicle=True)  
            
                for i in template_folder:
                    if i.id >=530:
                        i.vehicle_type ="truck"
                        i.save()

                        
            except Exception as E:    
                
                return Response({"error":str(E),"jj":"jj"})


           
            return Response({"data":"okay"})
        except Exception as E:
            return Response({"data":str(E)})
