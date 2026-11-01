
from django.urls import path

from .views import AppointmentCreateAPIView, AvailableSlotsApiView


urlpatterns = [
    path('appointment/',AppointmentCreateAPIView.as_view()),
    path("doctors/<int:pk>/available-slots/",AvailableSlotsApiView.as_view()),
]