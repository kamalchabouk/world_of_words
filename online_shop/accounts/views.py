from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from django.contrib.auth import login
from django import forms
from django import forms
from django.shortcuts import redirect, render
from .forms import CustomUserChangeForm, CustomUserCreationForm
from django.views.generic import CreateView, ListView, View, FormView,TemplateView
from django.urls import reverse_lazy, reverse

class RegistrationForm(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/register.html"

    class Meta:
        model=CustomUser
        fields = ["username", "email", "password1", "password2"]

# class CustomUserCreationForm(UserCreationForm):
#     class Meta:
#         model=CustomUser
#         fields = ("username", "email", "password1", "password2")

def registration_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Don't commit yet to avoid saving unhashed password
            user.set_password(user.cleaned_data['password'])  # Set and hash the password
            user.save()  # Now save the user with hashed password
            login(request, user)



            return redirect("index")
    else:
        form = RegistrationForm()

    return render(request, "registration/register.html", {"form": form})


class IndexView(TemplateView):
    template_name="index.html"

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
            try:
                form.save()
                # Add success message to context (optional)
                context = {'form': form, 'success_message': 'Profile updated successfully!'}
                return redirect('accounts:index', context=context)
            except Exception as e:
                context = {'form': form, 'error_message': f'An error occurred: {e}'}
                return render(request, self.template_name, context)
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
class ChangePasswordView(FormView):
    template_name = 'change_password.html'
    form_class = PasswordChangeForm
    success_url = 'accounts/index.html'  # Replace with your desired success page URL

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
 
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Change Password'  # Optional title for the template
        return context


class LogoutView(TemplateView):
    template_name = 'logout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'Thank you for visiting'