from django.db import models
from medical_app import settings

class Doctor(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="doctor_profile"
    )

    profile_pic =models.ImageField(
        upload_to='profile_pics/',   # folder inside MEDIA_ROOT
        null=True,
        blank=True,
        default='profile_pics/default.jpg')
    speciality = models.CharField(max_length=100)
    biography = models.TextField (blank=True)
    location  = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)

    
# models.py

from django.db import models
from django.conf import settings


class Schedule(models.Model):

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE
    )
    class Day(models.TextChoices):
      Sunday   = "SUNDAY","Sunday"
      Monday   = "MONDAY","Monday"
      Tuesday = "TUESDAY", "Tuesday"
      Wednesday = "WEDNESDAY", "Wednesday"
      Thursday  = "THURSDAY","Thursday"
      Friday    = "FRIDAY","Friday"
      Saturday  = "SATURDAY","Saturday"

    day_of_week  = models.CharField(
     max_length=20,
     choices= Day.choices,
     default= Day.Sunday     
    ) 
    start_time = models.TimeField()
    end_time   = models.TimeField()    
    
      

    def __str__(self):
        return f"{self.doctor} - {self.day_of_week}"
