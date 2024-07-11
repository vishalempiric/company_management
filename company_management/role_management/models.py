from django.db import models

# Create your models here.
class Role(models.Model):
    title = models.CharField(max_length=30, verbose_name="Role Title", unique=True)
    priority = models.IntegerField(default=0)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Role"
        verbose_name_plural = "Roles"   