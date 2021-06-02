from django.db import models
from accounts.models import Employee

class TeamArchiveFolders(models.Model):
    name = models.CharField(max_length=300)
    def __str__(self): 
         return self.name

class TeamArchiveFiles(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    team_archive_folder = models.ForeignKey(TeamArchiveFolders, on_delete=models.CASCADE)
    file_item = models.FileField(upload_to='uploads/employee/file-archive/')