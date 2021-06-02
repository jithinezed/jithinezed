"""enviro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/accounts/', include('accounts.urls'), name='accounts-api-v1-parent'),
    path('api/v1/vehicles/', include('vehicles.urls'), name='vehicles-api-v1-parent'),
    path('api/v1/team/', include('team.urls'), name='team-api-v1-parent'),
    path('api/v1/clients/', include('clients.urls'), name='clients-api-v1-parent'),
    path('api/v1/roaster/', include('roaster.urls'), name='roaster-api-v1-parent'),
    path('api/v1/email_service/', include('email_service.urls'), name='email_service-api-v1-parent'),
    path('api/v1/sales/', include('sales_quotes.urls'), name='sales-api-v1-parent'),
    path('api/v1/intranet_archive/', include('archive_intranets.urls'), name='intranet_archive-api-v1-parent'),
    path('api/v1/pro-pdf/', include('pro_pdf.urls'), name='pro_pdf-api-v1-parent'),
    path('api/v1/home/', include('home.urls'), name='home-api-v1'),
    # path('api/v1/ohs/', include('oh_ands.urls'), name='ohs-api-v1'),
    path('api/v1/oh_and_s/', include('oh_and_s.urls'), name='oh_and_s-api-v1'),
    path('api/v1/drive/', include('drive.urls'), name='drive-api-v1'),
    path('api/v1/notification/', include('notification.urls'), name='notification-api-v1'),
    path('api/v1/jobs/', include('jobs.urls'), name='jobs-api-v1'),
    path('api/v1/schedule/', include('schedules.urls'), name='schedule-api-v1'),
    path('api/v1/accounts_files/', include('accounts_file.urls'), name='accounts_file-api-v1'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

