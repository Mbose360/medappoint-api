from django.urls import path , include
from . import views
from .views import LoginAPI
urlpatterns = [
   path('register/',views.RegisterAPI.as_view()),
   path('login/',LoginAPI.as_view())
   ]