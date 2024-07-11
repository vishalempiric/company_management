from django.db import models
from django.contrib.auth.models import AbstractUser

from role_management.models import Role

# Create your models here.
class User(AbstractUser):
    profile_pic = models.CharField(max_length=50, blank=True, verbose_name="Profile Picture")
    description = models.TextField(blank=True, verbose_name="Description")
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='users', verbose_name="Role", blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='deleted_user', blank=True, null=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"