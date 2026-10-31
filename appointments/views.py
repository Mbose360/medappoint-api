from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Patient
from .serializers import AppointmentSerializer


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