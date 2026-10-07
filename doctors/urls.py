from django.urls import path
from .views import ScheduleAPI

urlpatterns = [
    path("doctor/schedule/", ScheduleAPI.as_view(), name="doctor-schedule"),
]