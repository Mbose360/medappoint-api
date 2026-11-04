from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Patient ,Appointment
from doctors.models import Schedule
from .serializers import AppointmentSerializer, AvailableSlotsSerializer,PatientAppointmentSerializer
from datetime import date, datetime, timedelta

class AppointmentCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            patient = Patient.objects.get(user=request.user)
        except Patient.DoesNotExist:
            return Response(
                {"detail": "Patient profile not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = AppointmentSerializer(data=request.data)

        if serializer.is_valid():
            appointment = serializer.save(patient=patient)

            return Response(
                AppointmentSerializer(appointment).data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class AvailableSlotsApiView(APIView):

    def get(self, request, pk):

        serializer = AvailableSlotsSerializer(
            data=request.query_params
        )
        serializer.is_valid(raise_exception=True)

        selected_date = serializer.validated_data["date"]

        day = selected_date.strftime("%A").upper()

        schedules = Schedule.objects.filter(
            doctor_id=pk,
            day_of_week=day
        )

        appointments = Appointment.objects.filter(
            doctor_id=pk,
            date=selected_date,
            status__in=["PENDING", "BOOKED"]
        )

        available_slots = []

        for schedule in schedules:

            current_time = datetime.combine(
                selected_date,
                schedule.start_time
            )

            end_time = datetime.combine(
                selected_date,
                schedule.end_time
            )

            while current_time + timedelta(minutes=30) <= end_time:

                slot_start = current_time.time()
                slot_end = (current_time + timedelta(minutes=30)).time()

                is_available = True

                for appointment in appointments:

                    if (
                        slot_start < appointment.end_time
                        and slot_end > appointment.start_time
                    ):
                        is_available = False
                        break

                if is_available:
                    available_slots.append(
                        slot_start.strftime("%H:%M")
                    )

                current_time += timedelta(minutes=30)

        return Response({
            "doctor": pk,
            "date": selected_date,
            "available_slots": available_slots
        })

class PatientAppointmentListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def  get(self,request):

        patient = get_object_or_404(Patient, user=request.user)
        appointments = appointments = Appointment.objects.filter(
         patient=patient
         ).select_related(
         "doctor",
         "doctor__user"
         ).order_by("-date", "-start_time")
        serializer = PatientAppointmentSerializer(appointments, many = True)

        return Response(
            serializer.data
        )

class CancelAppointmentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):

        patient = get_object_or_404(
            Patient,
            user=request.user
        )

        appointment = get_object_or_404(
            Appointment,
            pk=pk,
            patient=patient
        )

        if appointment.status not in [
            Appointment.AppointmentStatus.PENDING,
            Appointment.AppointmentStatus.BOOKED
        ]:
            return Response(
                {"detail": "This appointment cannot be cancelled."},
                status=status.HTTP_400_BAD_REQUEST
            )

        appointment.status = Appointment.AppointmentStatus.CANCELLED
        appointment.save(update_fields=["status"])

        serializer = PatientAppointmentSerializer(appointment)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )    