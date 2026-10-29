
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import DoctorScheduleApiView, DoctorScheduleViewSet,DoctorListAPIView,DoctorDetailAPIView

router = DefaultRouter()

router.register(
    "doctor/schedule",
    DoctorScheduleViewSet,
    basename="doctor-schedule",
)

urlpatterns = [
    path("", include(router.urls)),
    path('doctors/',DoctorListAPIView.as_view()),
    path('doctors/<int:pk>/',DoctorDetailAPIView.as_view()),
    path('doctors/<int:pk>/Schedule/',DoctorScheduleApiView.as_view())
]