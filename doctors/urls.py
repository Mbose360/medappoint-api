from django.urls import path
# from .views import ScheduleAPI
from django.urls import include, path
from rest_framework.routers import DefaultRouter


from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import DoctorScheduleViewSet

router = DefaultRouter()

router.register(
    "doctor/schedule",
    DoctorScheduleViewSet,
    basename="doctor-schedule",
)

urlpatterns = [
    path("", include(router.urls)),
]