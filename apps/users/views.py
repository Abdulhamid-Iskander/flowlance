from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import User

def login_view(request):
    if request.user.is_authenticated:
        return redirect('projects:dashboard')
        
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        if user is not None:
            login(request, user)
            return redirect('projects:dashboard')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    return render(request, 'users/login.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('projects:dashboard')
        
    if request.method == 'POST':
        u = request.POST.get('username')
        e = request.POST.get('email')
        p = request.POST.get('password')
        r = request.POST.get('role')
        
        if User.objects.filter(username=u).exists():
            messages.error(request, "Username already exists. Please choose a different one.")
            return render(request, 'users/register.html')
            
        user = User.objects.create_user(username=u, email=e, password=p, role=r)
        login(request, user)
        return redirect('projects:dashboard')
    return render(request, 'users/register.html')

def logout_view(request):
    logout(request)
    return redirect('users:login')