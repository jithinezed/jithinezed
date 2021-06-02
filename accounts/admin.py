from django.contrib import admin

# Register your models here.

from .models import Employee,EmployeeCertification,Client, SiteDetails,StaticImages,PushNotification,NotificationKeys
from vehicles.models import Vehicle,Fleet,TruckMaintananceReport,FuelExpense,ForkliftMaintananceReport,PreInspectionCheck
from roaster.models import Roaster
admin.site.register(Employee)

admin.site.register(EmployeeCertification)
admin.site.register(Client)
admin.site.register(Vehicle)
admin.site.register(Fleet)
admin.site.register(TruckMaintananceReport)
admin.site.register(FuelExpense)
admin.site.register(ForkliftMaintananceReport)
admin.site.register(PreInspectionCheck)
admin.site.register(Roaster)
admin.site.register(StaticImages)
admin.site.register(PushNotification)
admin.site.register(NotificationKeys)
admin.site.register(SiteDetails)


