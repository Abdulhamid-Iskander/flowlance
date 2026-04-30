from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Project, Proposal
from .services import get_dashboard_stats, get_recent_projects, get_user_tasks, create_new_project, submit_proposal, accept_proposal, update_task_status, mark_notifications_read, get_user_notifications, get_user_teams, get_available_members, create_new_team, get_all_open_projects

@login_required(login_url='users:login')
def dashboard_view(request):
    stats = get_dashboard_stats(request.user)
    recent_projects = get_recent_projects(request.user)
    user_tasks = get_user_tasks(request.user)

    context = {
        'username': request.user.username,
        'total_projects': stats['total_projects'],
        'open_projects': stats['open_projects'],
        'active_workflows': stats['active_workflows'],
        'pending_proposals': stats['pending_proposals'],
        'recent_projects': recent_projects,
        'user_tasks': user_tasks,
    }
    return render(request, 'projects/dashboard.html', context)

@login_required(login_url='users:login')
def create_project_view(request):
    if request.method == 'POST':
        create_new_project(request.user, request.POST)
        return redirect('projects:dashboard')
    return render(request, 'projects/create.html')

@login_required(login_url='users:login')
def project_detail_view(request, pk):
    project = get_object_or_404(Project, pk=pk)
    proposals = project.proposals.all()

    if request.method == 'POST' and 'bid_amount' in request.POST:
        submit_proposal(request.user, project.id, request.POST)
        return redirect('projects:project_detail', pk=project.id)

    context = {
        'project': project,
        'proposals': proposals,
        'is_client': request.user == project.client,
    }
    return render(request, 'projects/detail.html', context)

@login_required(login_url='users:login')
def accept_proposal_view(request, proposal_id):
    accept_proposal(proposal_id)
    proposal = get_object_or_404(Proposal, id=proposal_id)
    return redirect('projects:project_detail', pk=proposal.project.id)

@login_required(login_url='users:login')
def update_task_status_view(request, task_id, new_status):
    update_task_status(task_id, new_status)
    return redirect('projects:dashboard')

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
    
    teams = get_user_teams(request.user)
    available_members = get_available_members(request.user)
    return render(request, 'projects/teams.html', {
        'teams': teams,
        'available_members': available_members
    })

@login_required(login_url='users:login')
def marketplace_view(request):
    query = request.GET.get('q', '')
    projects = get_all_open_projects(query)
    return render(request, 'projects/marketplace.html', {
        'projects': projects,
        'query': query
    })