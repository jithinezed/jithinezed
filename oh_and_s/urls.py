from django.urls import path, include
from . import views

urlpatterns = [
    path('notification/create/', views.notification, name='notification'),
    path('notification/view/<int:page_number>/', views.notification, name='notification'),
    path('notification/delete/<int:notification_id>/', views.notification, name='notification'),
    path('news/create/', views.Team_news, name='Team_news'),
    path('news/view/<int:page_number>/', views.Team_news, name='Team_news'),
    path('news/delete/<int:news_id>/', views.Team_news, name='Team_news'),
    path('news/edit/<int:news_id>/', views.Team_news, name='Team_news'),

    path('folder/view/', views.folder_list, name='folder_list'),
    path('notification/status/<int:notification_id>/', views.notification_read_status, name='notification_read_status'),
    path('news/status/<int:news_id>/', views.news_read_status, name='news_read_status'),
    # path('folder/intranet/create/', views.folder_list, name='folder_list'),
    # path('folder/intranet/delete/<int:folder_id>/', views.folder_list, name='folder_list'),
    # path('folder/intranet/edit/<int:folder_id>/', views.folder_list, name='folder_list'),
    # path('intranet/file/create/', views.intranet_files, name='intranet_files'),
    # path('intranet/file/delete/<int:file_id>/', views.intranet_files, name='intranet_files'),
    
# #sub foldes and files
    
#     path('intranet/sub/folder/create/', views.intranet_sub_folder, name='intranet_sub_folder'),
#     path('intranet/sub/folder/delete/<int:sub_folder_id>/', views.intranet_sub_folder, name='intranet_sub_folder'),
#     path('intranet/sub/folder/edit/<int:sub_folder_id>/', views.intranet_sub_folder, name='intranet_sub_folder'),
#     path('intranet/sub/file/create/', views.intranet_sub_folder_files, name='intranet_sub_folder_files'),
#     path('intranet/sub/file/delete/<int:file_id>/', views.intranet_sub_folder_files, name='intranet_sub_folder_files'), 
#     path('intranet/sub1/folder/create/', views.intranet_sub1_folder, name='intranet_sub1_folder'),
#     path('intranet/sub1/folder/delete/<int:sub1_folder_id>/', views.intranet_sub1_folder, name='intranet_sub1_folder'),
#     path('intranet/sub1/folder/edit/<int:sub1_folder_id>/', views.intranet_sub1_folder, name='intranet_sub1_folder'),
#     path('intranet/sub1/file/create/', views.intranet_sub1_folder_files, name='intranet_sub1_folder_files'),
#     path('intranet/sub1/file/delete/<int:file_id>/', views.intranet_sub1_folder_files, name='intranet_sub1_folder_files'),       

    path('drive/',include('drive.urls')),
    path('folder/intranet/create/', views.folder_list, name='folder_list'),
    path('folder/segment/list/<int:folder_id>/', views.folder_segment_list, name='folder_segment_list'),
    path('safety-data/', views.safety_data, name='safety_data'),

    path('safety-data/<int:safety_data_id>/', views.safety_data, name='safety_data'),
    
    
]
