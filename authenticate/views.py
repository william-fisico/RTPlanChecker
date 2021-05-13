from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib import messages
from .forms import EditProfileForm, SignUpForm


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ('You Have Registered...'))
            return redirect('home')
    else:
        form = SignUpForm()

    context = {'form': form}
    return render(request, 'authenticate/register.html', context)


def home(request):
    return render(request, 'authenticate/home.html')


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            #messages.success(request, ('Login realizado com sucesso!'))
            return redirect('home')
        else:
            messages.success(request, ('Erro ao logar. Por favor tente novamente'))
            return redirect('login')
    else:
        return render(request, 'authenticate/login.html')


def logout_user(request):
    logout(request)
    messages.success(request, ('Você foi desconectado!'))
    return redirect('home')


def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, ('Dados autalizados com sucesso.'))
            return redirect('edit_profile')
    else:
        form = EditProfileForm(instance=request.user)

    context = {'form':form}
    return render(request, 'authenticate/edit_profile.html', context)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, ('Senha atualizada com sucesso.'))
            return redirect('home')
    else:
        form = PasswordChangeForm(user=request.user)

    context = {'form':form}
    return render(request, 'authenticate/change_password.html', context)


def login_permission_error(request):
    return render(request, 'authenticate/login_permission.html')
