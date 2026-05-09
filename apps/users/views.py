from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import User, PortfolioItem, FriendRequest


def login_view(request):
    if request.user.is_authenticated:
        return redirect('projects:dashboard')
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        if user:
            login(request, user)
            return redirect('projects:dashboard')
        messages.error(request, "Invalid username or password.")
    return render(request, 'users/login.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('projects:dashboard')
    if request.method == 'POST':
        u = request.POST.get('username')
        e = request.POST.get('email')
        p = request.POST.get('password')
        r = request.POST.get('role')
        if User.objects.filter(username=u).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'users/register.html')
        user = User.objects.create_user(username=u, email=e, password=p, role=r)
        login(request, user)
        return redirect('projects:dashboard')
    return render(request, 'users/register.html')


def logout_view(request):
    logout(request)
    return redirect('users:login')


@login_required(login_url='users:login')
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    portfolio    = profile_user.portfolio_items.all().order_by('-created_at')

    friend_status = None
    if request.user != profile_user:
        req = FriendRequest.objects.filter(from_user=request.user, to_user=profile_user).first()
        if req:
            friend_status = req.status
        else:
            rev = FriendRequest.objects.filter(from_user=profile_user, to_user=request.user, status='PENDING').first()
            if rev:
                friend_status = 'RECEIVED'

    friends = User.objects.filter(
        sent_requests__to_user=profile_user, sent_requests__status='ACCEPTED'
    ) | User.objects.filter(
        received_requests__from_user=profile_user, received_requests__status='ACCEPTED'
    )

    return render(request, 'users/profile.html', {
        'profile_user':  profile_user,
        'reviews':       profile_user.received_reviews.all(),
        'portfolio':     portfolio,
        'friend_status': friend_status,
        'friends_count': friends.distinct().count(),
    })


@login_required(login_url='users:login')
def edit_profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    if request.user != profile_user:
        return redirect('users:profile', username=username)

    if request.method == 'POST':
        profile_user.full_name  = request.POST.get('full_name', '').strip()
        profile_user.bio        = request.POST.get('bio', '').strip()
        profile_user.skills     = request.POST.get('skills', '').strip()
        profile_user.location   = request.POST.get('location', '').strip()
        profile_user.linkedin   = request.POST.get('linkedin', '').strip() or None
        profile_user.instagram  = request.POST.get('instagram', '').strip() or None
        profile_user.facebook   = request.POST.get('facebook', '').strip() or None
        hourly = request.POST.get('hourly_rate', '').strip()
        profile_user.hourly_rate = hourly if hourly else None
        if 'profile_picture' in request.FILES:
            profile_user.profile_picture = request.FILES['profile_picture']
        if 'cover_picture' in request.FILES:
            profile_user.cover_picture = request.FILES['cover_picture']
        profile_user.save()
        messages.success(request, "Profile updated!")
        return redirect('users:profile', username=username)

    return render(request, 'users/edit_profile.html', {'profile_user': profile_user})


@login_required(login_url='users:login')
def add_portfolio_view(request):
    if request.method == 'POST':
        item = PortfolioItem(user=request.user)
        item.title       = request.POST.get('title', '').strip()
        item.description = request.POST.get('description', '').strip()
        item.link        = request.POST.get('link', '').strip() or None
        if 'image' in request.FILES:
            item.image = request.FILES['image']
        item.save()
    return redirect('users:profile', username=request.user.username)


@login_required(login_url='users:login')
def delete_portfolio_view(request, item_id):
    item = get_object_or_404(PortfolioItem, id=item_id, user=request.user)
    item.delete()
    return redirect('users:profile', username=request.user.username)


@login_required(login_url='users:login')
def send_friend_request_view(request, username):
    to_user = get_object_or_404(User, username=username)
    if to_user != request.user:
        FriendRequest.objects.get_or_create(from_user=request.user, to_user=to_user)
    return redirect('users:profile', username=username)


@login_required(login_url='users:login')
def respond_friend_request_view(request, request_id, action):
    freq = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
    freq.status = 'ACCEPTED' if action == 'accept' else 'REJECTED'
    freq.save()
    return redirect('users:friend_requests')


@login_required(login_url='users:login')
def friend_requests_view(request):
    received = FriendRequest.objects.filter(to_user=request.user, status='PENDING').select_related('from_user')
    sent     = FriendRequest.objects.filter(from_user=request.user).select_related('to_user')
    return render(request, 'users/friend_requests.html', {'received': received, 'sent': sent})


@login_required(login_url='users:login')
def settings_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'change_password':
            old_pw  = request.POST.get('old_password')
            new_pw  = request.POST.get('new_password')
            new_pw2 = request.POST.get('new_password2')
            if not request.user.check_password(old_pw):
                messages.error(request, "Current password is incorrect.")
            elif new_pw != new_pw2:
                messages.error(request, "New passwords don't match.")
            elif len(new_pw) < 6:
                messages.error(request, "Password must be at least 6 characters.")
            else:
                request.user.set_password(new_pw)
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, "Password changed successfully!")

        elif action == 'delete_account':
            if request.POST.get('confirm_delete') == request.user.username:
                request.user.delete()
                logout(request)
                return redirect('users:login')
            else:
                messages.error(request, "Username confirmation didn't match.")

    # ← هنا بنستخدم 'setting.html' (بدون s) زي ما هو موجود عندك
    return render(request, 'users/setting.html')


@login_required(login_url='users:login')
def notifications_count_api(request):
    from apps.projects.models import Notification
    count   = Notification.objects.filter(user=request.user, is_read=False).count()
    pending = FriendRequest.objects.filter(to_user=request.user, status='PENDING').count()
    return JsonResponse({'unread': count, 'friend_requests': pending})