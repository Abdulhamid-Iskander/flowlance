from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('marketplace/', views.marketplace_view, name='marketplace'),
    path('create/', views.create_project_view, name='create_project'),
    path('project/<int:pk>/', views.project_detail_view, name='project_detail'),
    path('project/<int:pk>/complete/', views.complete_project_action, name='complete_project'),
    path('proposal/<int:proposal_id>/accept/', views.accept_proposal_view, name='accept_proposal'),
    path('task/<int:task_id>/update/<str:new_status>/', views.update_task_status_view, name='update_task_status'),
    path('milestone/<int:milestone_id>/pay/', views.pay_milestone_view, name='pay_milestone'),
    path('notifications/', views.notifications_list_view, name='notifications_list'),
    path('teams/', views.teams_view, name='teams'),
]