from django.urls import path
from .views import filter_view


app_name = 'filter'

urlpatterns = [
    path('', filter_view, name='filter'),
]