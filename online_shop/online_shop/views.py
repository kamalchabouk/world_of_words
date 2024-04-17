from accounts.models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django import forms
from django import forms
from django.shortcuts import redirect, render


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model=CustomUser
        fields = ["username", "email", "password1", "password2"]


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


class CustomLoginView(LoginView):
    def get_success_url(self):
        return '/shop/view-cart/'  
    
def index(request):
    return render(request,"index.html")

