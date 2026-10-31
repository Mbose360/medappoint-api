from datetime import datetime, timedelta

from django.utils import timezone
from rest_framework import serializers

from .models import Appointment, Doctor

from django.utils import timezone
from rest_framework import serializers

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = [
            "id",
            "doctor",
            "date",
            "start_time",
            "end_time",
            "status",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "end_time",
            "status",
            "created_at",
        ]

    def validate_date(self, value):
         if value < timezone.localdate():
            raise serializers.ValidationError(
                "You cannot book an appointment in the past."
            )
         return value





    def validate(self, attrs):
        doctor = attrs["doctor"]
        date = attrs["date"]
        start_time = attrs["start_time"]

        # Check that the appointment is in the future
        start_datetime = datetime.combine(date, start_time)
        now = timezone.localtime()

        if start_datetime <= now.replace(tzinfo=None):
            raise serializers.ValidationError(
                "The appointment must be in the future."
            )

        # Calculate the end time (30-minute appointment)
        end_time = (
            datetime.combine(date, start_time)
            + timedelta(minutes=30)
        ).time()

        # Check for overlapping appointments
        appointments = Appointment.objects.filter(
            doctor=doctor,
            date=date,
            status__in=[
                Appointment.AppointmentStatus.PENDING,
                Appointment.AppointmentStatus.BOOKED,
            ],
        )

        for appointment in appointments:
            if (
                start_time < appointment.end_time
                and end_time > appointment.start_time
            ):
                raise serializers.ValidationError(
                    "The doctor already has an appointment at that time."
                )

        attrs["end_time"] = end_time
        return attrs
        

   