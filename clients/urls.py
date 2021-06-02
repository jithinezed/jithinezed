from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('searchClient/all/<str:tab_type>/', views.searchClient, name='searchClient'),
    path('single/<str:client_id>/', views.getClientAPI, name='getClientAPI'),
    path('create/', views.createClientAPI, name='createClientAPI'),
    path('all/<str:sort_by>/<str:tab_type>/', views.sortedClientList, name='sortedClientList'),
    path('all/<str:tab_type>/', views.clientGetAllAPI, name='clientGetAllAPI'),
    path('delete/<str:client_id>/', views.clientDeleteAPI, name='clientDeleteAPI'),
    path('edit/<str:client_id>/', views.clientEditAPI, name='clientEditAPI'),
    path('emailAvail/', views.emailIdAvailability, name='emailIdAvailability'),
    path('clientIdAvail/', views.clientIdAvailability, name='clientIdAvailability'),
    path('files/<int:client_id>/', views.files_list, name='files_list'),
    # path('files/', views.files_list, name='files_list'),
    # path('files/<int:client_id>/<int:folder_id>/', views.files_list, name='files_list'),
    path('folder/', views.get_all_ClientFolders, name='get_all_ClientFolders'),
    # path('files/<int:client_id>/<int:folder_id>/', views.get_files, name='get_files')     

    # temporary client
    path('temporary-client/search/<str:tab_type>/', views.searchTemporary_client, name='searchTemporary_client'),
    path('temporary-client/', views.temporary_client, name='temporary_client'),
    path('temporary-client/list/<str:tab_type>/', views.getAllTemporary_client, name='getAllTemporary_client'), 
    path('temporary-client/list/<str:order_by>/<str:tab_type>/', views.getAllTemporary_client, name='getAllTemporary_client'), 
    path('temporary-client/<str:client_id>/', views.temporary_client, name='temporary_client'),
    path('temporary-client/search/<str:sort_by>/<str:tab_type>/', views.sortedTemporaryClientList, name='sortedTemporaryClientList'),
    
    path('file/delete/<int:file_id>/', views.delete_client_files, name='delete_client_files'),
   
    path('detail/crud/<sited_id>/', views.Site_details, name='Site_details'),
    path('detail/crud/', views.Site_details, name='Site_details'),
]