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

