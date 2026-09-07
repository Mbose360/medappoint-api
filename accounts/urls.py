from django.urls import path , include
from . import views

urlpatterns = [
   path('register/',views.RegisterAPI.as_view()),
   ]