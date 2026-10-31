
from django.urls import path

from .views import AppointmentCreateAPIView


urlpatterns = [
    path('appointment/',AppointmentCreateAPIView.as_view())
]