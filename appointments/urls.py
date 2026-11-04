
from django.urls import path

from .views import AppointmentCreateAPIView, AvailableSlotsApiView,PatientAppointmentListAPIView,CancelAppointmentAPIView


urlpatterns = [
    path('appointment/',AppointmentCreateAPIView.as_view()),
    path("doctors/<int:pk>/available-slots/",AvailableSlotsApiView.as_view()),
    path("appointments/my/",PatientAppointmentListAPIView.as_view(),name="my-appointments"),
    path("appointments/<int:pk>/cancel/",CancelAppointmentAPIView.as_view(),name="cancel-appointment")
]