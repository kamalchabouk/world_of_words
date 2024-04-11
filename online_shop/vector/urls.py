from django.urls import path
from . import views

app_name = 'vector' 

urlpatterns = [
    path('search/',views.search , name='search'),
]