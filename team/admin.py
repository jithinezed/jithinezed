from django.contrib import admin
from .models import EmployeeFile,EmployeeFolder,PostImage,EmployeeImages,SafteyInfo
# Register your models here.

admin.site.register(EmployeeFolder)
admin.site.register(EmployeeFile)
admin.site.register(EmployeeImages)
admin.site.register(PostImage)
admin.site.register(SafteyInfo)
