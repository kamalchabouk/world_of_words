from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django import forms
from django import forms
from django.shortcuts import redirect, render
from .forms import CustomUserChangeForm
from django.views.generic import CreateView, ListView, View, TemplateView, UpdateView

class RegistrationForm(CreateView):
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


def index(request):
    return render(request,"index.html")

class EditProfileView(View):
    template_name = 'edit_profile.html'
    
    def get(self, request):
        user = request.user
        form = CustomUserChangeForm(instance=user)
        context = {'form': form}
        return render(request, self.template_name, context)
    
    def post(self, request):
        user = request.user
        form = CustomUserChangeForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('frontend_courses:home')  
        else:
            context = {'form': form}
            return render(request, self.template_name, context)


class ProfileView(ListView):
    model = CustomUser
    template_name = "my_profile.html"
    context_object_name = "profile"

    def get_queryset(self):
        return CustomUser.objects.filter(pk=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = context['object_list'].first()  
        context['profile'] = profile
        return context
