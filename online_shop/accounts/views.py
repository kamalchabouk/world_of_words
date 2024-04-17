from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django import forms
from django import forms
from django.shortcuts import redirect, render

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model=CustomUser
        fields = ["username", "email", "password1", "password2"]

# class CustomUserCreationForm(UserCreationForm):
#     class Meta:
#         model=CustomUser
#         fields = ("username", "email", "password1", "password2")

def  registration_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect("index")
    else:
        form = RegistrationForm()

    return render(request, "registration/register.html", {"form" : form})


    
def logout_view(request):
    logout(request)
    return redirect('shop:home')

def index(request):
    return render(request,"index.html")
        