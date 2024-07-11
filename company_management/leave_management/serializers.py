from datetime import datetime, timedelta

from rest_framework import serializers
from rest_framework.serializers import ValidationError

from .models import LeaveRule, Leave, LeaveType
from user_management.models import User
from role_management.models import Role


class RoleSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = Role
        fields = ['id', 'title', 'status'] 


class UserSerializer(serializers.ModelSerializer):

    role = RoleSerializer()

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'role', 'email'] 


class LeaveSerializer(serializers.ModelSerializer):
    
    extra_field = serializers.SerializerMethodField()
    approve_by_tl = UserSerializer()

    class Meta:
        model = Leave
        fields = [
            "id", "leave_type", "start_date", "end_date", "reason", "status",
            "approve_by_tl", "approve_by_pm", "approve_by_hr", "approve_by_admin",
            "extra_field",
        ]
    
    def get_extra_field(self, obj):
        # Add logic to calculate the value of the extra field
        return "Extra Field Value"
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['status'] = instance.get_status_display()       
        representation['additional_info'] = "This is some additional information"
        return representation

    def create(self, validated_data):
        user = self.context.get('user')
        print('user: ', user)
        validated_data['user'] = user
        leave_type = validated_data['leave_type']  
        start_date = validated_data['start_date']
        current_date = datetime.today().date()
        
        if not leave_type.status:
            raise ValidationError("No leave type found")

        if not leave_type.name == 'seek leave':
            leave_rule = LeaveRule.objects.filter(leave_type=leave_type, role=user.role, status=True).first()

            if not leave_rule:
                raise ValidationError("No leave rule found for this role and leave type.")
            
            advance_notice_date = start_date - timedelta(days=leave_rule.advance_notice_days)

            if current_date > advance_notice_date:
                raise ValidationError("You must apply for leave within the advance notice period.")
            
        leave = Leave.objects.create(**validated_data)
        return leave


class LeaveTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = LeaveType
        fields = ['id', 'name', 'description']
    
    def create(self, validated_data):
        leave_type = LeaveType.objects.create(**validated_data)
        return leave_type

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance 
    

class LeaveRuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = LeaveRule
        fields = ['id', 'leave_type', 'role', 'advance_notice_days']
    
    def create(self, validated_data):
        leave_rule = LeaveRule.objects.create(**validated_data)
        return leave_rule

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
