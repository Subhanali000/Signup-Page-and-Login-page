from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    
    address_line1 = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    user_type = models.CharField(
        max_length=10,
        choices=[('doctor', 'Doctor'), ('patient', 'Patient')],
        default='patient'
    )

    def __str__(self):
        return self.username
