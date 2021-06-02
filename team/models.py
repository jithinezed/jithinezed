from django.db import models
from accounts.models import Employee
#   
# from django_mysql.models import JSONField, Model


class EmployeeFolder(models.Model):
    name = models.CharField(max_length=300,null=True,blank=True)
    visibility = models.BooleanField(default=True,null=True,blank=True)
    accessibility = models.BooleanField(default=True,null=True,blank=True)
    created_by =models.ForeignKey(Employee,on_delete=models.CASCADE,null=True,blank=True)
    created_date_time = models.DateTimeField(auto_now_add=True, blank=True)
    edited_date_time = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        ordering = ['-created_date_time', '-id']
class EmployeeFile(models.Model):
    active_status = models.BooleanField(default=True)
    homepage_visibility = models.BooleanField(default=False)
    expiry_date = models.DateField(null=True,blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    employee_folder = models.ForeignKey(EmployeeFolder, on_delete=models.CASCADE)
    file_item = models.FileField(upload_to='uploads/employee/data/',null=True, blank=True)
    alert_before = models.DateField(null=True,blank=True)

    created_date_time = models.DateTimeField(auto_now_add=True, blank=True)
    edited_date_time = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        ordering = ['-created_date_time', '-id']  

class PostImage(models.Model):
    file = models.FileField(upload_to='uploads/client/images/', max_length=254)
    file_name = models.CharField(max_length=500,null=True,blank=True)
    
    created_date_time = models.DateTimeField(auto_now_add=True, blank=True)
    edited_date_time = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        ordering = ['-created_date_time', '-id']  

class EmployeeImages(models.Model):
    attachments = models.ManyToManyField(PostImage, related_name="post_image", blank=True)
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE)
    folder = models.ForeignKey(EmployeeFolder,on_delete=models.CASCADE)
    expiry_date = models.DateField(null=True,blank=True)
    alert_before = models.DateField(null=True,blank=True)

    created_date_time = models.DateTimeField(auto_now_add=True, blank=True)
    edited_date_time = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        ordering = ['-created_date_time', '-id']

def my_default():
    return {'goods': 'Update Dangerous goods data'}  
class SafteyInfo(models.Model):
    name = models.CharField(max_length=200,null=True,blank=True)
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE,null=True,blank=True)
    data = models.JSONField(null=True,default=my_default)

