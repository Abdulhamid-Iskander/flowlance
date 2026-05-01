from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
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

@login_required(login_url='users:login')
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    
    if request.method == 'POST' and request.user == profile_user:
        profile_user.bio = request.POST.get('bio')
        profile_user.skills = request.POST.get('skills')
        if 'profile_picture' in request.FILES:
            profile_user.profile_picture = request.FILES['profile_picture']
        profile_user.save()
        return redirect('users:profile', username=username)
        
    return render(request, 'users/profile.html', {
        'profile_user': profile_user,
        'reviews': profile_user.received_reviews.all()
    })