from django.db import models
from  accounts.models import Client,Employee
from archive_intranets.models import IntranetArchiveFiles,IntranetFolderFiles
import uuid
import datetime
from datetime import datetime
from drive.models import DriveFolder,Files
        

class EmailBcc(models.Model):
    bcc = models.EmailField(null=True,blank=True)
class EmailCc(models.Model):
    cc = models.EmailField(null=True,blank=True)    
class Quote(models.Model):
    tab_choice = (
    ("waste", "waste"),
    ("hills", "hills"),
    ("pumps", "pumps"),
    ("destruction", "destruction"),
    ("all","all"))

    tab_type = models.CharField(max_length=50,
    choices=tab_choice,
    default="waste")
    uuid = models.UUIDField(
         default = uuid.uuid4)
         
    template = models.FileField(upload_to='quote/archive/' ,null=True,blank=True) 
    template_html_send = models.TextField(null=True, blank=True)
    template_html_receive = models.TextField(null=True, blank=True)
    template_receive = models.FileField(upload_to='quote/archive/' ,null=True,blank=True)  

    template_name = models.CharField(max_length=200,null=True,blank=True)
    reoccurring = models.BooleanField(default=False) 
    quote_attach_files_in  = models.ManyToManyField(Files,related_name="quote_attach_file", blank=True)
    # quote_attach_files = models.ManyToManyField(QuoteAttachTemplates,related_name="quote_attach_files", blank=True)
    auto_create = models.IntegerField(null = True, blank =True)
    status = models.CharField(max_length =50,default = "pending")
    url = models.CharField(max_length = 250,null = True,blank = True)
    employee = models.ForeignKey(Employee, on_delete =models.CASCADE)
    won_reject_date = models.DateTimeField(default=datetime.now, blank=True)
    date = models.DateTimeField(default=datetime.now, blank=True)
    client = models.ForeignKey(Client,on_delete=models.CASCADE)
    paid_status = models.CharField(max_length =50,default = "un-paid")
    job_type = models.CharField(max_length=200, null=True,blank=True)
    invoice_amt = models.CharField(max_length = 200, null = True,blank = True)
    company_name = models.CharField(max_length = 200, null = True,blank = True)
    amount = models.CharField(max_length = 200,default="0")
    mail_bcc  = models.ManyToManyField(EmailBcc,related_name="mail_bcc", blank=True)
    mail_cc  = models.ManyToManyField(EmailCc,related_name="mail_cc", blank=True)
    mail_subject = models.CharField(max_length=500,null=True,blank=True)
    mail_body = models.CharField(max_length=1500,null=True,blank=True)
    safety_data = models.FileField(upload_to='quote/archive/' ,null=True,blank=True) 
    safety_data_html_send = models.TextField(null=True, blank=True)
    created_date_time = models.DateTimeField(auto_now_add=True, blank=True)
    edited_date_time = models.DateTimeField(auto_now=True, blank=True)
    sales_team_review = models.BooleanField(default=False)
    

    class Meta:
        ordering = ['-created_date_time', '-id']
#WHS
class Jobfolder(models.Model):
    name = models.CharField(max_length=300)
    def __str__(self): 
         return self.name

class JobFile(models.Model):
    file = models.FileField(upload_to='uploads/temporary_client/whs/', max_length=254)

class JobImages(models.Model):
    attachments = models.ManyToManyField(JobFile, related_name="job_file", blank=True)
    employee = models.ForeignKey(Employee,on_delete =models.CASCADE) 
    folder = models.ForeignKey(Jobfolder,on_delete=models.CASCADE)
    job_id = models.ForeignKey(Quote,on_delete=models.CASCADE) 
    
class DummyTemplate(models.Model):
    tab_choice = (
    ("waste", "waste"),
    ("hills", "hill"),
    ("pumps", "pumps"),
    ("destruction", "destruction"))
    
    tab_type = models.CharField(max_length=50,
    choices=tab_choice,
    default="waste")
    template_content = models.TextField()
    tamplate_name = models.CharField(max_length=100,null=True,blank=True)

    created_date_time = models.DateTimeField(auto_now_add=True, blank=True)
    edited_date_time = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        ordering = ['-created_date_time', '-id']


class SalesFolders(models.Model):
    tab_choice = (
    ("waste", "waste"),
    ("hills", "hills"),
    ("pumps", "pumps"),
    ("destruction", "destruction"))

    tab_type = models.CharField(max_length=50,
    choices=tab_choice,
    default="waste")

    folder_choice = (
    ("Description of waste", "Description of waste"),
    ("Power point", "Power point"),
    ("Marketing", "Marketing"),
    ("Pricing", "Pricing"),
    ("Tender", "Tender"),
    ("others", "others"))

    Sales_folder_list = models.CharField(max_length=50,
    choices=folder_choice,
    default="others")
    
    name = models.CharField(max_length=100,null=True,blank=True)

    created_date_time = models.DateTimeField(auto_now_add=True, blank=True)
    edited_date_time = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        ordering = ['-created_date_time', '-id']

class SalesFolderFiles(models.Model):
    folder = models.ForeignKey(SalesFolders, on_delete=models.CASCADE)   
    attachment = models.FileField(upload_to='uploads/sales/file-archive/', max_length=254,null=True,blank=True) 
    quote = models.ForeignKey(Quote,on_delete=models.CASCADE,null=True,blank=True) 
    created_date_time = models.DateTimeField(auto_now_add=True, blank=True)
    edited_date_time = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        ordering = ['-created_date_time', '-id']    


class Products(models.Model):
    name = models.CharField(max_length=200)
    created_date_time = models.DateTimeField(auto_now_add=True, blank=True)
    edited_date_time = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        ordering = ['-created_date_time', '-id']  

class UserQuoteTemplate(models.Model):
    send_by = models.ForeignKey(Employee,on_delete=models.CASCADE,null=True,blank=True) 
    send_to= models.ForeignKey(Client,on_delete=models.CASCADE,null=True,blank=True) 
    template_url=models.CharField(max_length = 250,null = True,blank = True)

    template = models.TextField(null=True, blank=True)
  
    created_date_time = models.DateTimeField(auto_now_add=True, blank=True)
    edited_date_time = models.DateTimeField(auto_now=True, blank=True)
    tab_type = models.CharField(max_length=20,default='waste',null=True, blank=True)

    class Meta:
        ordering = ['-created_date_time', '-id']    


class TemplateDraft(models.Model):
    created_by = models.ForeignKey(Employee,on_delete=models.CASCADE,null=True,blank=True) 
    client = models.ForeignKey(Client,on_delete=models.CASCADE,null=True,blank=True) 
    template = models.TextField(null=True, blank=True)
    template_receive_response = models.FileField(upload_to='quote/archive/' ,null=True,blank=True)  
    created_date_time = models.DateTimeField(auto_now_add=True, blank=True)
    edited_date_time = models.DateTimeField(auto_now=True, blank=True)
    tab_type = models.CharField(max_length=20,default='waste',null=True, blank=True)

    class Meta:
        ordering = ['-created_date_time', '-id']            

class UserSafetyData(models.Model):
    send_by = models.ForeignKey(Employee,on_delete=models.CASCADE,null=True,blank=True) 
    send_to = models.ForeignKey(Client,on_delete=models.CASCADE,null=True,blank=True) 
    safety_data = models.TextField(null=True, blank=True)
    created_date_time = models.DateTimeField(auto_now_add=True, blank=True)
    edited_date_time = models.DateTimeField(auto_now=True, blank=True)
    safety_data_url = models.CharField(max_length = 250,null = True,blank = True)
    tab_type = models.CharField(max_length=20,default='waste',null=True, blank=True)

    class Meta:
        ordering = ['-created_date_time', '-id'] 

class MailSignature(models.Model):
    signature = models.TextField(null=True, blank=True)

    created_date_time = models.DateTimeField(auto_now_add=True, blank=True)
    edited_date_time = models.DateTimeField(auto_now=True, blank=True)
    name =  models.ForeignKey(Employee,on_delete=models.CASCADE,null=True,blank=True) 

    class Meta:
        ordering = ['-created_date_time', '-id'] 

#model used to store dummy templates(8)
class QuoteAttachTemplates(models.Model):
    template = models.TextField(null=True, blank=True)
    name = models.CharField(max_length=100,null=True, blank=True,default="attach_template")
    editable = models.BooleanField(default=False)
    created_date_time = models.DateTimeField(auto_now_add=True, blank=True)
    edited_date_time = models.DateTimeField(auto_now=True, blank=True)
    tab_type = models.CharField(max_length=20,default='waste',null=True, blank=True)
    quote= models.ForeignKey(Files,on_delete=models.CASCADE,null=True,blank=True) 

    class Meta:
        ordering = ['-created_date_time', '-id']            


class TypeOfWaste(models.Model):
 
    
    w_type = models.CharField(max_length=200,null=True,blank=True)
  
    created_date_time = models.DateTimeField(auto_now_add=True, blank=True)
    edited_date_time = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        ordering = ['-created_date_time', '-id']        

class LoggingInfo(models.Model):
    quote= models.ForeignKey(Quote,on_delete=models.CASCADE,null=True,blank=True) 
    tab_type = models.CharField(max_length=20,default='waste',null=True, blank=True)
    employee= models.ForeignKey(Employee,on_delete=models.CASCADE,null=True,blank=True) 
    message= models.TextField(null=True, blank=True)   
    created_date_time = models.DateTimeField(auto_now_add=True, blank=True)
    edited_date_time = models.DateTimeField(auto_now=True, blank=True)
    class Meta:
        ordering = ['-created_date_time', '-id']    

class ClientQuoteAttachmentResponses(models.Model):
    quote_data=models.ForeignKey(Quote,on_delete=models.CASCADE,null=True,blank=True) 
    template_content= models.TextField(null=True, blank=True)
    quote_attach_template_response=models.ForeignKey(Files,on_delete=models.CASCADE,null=True,blank=True) 
    template_receive_response = models.FileField(upload_to='quote/archive/' ,null=True,blank=True)  
    created_date_time = models.DateTimeField(auto_now_add=True, blank=True)
    edited_date_time = models.DateTimeField(auto_now=True, blank=True)
    

    class Meta:
        ordering = ['-created_date_time', '-id']                