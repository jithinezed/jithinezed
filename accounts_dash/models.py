from django.db import models
import datetime

# Create your models here.
class Target(models.Model):
    date = models.DateField( default=datetime.date.today)
    target =models.IntegerField(default=120000)
