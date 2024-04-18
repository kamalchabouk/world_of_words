from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from .models import CustomUser,Comment, Rate
from django import forms


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'address', 'phone_number', 'last_name']


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'username',  'address', 'phone_number']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password')
        self.fields['username'].help_text = None  # Remove help text for the username field




class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = CustomUser


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'comment')  # Fields displayed in the form

class RateForm(forms.ModelForm):
    class Meta:
        model = Rate
        fields = ('rating',)  