from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager


class User(AbstractUser):
 class Role(models.TextChoices):
        PATIENT = "PATIENT", "Patient"
        DOCTOR = "DOCTOR", "Doctor"
 email = models.EmailField(unique=True)       
 role  = models.CharField( max_length=20 , choices=Role.choices)        
 phone_number = models.CharField( max_length=50 , blank= True)

 USERNAME_FIELD = "email"
 REQUIRED_FIELDS = []

 objects = UserManager()
 


