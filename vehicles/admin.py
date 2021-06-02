from django.contrib import admin
from .models import CarMaintananceReport, VehicleFile
from .models import VehicleFolder,PostImage,VehicleImages,VehicleImage,CarMaintananceReport

# Register your models here.
admin.site.register(VehicleFile)
admin.site.register(VehicleFolder)
admin.site.register(VehicleImages)
admin.site.register(PostImage)
admin.site.register(VehicleImage)
admin.site.register(CarMaintananceReport)

