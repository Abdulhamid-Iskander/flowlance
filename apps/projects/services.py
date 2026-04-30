from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import Project, Proposal, Task, Notification, Team

User = get_user_model()

def get_dashboard_stats(user):
    total_projects = Project.objects.filter(client=user).count()
    open_projects = Project.objects.filter(client=user, status='OPEN').count()
    active_workflows = Project.objects.filter(client=user, status='IN_PROGRESS').count()
    pending_proposals = Proposal.objects.filter(project__client=user, status='PENDING').count()
    
    return {
        'total_projects': total_projects,
        'open_projects': open_projects,
        'active_workflows': active_workflows,
        'pending_proposals': pending_proposals,
    }

def get_recent_projects(user):
    projects = Project.objects.filter(Q(client=user) | Q(proposals__freelancer=user)).distinct().order_by('-created_at')[:4]
    for project in projects:
        total_tasks = project.tasks.count()
        if total_tasks > 0:
            completed_tasks = project.tasks.filter(status__in=['SUBMITTED', 'UNDER_REVIEW']).count()
            project.progress = int((completed_tasks / total_tasks) * 100)
        else:
            project.progress = 0
    return projects

def get_user_tasks(user):
    return Task.objects.filter(assignee=user)[:5]

def create_new_project(user, data):
    project = Project.objects.create(
        client=user,
        title=data.get('title'),
        description=data.get('description'),
        budget=data.get('budget'),
        deadline=data.get('deadline'),
    )
    
    tags = data.get('skills', '').split(',')
    for tag in tags:
        tag = tag.strip()
        if tag:
            project.skills_required.add(tag)
            
    return project

def submit_proposal(user, project_id, data):
    project = Project.objects.get(id=project_id)
    Proposal.objects.create(
        project=project,
        freelancer=user,
        bid_amount=data.get('bid_amount'),
        duration=data.get('duration')
    )
    Notification.objects.create(
        user=project.client,
        message=f"New proposal submitted by {user.username} for {project.title}"
    )

def accept_proposal(proposal_id):
    proposal = Proposal.objects.get(id=proposal_id)
    project = proposal.project
    
    proposal.status = 'ACCEPTED'
    proposal.save()
    
    Proposal.objects.filter(project=project).exclude(id=proposal_id).update(status='REJECTED')
    
    project.status = 'IN_PROGRESS'
    project.save()
    
    default_tasks = ['UI/UX Design', 'Database Setup', 'Backend Development', 'Final Delivery']
    for task_name in default_tasks:
        Task.objects.create(
            project=project,
            name=task_name,
            status='TO_DO',
            assignee=proposal.freelancer
        )
        
    Notification.objects.create(
        user=proposal.freelancer,
        message=f"Congratulations! Your proposal for {project.title} was accepted."
    )

def update_task_status(task_id, new_status):
    task = Task.objects.get(id=task_id)
    task.status = new_status
    task.save()
    
    Notification.objects.create(
        user=task.project.client,
        message=f"Task '{task.name}' status updated to {new_status}."
    )

def get_user_notifications(user):
    return Notification.objects.filter(user=user).order_by('-created_at')

def mark_notifications_read(user):
    Notification.objects.filter(user=user, is_read=False).update(is_read=True)

def get_user_teams(user):
    return Team.objects.filter(Q(leader=user) | Q(members=user)).distinct()

def get_available_members(user):
    return User.objects.exclude(id=user.id)

def create_new_team(user, data):
    team = Team.objects.create(name=data.get('name'), leader=user)
    member_ids = data.getlist('members')
    if member_ids:
        team.members.add(*member_ids)
    return team

def get_all_open_projects(query=None):
    projects = Project.objects.filter(status='OPEN').order_by('-created_at')
    if query:
        projects = projects.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) | 
            Q(skills_required__name__icontains=query)
        ).distinct()
    return projects