from django.db import models
from accounts.models import Employee

# Create your models here.

class NotificationMembers(models.Model):
    member_id = models.ForeignKey(Employee,on_delete = models.CASCADE)
    read_status = models.BooleanField(default=False)
    created_date_time = models.DateTimeField(auto_now_add=True, blank=True)
    edited_date_time = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        ordering = ['-created_date_time', '-id']
class Notification(models.Model):
    title = models.CharField(max_length=500,null=True,blank=True)
    description = models.CharField(max_length = 500,null=True,blank=True)
    members = models.ManyToManyField(NotificationMembers,blank=True)
    file_attachment = models.FileField(upload_to='uploads/notification/',null=True, blank=True)
    created_by = models.ForeignKey(Employee,on_delete = models.CASCADE,null=True, blank=True)

   
    edited_date_time = models.DateTimeField(auto_now=True, blank=True)
    created_date_time = models.DateTimeField(auto_now_add=True, null=True,blank=True)
    class Meta:
        ordering = ['-created_date_time', '-id']

class NewesMembers(models.Model):
    member_id = models.ForeignKey(Employee,on_delete = models.CASCADE, null=True, blank=True)
    read_status = models.BooleanField(default=False)

    created_date_time = models.DateTimeField(auto_now_add=True, blank=True)
    edited_date_time = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        ordering = ['-created_date_time', '-id']
class News(models.Model):
    title = models.CharField(max_length=500,null=True,blank=True)
    description = models.CharField(max_length = 500,null=True,blank=True)
    news_member = models.ManyToManyField(NewesMembers,blank=True)
    file_attachment = models.FileField(upload_to='uploads/news/',null=True, blank=True)
    created_by = models.ForeignKey(Employee,on_delete = models.CASCADE,null=True,blank=True)

    
    edited_date_time = models.DateTimeField(auto_now=True, blank=True)
    created_date_time = models.DateTimeField(auto_now_add=True, null=True,blank=True)
    class Meta:
        ordering = ['-created_date_time', '-id']        

class SafetyData(models.Model):   
    lti_mtd = models.CharField(max_length = 500,null=True,blank=True)
    lti_ytd = models.CharField(max_length = 500,null=True,blank=True)
    mti_mtd = models.CharField(max_length = 500,null=True,blank=True)
    mti_ytd = models.CharField(max_length = 500,null=True,blank=True)
    fti_mtd = models.CharField(max_length = 500,null=True,blank=True)
    fti_ytd = models.CharField(max_length = 500,null=True,blank=True)
    notFault_mtd = models.CharField(max_length = 500,null=True,blank=True)
    notFault_ytd = models.CharField(max_length = 500,null=True,blank=True)
    atFault_ytd = models.CharField(max_length = 500,null=True,blank=True)
    atFault_mtd = models.CharField(max_length = 500,null=True,blank=True)
  

    edited_date_time = models.DateTimeField(auto_now=True, blank=True)
    created_date_time = models.DateTimeField(auto_now_add=True, null=True,blank=True)
    class Meta:
        ordering = ['-created_date_time', '-id']   