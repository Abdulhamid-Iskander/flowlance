from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Auth
    path('login/',    views.login_view,    name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/',   views.logout_view,   name='logout'),

    # Profile
    path('profile/<str:username>/',       views.profile_view,      name='profile'),
    path('profile/<str:username>/edit/',  views.edit_profile_view, name='edit_profile'),

    # Portfolio
    path('portfolio/add/',              views.add_portfolio_view,    name='add_portfolio'),
    path('portfolio/<int:item_id>/delete/', views.delete_portfolio_view, name='delete_portfolio'),

    # Friend Requests
    path('friend-request/send/<str:username>/',          views.send_friend_request_view,    name='send_friend_request'),
    path('friend-request/<int:request_id>/<str:action>/', views.respond_friend_request_view, name='respond_friend_request'),
    path('friend-requests/',                              views.friend_requests_view,         name='friend_requests'),

    # Settings
    path('settings/', views.settings_view, name='settings'),

    # API
    path('api/notifications-count/', views.notifications_count_api, name='notifications_count_api'),
]