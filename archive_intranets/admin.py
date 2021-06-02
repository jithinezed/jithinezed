from django.contrib import admin
from .models import (
IntranetFolders,IntranetFolderFiles,IntranetSubFolders,IntranetSubFolderFiles,IntranetSubFolders2,IntranetSubFolder2Files,
IntranetBarAttachments)


# Register your models here.

admin.site.register(IntranetFolders)
admin.site.register(IntranetFolderFiles)
admin.site.register(IntranetSubFolders)
admin.site.register(IntranetSubFolderFiles)
admin.site.register(IntranetSubFolder2Files)
admin.site.register(IntranetSubFolders2)
admin.site.register(IntranetBarAttachments)

