from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django import forms

class EditProfileForm(UserChangeForm):
    password = forms.CharField(label="", widget=forms.TextInput(attrs={'type':'hidden'}))
    first_name = forms.CharField(label="Nome", max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(label="Sobrenome", max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(label="Email", max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')

