from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('create/', views.create_project_view, name='create_project'),
    path('project/<int:pk>/', views.project_detail_view, name='project_detail'),
    path('proposal/<int:proposal_id>/accept/', views.accept_proposal_view, name='accept_proposal'),
    path('task/<int:task_id>/update/<str:new_status>/', views.update_task_status_view, name='update_task_status'),
    path('notifications/read/', views.read_notifications_view, name='read_notifications'),
]