from django.contrib.auth import get_user_model
from .models import Notification

User = get_user_model()

def notifications_processor(request):
    user = request.user if request.user.is_authenticated else User.objects.first()
    if user:
        unread_count = Notification.objects.filter(user=user, is_read=False).count()
        return {'unread_notifications_count': unread_count}
    return {'unread_notifications_count': 0}