from django.contrib.auth.models import AbstractUser
from django.db import models

class Blog(models.Model):
    CATEGORIES = [
        ('Health', 'Health'),
        ('Wellness', 'Wellness'),
        ('News', 'News'),
        ('Research', 'Research'),
    ]

    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='blog_images/')
    category = models.CharField(max_length=50, choices=CATEGORIES)
    summary = models.TextField(max_length=15)
    content = models.TextField()
    is_draft = models.BooleanField(default=True)  # Field to mark draft status
    created_at = models.DateTimeField(auto_now_add=True)
    # Use string reference for the ForeignKey
    author = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='blogs')

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"

    def __str__(self):
        return self.title


class CustomUser(AbstractUser):
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    user_type = models.CharField(
        max_length=10,
        choices=[('doctor', 'Doctor'), ('patient', 'Patient')],
        default='patient'
    )

    class Meta:
        verbose_name = "Custom User"
        verbose_name_plural = "Custom Users"

    def __str__(self):
        return f"{self.username} ({self.user_type})"
