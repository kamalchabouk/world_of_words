from django.urls import path
from django.urls import path, include
from . import views

app_name = "frontend"

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
]