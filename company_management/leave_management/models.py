from django.db import models
from user_management.models import User
from role_management.models import Role


# Create your models here.
class LeaveType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deleted_leavetypes', blank=True, null=True)

    def __str__(self):
        return self.name


class LeaveRule(models.Model):
    leave_type = models.ForeignKey(LeaveType, related_name='leave_rules', on_delete=models.CASCADE)
    role = models.ForeignKey(Role, related_name='leave_rules', on_delete=models.CASCADE)
    advance_notice_days = models.IntegerField(default=0)  # Number of days in advance notice required
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deleted_leaverules', blank=True, null=True)

    def __str__(self):
        return f"{self.role.title} - {self.leave_type.name} Leave Rule"


class Leave(models.Model):
    CHOICES = [
        (0, 'Pending'),
        (1, 'Approved'),
        (2, 'Rejected'),
        (3, 'Pending HR Approval'),
    ]
    user = models.ForeignKey(User, related_name='leaves', on_delete=models.CASCADE)
    leave_type = models.ForeignKey(LeaveType, related_name='leaves', on_delete=models.CASCADE)
    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True)
    reason = models.TextField()

    approve_by_tl = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='tl_approvals')
    approve_by_pm = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='pm_approvals')
    approve_by_hr = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='hr_approvals')
    approve_by_admin = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='admin_approvals')

    status = models.IntegerField(choices=CHOICES, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deleted_leave', blank=True, null=True)

    def __str__(self):
        return f"Leave {self.id} - {self.user.username} ({self.start_date} to {self.end_date})"