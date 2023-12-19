from django.shortcuts import render, redirect
from .import forms
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash, logout
from django.contrib.auth.decorators import login_required
# Create your views here.


def register(request):
    if request.method == "POST":
        signup_form = forms.RegistrationForm(request.POST)
        if signup_form.is_valid():
            signup_form.save()
            messages.success(request, 'Account created successfully')
            return redirect('user_login')
    else:
        signup_form = forms.RegistrationForm()
    return render(request, 'register.html', {'data': signup_form, 'type': 'Register'})


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['username']
            user_password = form.cleaned_data['password']
            user = authenticate(username=user_name, password=user_password)
            if user is not None:
                messages.success(request, 'login successfully')
                login(request, user)
                return redirect('profile')
            else:
                messages.warning(request, 'login information are incorrect')
                return redirect('register')
    else:
        form = AuthenticationForm()
    return render(request, 'register.html', {'data': form, 'type': 'Login'})


def change_pass(request):
    if request.method == "POST":
        form = SetPasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'password changed successfully')
            update_session_auth_hash(request, form.user)
            return redirect('profile')
    else:
        form = SetPasswordForm(request.user)
    return render(request, 'register.html', {'data': form})


def profile(request):
    return render(request, 'profile.html')


def user_logout(request):
    logout(request)
    messages.success(request, 'logout successfully')
    return redirect('user_login')
