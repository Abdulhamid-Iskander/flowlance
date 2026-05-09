from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('CLIENT', 'Client'),
        ('FREELANCER', 'Freelancer'),
        ('TEAM_LEADER', 'Team Leader'),
        ('TEAM_MEMBER', 'Team Member'),
    )

    role            = models.CharField(max_length=20, choices=ROLE_CHOICES, default='CLIENT')
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    cover_picture   = models.ImageField(upload_to='covers/',   null=True, blank=True)
    bio             = models.TextField(blank=True, null=True)
    skills          = models.CharField(max_length=255, blank=True, null=True)
    full_name       = models.CharField(max_length=150, blank=True, null=True)
    linkedin        = models.URLField(blank=True, null=True)
    instagram       = models.URLField(blank=True, null=True)
    facebook        = models.URLField(blank=True, null=True)
    hourly_rate     = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    location        = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class PortfolioItem(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='portfolio_items')
    title       = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    link        = models.URLField(blank=True, null=True)
    image       = models.ImageField(upload_to='portfolio/', null=True, blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"


class FriendRequest(models.Model):
    STATUS_CHOICES = (
        ('PENDING',  'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
    )
    from_user  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    to_user    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')
    status     = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f"{self.from_user} → {self.to_user} ({self.status})"
    
