import os
import datetime
from django.shortcuts import render, HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework import status

from .models import TeamArchiveFolders, TeamArchiveFiles
from accounts.models import Employee

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def employee_archive(request, employee_id):
    try:
        employee = Employee.objects.get(id=employee_id)
        folders = TeamArchiveFolders.objects.all()
        data = []
        for folder in folders:
            if TeamArchiveFiles.objects.filter(employee=employee, team_archive_folder=folder):
                in_dict = {'folder_name':folder.name, 'files': TeamArchiveFiles.objects.filter(employee=employee, team_archive_folder=folder).values('id', 'file_item')}
                data.append(in_dict)
                
        return Response(data)
    except Exception as E:
        return Response({'Error': str(E), 'app_data':'Something went wrong while fetching files'}, status=status.HTTP_400_BAD_REQUEST)