from .models import Project, Proposal, Task

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
    return Project.objects.filter(client=user).order_by('-created_at')[:2]

def get_user_tasks(user):
    return Task.objects.filter(project__client=user)[:5]

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