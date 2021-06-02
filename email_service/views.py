from django.shortcuts import render
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


from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings





@api_view(['GET'])
@permission_classes([IsAuthenticated])
def send_email(request):
    print("iam in")
    subject = 'Thank you for registering to our site'
    message = ' it  means a world to us '
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['jithin.ezedtech@gmail.com',]
    send_mail( subject, message, email_from, recipient_list )
    return Response({'Error': 'No such Client found', 'app_data': 'No such a Client found '})