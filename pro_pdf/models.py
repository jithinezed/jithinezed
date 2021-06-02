from django.db import models

# Create your models here.

class Template(models.Model):
    tab_choice = (
    ("waste", "waste"),
    ("hill", "hill"),
    ("pump", "pump"),
    ("destruction", "destruction"))

    tab_type = models.CharField(max_length=50,
    choices=tab_choice,
    default="waste")
    html_content = models.TextField()
    template_name = models.CharField(max_length=100,null=True,blank=True)
class EditedForm(models.Model):
    html_content = models.TextField(null=True,blank=True)
    form_name = models.CharField(max_length=100,null=True,blank=True)
    files = models.FileField(upload_to='uploads/template/',null=True,blank=True)
    