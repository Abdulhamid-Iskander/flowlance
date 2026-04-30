from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('CLIENT', 'Client'),
        ('FREELANCER', 'Freelancer'),
        ('TEAM_LEADER', 'Team Leader'),
        ('TEAM_MEMBER', 'Team Member'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='CLIENT')
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"