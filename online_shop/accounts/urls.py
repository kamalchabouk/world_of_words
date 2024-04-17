from django.urls import path
from .views import RegistrationForm,EditProfileView,ProfileView,ChangePasswordView,LogoutView,IndexView

app_name = 'accounts'

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("register/", RegistrationForm.as_view(), name="register"),
    path('edit_profile/', EditProfileView.as_view(), name='edit_profile'),
    path('my_profile/', ProfileView.as_view(), name='my_profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('logout/', LogoutView.as_view(), name='logout'),


]
