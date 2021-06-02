from django.urls import path
from .import views
urlpatterns = [
    path('demo/', views.drive,name='drive'),
    path('folder/create/', views.folder_drive,name='folder_drive'),
    #team private folder file RENAME
    path('file/rename/<file_id>/',views.file_drive, name='file_drive'),

    path('file/create/', views.file_drive,name='file_drive'),
    path('folder/delete/<int:id>/', views.folder_delete,name='folder_delete'),
    path('file/delete/<int:file_id>/<int:folder_id>/', views.file_delete,name='file_delete'),
    path('folder/rename/<int:folder_id>/', views.folder_rename,name='folder_rename'),

    path('root/folder/', views.get_root_folder,name='get_root_folder'),

     #creating folder for team member
    path( 'create/team/folder/',views.team_folder,name='team_folder'),
     #creating folder for vehicle
    path( 'create/vehicle/folder/',views.vehicle_folder,name='vehicle_folder'),
    path( 'view/vehicle/folder/<str:vehicle_type>/<int:vehicle_id>/<int:folder_id>/',views.vehicle_folder,name='vehicle_folder'),

    #team individual folder
    path('create/team/individual/folder/', views.team_individual_folder,name='team_individual_folder'),

    path('search/<str:type>/', views.search_folder_files,name='search_folder_files'),
    path('site/search/<str:type>/', views.site_search_folder_files,name='site_search_folder_files'),

    #new one for master get folder
    path('team/master/folder/<int:folder_id>/',views.get_team_master_folders, name='get_team_master_folders'),
    path('team/master/folder/',views.get_team_master_folders, name='get_team_master_folders'),

    #employee inner folder
    path('team/folder/<int:emp_id>/<folder_id>/',views.get_employee_folders, name='get_employee_folders'),
    path('team/folder/<int:emp_id>/',views.get_employee_folders, name='get_employee_folders'),
    #team private folder file upload
    path('team/add/files/',views.create_file_in_team_member, name='create_file_in_team_member'),


    #site inner folder get
    path('site/folder/<int:site_id>/<folder_id>/',views.get_site_folders, name='get_site_folders'),
    path('site/folder/<int:site_id>/',views.get_site_folders, name='get_site_folders'),

    #site individual folder
    path('create/site/individual/folder/', views.site_individual_folder,name='site_individual_folder'),

    #site private folder
    path( 'create/site/private/folder/',views.private_site_folder,name='private_site_folder'),


    #site private folder file upload
    path('site/add/files/',views.create_file_in_site_member, name='create_file_in_site_member'),

    # multiple delete folders and files
    path('delete/<str:type>/', views.drive_multipe_delete,name='drive_multipe_delete'),

    
]