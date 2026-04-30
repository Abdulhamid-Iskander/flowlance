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