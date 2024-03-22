# api/urls.py
from django.urls import path
from .views import ContactListCreate, ContactDetail, GenreList, GenreDetail, APIRoot

urlpatterns = [
    path('', APIRoot.as_view(), name='api-root'), 
    path('contacts/', ContactListCreate.as_view(), name='contact-list'),
    path('contacts/<int:pk>/', ContactDetail.as_view(), name='contact-detail'),
    path('genres/', GenreList.as_view(), name='genre-list'),
    path('genres/<int:pk>/', GenreDetail.as_view(), name='genre-detail'),
]
