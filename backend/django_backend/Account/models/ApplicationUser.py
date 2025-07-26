from django.contrib.auth.models import AbstractUser
from django.db import models

class ApplicationUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('citizen', 'Citizen'),
        ('journalist', 'Journalist'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='citizen')