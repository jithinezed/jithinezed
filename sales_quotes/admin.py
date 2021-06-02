from django.contrib import admin
from .models import (Quote,JobFile,Jobfolder,JobImages,UserQuoteTemplate,Products,TemplateDraft,QuoteAttachTemplates,TypeOfWaste,
SalesFolderFiles,SalesFolders,MailSignature,LoggingInfo,ClientQuoteAttachmentResponses)
# Register your models here.

admin.site.register(Quote)
admin.site.register(JobImages)
admin.site.register(Jobfolder)
admin.site.register(JobFile)
admin.site.register(SalesFolders)
admin.site.register(SalesFolderFiles)
admin.site.register(UserQuoteTemplate)
admin.site.register(Products)
admin.site.register(TemplateDraft)
admin.site.register(MailSignature)
admin.site.register(QuoteAttachTemplates)
admin.site.register(TypeOfWaste)
admin.site.register(LoggingInfo)
admin.site.register(ClientQuoteAttachmentResponses)









