from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
# A form that creates a user, with no privileges, from the given username and password.
# https://github.com/django/django/blob/main/django/contrib/auth/forms.py
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm


def home(request):
    return render(request, 'home.html', {})


def signup(request):
    submitted = False
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            submitted = True
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {
        'form': form, 'submitted':submitted
        })


def change_password(request):
    # Verificar exibição de mensagens para indicar se deu certo ou mão a atualização da senha
    changed = False
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            changed = True
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {
        'form':form, 'changed':changed
    })