from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Project, Proposal, Task, Team, Milestone, Message
from .services import *

@login_required(login_url='users:login')
def dashboard_view(request):
    stats = get_dashboard_stats(request.user)
    recent_projects = get_recent_projects(request.user)
    user_tasks = get_user_tasks(request.user)
    return render(request, 'projects/dashboard.html', {
        'username': request.user.username,
        'total_projects': stats['total_projects'],
        'open_projects': stats['open_projects'],
        'active_workflows': stats['active_workflows'],
        'avg_rating': stats.get('avg_rating', 0),
        'recent_projects': recent_projects,
        'user_tasks': user_tasks,
    })

@login_required(login_url='users:login')
def project_detail_view(request, pk):
    project = get_object_or_404(Project, pk=pk)
    is_client = request.user == project.client
    is_freelancer = project.proposals.filter(freelancer=request.user, status='ACCEPTED').exists()

    if request.method == 'POST':
        if 'chat_message' in request.POST and (is_client or is_freelancer):
            Message.objects.create(project=project, sender=request.user, content=request.POST.get('chat_message'))
        elif 'file' in request.FILES:
            upload_project_file(project.id, request.user, request.FILES['file'], request.POST.get('description'))
        elif 'bid_amount' in request.POST:
            submit_proposal(request.user, project.id, request.POST)
        elif 'milestone_title' in request.POST and is_client:
            create_milestone(project.id, request.POST)
        elif 'rating' in request.POST and is_client:
            create_review(project.id, request.user, request.POST)
        return redirect('projects:project_detail', pk=project.id)

    return render(request, 'projects/detail.html', {
        'project': project,
        'proposals': project.proposals.all(),
        'tasks': project.tasks.all(),
        'milestones': project.milestones.all(),
        'files': project.files.all(),
        'is_client': is_client,
        'is_freelancer': is_freelancer,
        'has_review': hasattr(project, 'review'),
    })

@login_required(login_url='users:login')
def create_project_view(request):
    if request.method == 'POST':
        create_new_project(request.user, request.POST)
        return redirect('projects:dashboard')
    return render(request, 'projects/create.html')

@login_required(login_url='users:login')
def marketplace_view(request):
    query = request.GET.get('q', '')
    projects = get_all_open_projects(query)
    return render(request, 'projects/marketplace.html', {'projects': projects, 'query': query})

@login_required(login_url='users:login')
def accept_proposal_view(request, proposal_id):
    proposal = get_object_or_404(Proposal, id=proposal_id)
    if request.user != proposal.project.client:
        return HttpResponseForbidden("Unauthorized: Only the client can accept proposals.")
    accept_proposal(proposal_id)
    return redirect(request.META.get('HTTP_REFERER', 'projects:dashboard'))

@login_required(login_url='users:login')
def update_task_status_view(request, task_id, new_status):
    task = get_object_or_404(Task, id=task_id)
    if request.user != task.assignee and request.user != task.project.client:
        return HttpResponseForbidden("Unauthorized: You cannot update this task.")
    update_task_status(task_id, new_status)
    return redirect(request.META.get('HTTP_REFERER', 'projects:dashboard'))

@login_required(login_url='users:login')
def pay_milestone_view(request, milestone_id):
    milestone = get_object_or_404(Milestone, id=milestone_id)
    if request.user != milestone.project.client:
        return HttpResponseForbidden("Unauthorized: Only the client can pay.")
    pay_milestone(milestone_id)
    return redirect(request.META.get('HTTP_REFERER', 'projects:dashboard'))

@login_required(login_url='users:login')
def complete_project_action(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.user != project.client:
        return HttpResponseForbidden("Unauthorized")
    complete_project(pk)
    return redirect('projects:project_detail', pk=pk)

@login_required(login_url='users:login')
def notifications_list_view(request):
    notifications = get_user_notifications(request.user)
    mark_notifications_read(request.user)
    return render(request, 'projects/notifications.html', {'notifications': notifications})

@login_required(login_url='users:login')
def teams_view(request):
    if request.method == 'POST':
        create_new_team(request.user, request.POST)
        return redirect('projects:teams')
    
    from django.contrib.auth import get_user_model
    User = get_user_model()
    return render(request, 'projects/teams.html', {
        'teams': get_user_teams(request.user),
        'available_members': User.objects.exclude(id=request.user.id)
    })