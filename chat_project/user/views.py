from django.shortcuts import render, redirect
from django.contrib import messages
from .form import UserRegistrationForm, UserLoginForm
from django.contrib.auth import get_user_model, authenticate, login, logout

User = get_user_model()
# Create your views here.

def register(request):
    """Registering User"""
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Registration Successful')
            return redirect('login')
        else:
            messages.error(request, 'Invalid Form')
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html',{'form':form})

def user_login(request):
    """User Login View"""
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                #return redirect('home')
                return redirect(f'chat/{user.email}/')
            else:
                messages.error(request, 'Invalid Email or Password')
    else:
        form = UserLoginForm()
    return render(request,'login.html',{'form':form})

def user_logout(request):
    """User Logout View"""
    logout(request)
    return redirect('login')