from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status ,viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from doctors.models import Doctor , Schedule
from .serializers import ScheduleSerializer,DoctorSerializer,DoctorDetailSerializer


# class ScheduleAPI(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         doctor = Doctor.objects.get(user=request.user)

#         serializer = ScheduleSerializer(
#             data=request.data,
#             context={"doctor": doctor}
#         )

#         serializer.is_valid(raise_exception=True)

#         schedule = serializer.save(
#             doctor=doctor
#         )

#         return Response(
#             ScheduleSerializer(schedule).data,
#             status=status.HTTP_201_CREATED
#         )



from doctors.models import Doctor
from .models import Schedule
from .serializers import ScheduleSerializer


class DoctorScheduleViewSet(viewsets.ModelViewSet):
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated]

    def get_doctor(self):
        """Return the Doctor profile belonging to the logged-in user."""
        try:
            return Doctor.objects.get(user=self.request.user)
        except Doctor.DoesNotExist:
            raise PermissionDenied(
                "You must have a doctor profile to manage schedules."
            )

    def get_queryset(self):
        """Return only schedules belonging to this doctor."""
        doctor = self.get_doctor()
        return Schedule.objects.filter(doctor=doctor)

    def get_serializer_context(self):
        """Add the doctor to DRF's default serializer context."""
        context = super().get_serializer_context()
        context["doctor"] = self.get_doctor()
        return context

    def perform_create(self, serializer):
        """Automatically assign the schedule to this doctor."""
        serializer.save(doctor=self.get_doctor())




class DoctorListAPIView(APIView):
    def get(self,request):

        doctors = Doctor.objects.select_related("user").all()
        serializer = DoctorSerializer(doctors , many=True)

        return Response(serializer.data)

class DoctorDetailAPIView(APIView):
    def get(self,request,pk):
        try:
         doctor = Doctor.objects.select_related("user").get(pk=pk)
        except Doctor.DoesNotExist:  
           return Response(
                {"detail": "Doctor not found."},
                status=status.HTTP_404_NOT_FOUND,
           )
        
        serializer = DoctorDetailSerializer(doctor)
        return Response(
            serializer.data
        )