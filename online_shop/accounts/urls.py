from django.urls import path
from .views import RegistrationForm,EditProfileView,ProfileView

app_name = 'accounts'

urlpatterns = [

    path("register/", RegistrationForm.as_view(), name="register"),
    path('edit_profile/', EditProfileView.as_view(), name='edit_profile'),
    path('my_profile/', ProfileView.as_view(), name='my_profile'),

]
