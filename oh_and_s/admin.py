from django.contrib import admin
from .models import Notification,NotificationMembers,NewesMembers,News,SafetyData
admin.site.register(NotificationMembers)
admin.site.register(Notification)
admin.site.register(News)
admin.site.register(NewesMembers)
admin.site.register(SafetyData)