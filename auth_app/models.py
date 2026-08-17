from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    User profile model extending Django's User model.
    
    Attributes:
        user: OneToOne relationship with Django User model
        fullname: User's full name for display purposes
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    fullname = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
        ordering = ['fullname']

    def __str__(self):
        return f'{self.fullname} ({self.user.email})'