from django.contrib import admin
from .models import ClientFolder,ClientFile,ClientImages,PostImage

# Register your models here.
 
admin.site.register(ClientFile)
admin.site.register(ClientFolder)
admin.site.register(ClientImages)
admin.site.register(PostImage)
