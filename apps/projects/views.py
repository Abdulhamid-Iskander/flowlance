from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from .models import Project, Proposal
from .services import get_dashboard_stats, get_recent_projects, get_user_tasks, create_new_project, submit_proposal, accept_proposal, update_task_status, mark_notifications_read

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
    user = request.user if request.user.is_authenticated else User.objects.first()
    
    if request.method == 'POST':
        create_new_project(user, request.POST)
        return redirect('projects:dashboard')
        
    return render(request, 'projects/create.html')

def project_detail_view(request, pk):
    user = request.user if request.user.is_authenticated else User.objects.first()
    project = get_object_or_404(Project, pk=pk)
    proposals = project.proposals.all()

    if request.method == 'POST' and 'bid_amount' in request.POST:
        submit_proposal(user, project.id, request.POST)
        return redirect('projects:project_detail', pk=project.id)

    context = {
        'project': project,
        'proposals': proposals,
        'is_client': True,
    }
    return render(request, 'projects/detail.html', context)

def accept_proposal_view(request, proposal_id):
    accept_proposal(proposal_id)
    proposal = get_object_or_404(Proposal, id=proposal_id)
    return redirect('projects:project_detail', pk=proposal.project.id)

def update_task_status_view(request, task_id, new_status):
    update_task_status(task_id, new_status)
    return redirect('projects:dashboard')

def read_notifications_view(request):
    user = request.user if request.user.is_authenticated else User.objects.first()
    mark_notifications_read(user)
    return redirect(request.META.get('HTTP_REFERER', 'projects:dashboard'))