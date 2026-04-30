from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('create/', views.create_project_view, name='create_project'),
]