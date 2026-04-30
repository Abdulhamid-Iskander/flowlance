from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from .services import create_new_project

from .services import get_dashboard_stats, get_recent_projects, get_user_tasks

User = get_user_model()

def dashboard_view(request):
    user = request.user if request.user.is_authenticated else User.objects.first()
    
    if not user:
        return render(request, 'projects/dashboard.html', {})

    stats = get_dashboard_stats(user)
    recent_projects = get_recent_projects(user)
    user_tasks = get_user_tasks(user)

    context = {
        'username': user.username,
        'total_projects': stats['total_projects'],
        'open_projects': stats['open_projects'],
        'active_workflows': stats['active_workflows'],
        'pending_proposals': stats['pending_proposals'],
        'recent_projects': recent_projects,
        'user_tasks': user_tasks,
    }
    return render(request, 'projects/dashboard.html', context)



def create_project_view(request):
    if request.method == 'POST':
        create_new_project(request.user, request.POST)
        return redirect('projects:dashboard')
        
    return render(request, 'projects/create.html')