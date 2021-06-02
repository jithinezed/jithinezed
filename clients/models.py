from django.db import models
from accounts.models import Client
import datetime

# Create your models here.
class ClientFolder(models.Model):
    name = models.CharField(max_length=300)
    def __str__(self): 
         return self.name



class ClientFile(models.Model):
    active_status = models.BooleanField(default=True)
    # homepage_visibility = models.BooleanField(default=False)
    expiry_date = models.DateField(null=True,blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    client_folder = models.ForeignKey(ClientFolder, on_delete=models.CASCADE)
    file_item = models.FileField(upload_to='uploads/employee/data/',null=True, blank=True)

class PostImage(models.Model):
   file = models.FileField(upload_to='uploads/client/images/', max_length=254)
#    created_date_time = models.DateField(default=datetime.date.today)

class ClientImages(models.Model):
        attachments = models.ManyToManyField(PostImage, related_name="post_image", blank=True)
        client = models.ForeignKey(Client,on_delete=models.CASCADE)
        folder = models.ForeignKey(ClientFolder,on_delete=models.CASCADE)   