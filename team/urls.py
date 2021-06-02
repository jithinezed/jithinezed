from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('create/', views.teamCreateAPI, name='teamCreateAPI'),
    path('employee/<int:id>/', views.teamGetAPI, name='teamGetAPI'),
    path('employee/file-archive/', include('team_file_archive.urls')),
    path('employee/all/', views.teamGetAllAPI, name='teamGetAllAPI'),
    path('employee/delete/<int:employee_id>/', views.teamDeleteAPI, name='teamDeleteAPI'),
    path('employee/edit/<int:employee_id>/', views.teamEditAPI, name='teamEditAPI'),
    path('createCertificate/', views.CreateCertificate, name='CreateCertificate'),
    path('searchEmployee/', views.searchEmployee, name='searchEmployee'),
    path('employeeIdAvail/', views.employeeIdAvailability, name='employeeIdAvailability'),
    path('contactAvail/', views.contactAvailability, name='contactAvailability'),
    path('usernameAvail/', views.usernameAvailability, name='usernameAvailability'),
    path('emailAvail/', views.emailAvailability, name='emailAvailability'),
    path('profile/', views.getProfile, name='getProfile'),
    path('folder/', views.folders, name='folders'),
    #file upload api
    path('files/<int:emp_id>/', views.folders, name='folders'),
    path('files/list/<int:folder_id>/', views.getFolder, name='getFolder'),
    path('folder/<int:emp_id>/', views.getEmp, name='getEmp'),
    path('folder/search/',views.searchEmployeeInFolder, name='searchEmployeeInFolder'),
    path('folder/create/',views.createFolder, name='createFolder'),
   
    path('designations/',views.get_designations, name='get_designations'),



    path('employee/file/delete/<int:file_id>/',views.delete_emp_files, name='delete_emp_files'),
    path('employee/notifications/view/',views.getNotifications, name='getNotifications'),

    path('status/<str:team_status>/', views.team_status, name='team_status'),
    path('safety/info/<int:id>/<int:employee_id>/', views.safety_info, name='safety_info'),
    path('warning/info/<int:employee_id>/', views.warning_info, name='warning_info'),
    path('update/<str:f_type>/create/', views.update_team_folder, name='update_team_folder'),
    path('update/<str:f_type>/<int:f_id>/', views.update_team_folder, name='update_team_folder'),

   
    
]
