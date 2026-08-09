from django.db import models

from doctors.models import Doctor
from patients.models import Patient

class Appointment(models.Model):
 class AppointmentStatus(models.TextChoices):
  PENDING   = 'PENDING','Pending',
  BOOKED    = "BOOKED", "Booked",
  CANCELLED = "CANCELLED", "Cancelled",
  COMPLETED =  "COMPLETED", "Completed",
  

 doctor = models.ForeignKey(
    Doctor,
    on_delete=models.CASCADE,
    related_name='appointments'
 )   
 patient = models.ForeignKey(
    Patient,
    on_delete=models.CASCADE,
    related_name="appointments"
    ) 
 date = models.DateField()
 start_time = models.TimeField()
 end_time = models.TimeField()
 created_at = models.DateTimeField(auto_now_add=True)
 status = models.CharField(
   max_length=20,
   choices=AppointmentStatus.choices,
   default=AppointmentStatus.PENDING
 )

