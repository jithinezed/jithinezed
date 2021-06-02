from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('<str:show_on>/', views.sales_archive, name='sales_archive'),
    # path('folder/<int:folder_id>/', views.intranet_folderFiles, name='intranet_folderFiles'),
    # path('folder/<str:tab_type>/<int:folder_id>/', views.intranet_folderFiles, name='intranet_folderFiles'),
    path('folder/list/', views.all_intranet_folders, name='all_intranet_folders'),
    


    path('folder/view/<int:folder_id>/', views.intranet_folder_list, name='intranet_folder_list'),
    
    path('home/file-attachment/', views.get_intranet_folder_files, name='get_intranet_folder_files'),
    path('folder/segment/<int:folder_id>/', views.get_intranet_folder_files, name='get_intranet_folder_files'),
    path('folder/create/', views.get_intranet_folder_files, name='get_intranet_folder_files'),
]
