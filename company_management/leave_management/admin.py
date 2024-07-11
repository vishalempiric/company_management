from django.contrib import admin
from .models import Leave, LeaveRule, LeaveType

# Register your models here.
@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    # list_display = [
    #     'id',
    #     "user",
    #     "leave_type",
    #     "start_date",
    #     "end_date",
    #     "reason",
    #     'status',
    #     'approve_by_tl',
    #     'approve_by_pm',
    #     'approve_by_hr',
    #     'approve_by_admin',
    # ]
    list_display = [field.name for field in Leave._meta.get_fields()]



@admin.register(LeaveRule)
class LeaveRuleAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'leave_type',
        'role',
        'advance_notice_days',
        'status',
        'created_at',
        'updated_at',
        'deleted_at',
        'deleted_by',
    ]


@admin.register(LeaveType)
class LeaveTypeAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name', 
        'description',
        'status',
        'created_at',
        'updated_at',
        'deleted_at',
        'deleted_by',
    ]
