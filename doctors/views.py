from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from doctors.models import Doctor
from .serializers import ScheduleSerializer


class ScheduleAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        doctor = Doctor.objects.get(user=request.user)

        serializer = ScheduleSerializer(
            data=request.data,
            context={"doctor": doctor}
        )

        serializer.is_valid(raise_exception=True)

        schedule = serializer.save(
            doctor=doctor
        )

        return Response(
            ScheduleSerializer(schedule).data,
            status=status.HTTP_201_CREATED
        )