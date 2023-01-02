from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email", max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(label="Nome", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nome'}))
    last_name = forms.CharField(label="Sobrenome", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Sobrenome'}))
    

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Nome de usuário'
        self.fields['username'].label = 'Nome de usuário'
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Máximo de 150 caracteres.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Senha'
        self.fields['password1'].label = 'Senha'
        self.fields['password1'].help_text = '<span class="form-text text-muted"><small>Senha deve ser complexa</small></span>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirme a Senha'
        self.fields['password2'].label = 'Confirme a Senha'
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Confirme a senha para verificação</small></span>'



class EditProfileForm(UserChangeForm):
    password = forms.CharField(label="", widget=forms.TextInput(attrs={'type':'hidden'}))
    first_name = forms.CharField(label="Nome", max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(label="Sobrenome", max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(label="Email", max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')

