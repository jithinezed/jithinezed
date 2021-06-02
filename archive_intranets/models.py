from django.db import models
from accounts.models import Client,Employee
class Inside_InnerFolder(models.Model):
    # intranet_archive_folder = models.ForeignKey(Inner_IntranetArchiveFolders, on_delete=models.CASCADE)
    inner_folder=models.BooleanField(default=False)
    name = models.CharField(max_length=300)
    sales_tab = models.BooleanField(default=True)
    generate_qoute = models.BooleanField(default=True)
    attach_quote = models.BooleanField(default=True)
    file_status = models.BooleanField(default=False)
    sub_folder_status = models.BooleanField(default=False)
    def __str__(self): 
         return self.name    
class Inside_Inner_File_Upload(models.Model):
    file = models.FileField(upload_to='uploads/intranet/file-archive/', max_length=254)

class Inside_Inner_IntranetArchiveFiles(models.Model):
    # client = models.ForeignKey(Client, on_delete=models.CASCADE)
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE,null=True,blank=True)
    inside_Inner_intranet_archive_folder = models.ForeignKey(Inside_InnerFolder, on_delete=models.CASCADE)
    attachments = models.ManyToManyField(Inside_Inner_File_Upload, related_name="Inside_Inner_File_Upload", blank=True)
    file_name = models.CharField(max_length=200,null=True,blank=True)   
       

class InnerFolder(models.Model):
    # intranet_archive_folder = models.ForeignKey(Inner_IntranetArchiveFolders, on_delete=models.CASCADE)
    inner_folder=models.BooleanField(default=False)
    inside_inner_folder_content = models.ManyToManyField(Inside_InnerFolder,related_name="inside_inner_folder_content", blank=True)
    name = models.CharField(max_length=300)
    sales_tab = models.BooleanField(default=True)
    generate_qoute = models.BooleanField(default=True)
    attach_quote = models.BooleanField(default=True)
    file_status = models.BooleanField(default=False)
    sub_folder_status = models.BooleanField(default=False)
    def __str__(self): 
         return self.name   

class Inner_File_Upload(models.Model):
    file = models.FileField(upload_to='uploads/intranet/file-archive/', max_length=254)

class Inner_IntranetArchiveFiles(models.Model):
    # client = models.ForeignKey(Client, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE,null=True,blank=True)
    inner_intranet_archive_folder = models.ForeignKey(InnerFolder, on_delete=models.CASCADE)
    attachments = models.ManyToManyField(Inner_File_Upload, related_name="Inner_File_Upload", blank=True)
    file_name = models.CharField(max_length=200,null=True,blank=True)    


class IntranetArchiveFolders(models.Model):
    inner_folder=models.BooleanField(default=False)
    inner_folder_content = models.ManyToManyField(InnerFolder,related_name="InnerFolder", blank=True)
    name = models.CharField(max_length=300)
    sales_tab = models.BooleanField(default=True)
    generate_qoute = models.BooleanField(default=True)
    attach_quote = models.BooleanField(default=True)
    file_status = models.BooleanField(default=False)
    sub_folder_status = models.BooleanField(default=False)
    def __str__(self): 
         return self.name
class Intranet_File_Upload(models.Model):
    file = models.FileField(upload_to='uploads/intranet/file-archive/', max_length=254) 

class IntranetArchiveFiles(models.Model):
    # client = models.ForeignKey(Client, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE,null=True)
    intranet_archive_folder = models.ForeignKey(IntranetArchiveFolders, on_delete=models.CASCADE)
    attachments = models.ManyToManyField(Intranet_File_Upload, related_name="Intranet_File_Upload", blank=True)
    file_name = models.CharField(max_length=200,null=True,blank=True)



class IntranetFolders(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)

    tab_choice = (
    ("waste", "waste"),
    ("hills", "hills"),
    ("pumps", "pumps"),
    ("destruction", "destruction"))

    tab_type = models.CharField(max_length=50,
    choices=tab_choice,
    default="waste")
    sales_tab = models.BooleanField(default=True)
    generate_quote = models.BooleanField(default=True)
    attach_quote = models.BooleanField(default=True)
    intranet =  models.BooleanField(default=True)
    templates =  models.BooleanField(default=False  )
class IntranetFolderFiles(models.Model):
    folder = models.ForeignKey(IntranetFolders, on_delete=models.CASCADE)   
    attachment = models.FileField(upload_to='uploads/intranet/file-archive/', max_length=254,null=True,blank=True) 
    quote_attach_template = models.TextField(null=True, blank=True)
    template_name = models.CharField(max_length=100,null=True,blank=True)
class IntranetSubFolders(models.Model):
    folder = models.ForeignKey(IntranetFolders, on_delete=models.CASCADE)  
    name = models.CharField(max_length=100,null=True,blank=True)

class IntranetSubFolderFiles(models.Model):
    folder = models.ForeignKey(IntranetSubFolders, on_delete=models.CASCADE)
    attachment = models.FileField(upload_to='uploads/intranet/file-archive/', max_length=254,null=True,blank=True)

class IntranetSubFolders2(models.Model):
    folder = models.ForeignKey(IntranetSubFolders, on_delete=models.CASCADE)  
    name = models.CharField(max_length=100,null=True,blank=True)
    sales_tab = models.BooleanField(default=True)
    generate_qoute = models.BooleanField(default=True)
    attach_quote = models.BooleanField(default=True)
    intranet =  models.BooleanField(default=True)

class IntranetSubFolder2Files(models.Model):
    folder = models.ForeignKey(IntranetSubFolders2, on_delete=models.CASCADE)
    attachment = models.FileField(upload_to='uploads/intranet/file-archive/', max_length=254,null=True,blank=True)    
    
class IntranetBarAttachments(models.Model):
    file = models.FileField(upload_to='uploads/intranet/file-archive/',max_length=254,null=True,blank=True)
    folder_name = models.CharField(max_length=100,null=True,blank=True)


