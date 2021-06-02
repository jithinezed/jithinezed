from django.db import models
from accounts.models import Employee,Client

# Create your models here.
class Notification_hub(models.Model):
    model_choice = (
    ("client", "client"),
    ("vehicle", "vehicle"),
    ("schedule", "schedule"),
    ("employee", "employee"),
    ("quote", "quote"),
    ("job", "job"),
    ("fork_lift_report", "fork_lift_report"),
    ("truck_report", "truck_report"),
    ("pre_inspection", "pre_inspection"),
    
    )
    model_type = models.CharField(max_length=100,
                  choices=model_choice,
                  default="client")

    type_choice = (
    ("added", "added"),
    ("deleted", "deleted"),
    ("edited", "edited"),
    ("accepted", "accepted"),
    ("rejected", "rejected"),
    )

    type = models.CharField(max_length=100,
                  choices=type_choice,
                  default="added")

    reference_id = models.IntegerField()
    send_to_team =models.ManyToManyField(Employee,blank=True)    
    send_to_client =models.ManyToManyField(Client,blank=True)          

    created_date_time = models.DateTimeField(auto_now_add=True, blank=True)
    edited_date_time = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        ordering = ['-created_date_time', '-id']    