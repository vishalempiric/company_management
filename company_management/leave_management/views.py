# Django Imports
from django.shortcuts import get_object_or_404
from django.utils import timezone

# Django Rest Framework Imports
from rest_framework import status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

# Local Imports
from .models import Leave, LeaveType, LeaveRule
from .serializers import (
    LeaveSerializer,
    LeaveTypeSerializer,
    LeaveRuleSerializer,
)
from company_management.utils import handle_exception
from .permissions import IsStaffOrHigherPermission, IsHROrAdminOnly
from role_management.models import Role


# Create your views here.
class LeaveApplyAPIView(views.APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @handle_exception
    def post(self, request):
        serializer = LeaveSerializer(data=request.data, context={"user": request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Leave Apply successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)


class LeaveApproveAPIView(views.APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStaffOrHigherPermission, IsAuthenticated]
    
    @handle_exception
    def update_leave_fields(self, instance, user):
        field_updates = {
            'Team Leader': ['approve_by_tl'],
            'Project Manager': ['approve_by_tl', 'approve_by_pm'],
            'HR': ['approve_by_tl', 'approve_by_pm', 'approve_by_hr', 'approve_by_admin'],
            'Admin': ['approve_by_tl', 'approve_by_pm', 'approve_by_hr', 'approve_by_admin']
        }

        all_priorities = Role.objects.all()
        all_priorities_numbers = [{"priority":priority.priority, "role":priority.title} for priority in all_priorities]
        print('all_priorities_numbers: ', all_priorities_numbers)

        role = user.role.title
        print('role: ', role)   
        priority = user.role.priority
        print('priority: ', priority)

        if role in field_updates:
            for field in field_updates[role]:
                if not getattr(instance, field):
                    setattr(instance, field, user)


    # @handle_exception
    # def update_leave_fields(self, instance, user):
    #     all_roles = Role.objects.all().order_by('priority')
    #     print('all_roles: ', all_roles)
    #     user_role = user.role
    #     print('user_role: ', user_role) 
    #     print('priority: ', user_role.priority) 

    #     for role in all_roles:
    #         print("------", role.title)
    #         field_updates = {
    #             'Team Leader': 'approve_by_tl',
    #             'Project Manager': 'approve_by_pm',
    #             'HR': 'approve_by_hr',
    #             'Admin': 'approve_by_admin'
    #         }
    #         field_name = f'approve_by_{role.title.lower().replace(" ", "_")}'
    #         print(field_name)
    #         print('role.priority: ',  .priority)
    #         if user_role.priority <= role.priority:
    #             print('========================')
    #             setattr(instance, field_name, user)
                
    #             # If the current role priority is the highest, mark all prior approvals
    #             # if role.priority == user_role.priority:
    #             #     for prior_role in all_roles:
    #             #         print('-------------------')
    #             #         prior_field = f'approve_by_{prior_role.title.lower().replace(" ", "_")}'
    #             #         if prior_role.priority < user_role.priority:
    #             #             setattr(instance, prior_field, user)




    @handle_exception
    def patch(self, request, id):
        leave = get_object_or_404(Leave, pk=id)
        role = request.user.role.title
        user = request.user
        is_approved = request.data.get('is_approved')

        if role == 'Team Leader' and leave.approve_by_tl:
            return Response({"message": "Leave Already Approved", "data": LeaveSerializer(leave).data}, status=status.HTTP_200_OK)
        elif role == 'Project Manager' and leave.approve_by_pm:
            return Response({"message": "Leave Already Approved", "data": LeaveSerializer(leave).data}, status=status.HTTP_200_OK)
        elif role == 'HR' and leave.approve_by_hr:
            return Response({"message": "Leave Already Approved", "data": LeaveSerializer(leave).data}, status=status.HTTP_200_OK)
        elif role == 'Admin' and leave.approve_by_admin:
            return Response({"message": "Leave Already Approved", "data": LeaveSerializer(leave).data}, status=status.HTTP_200_OK)

        self.update_leave_fields(leave, user)
    
        if role in ["Team Leader", "Project Manager"]:
            leave.status = 3 if is_approved else 2
        elif role in ["HR", "Admin"]:
            leave.status = 1 if is_approved else 2

        leave.save()
        serializer = LeaveSerializer(leave)
        return Response({"message": "Leave updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)


class LeaveTypeCRUDAPIView(views.APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsHROrAdminOnly, IsAuthenticated]

    @handle_exception
    def post(self, request, *args, **kwargs):
        serializer = LeaveTypeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "LeaveType created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)

    @handle_exception
    def get(self, request, **kwargs):
        id = kwargs.get('id')
        if id:
            leavetype = get_object_or_404(LeaveType, pk=id)
            serializer = LeaveTypeSerializer(leavetype)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        else:
            leavetypes = LeaveType.objects.all()
            serializer = LeaveTypeSerializer(leavetypes, many=True)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    @handle_exception
    def patch(self, request, id):
        leavetype = get_object_or_404(LeaveType, pk=id)
        serializer = LeaveTypeSerializer(leavetype, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "LeaveType updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)

    @handle_exception
    def put(self, request, id):
        leavetype = get_object_or_404(LeaveType, pk=id)
        serializer = LeaveTypeSerializer(leavetype, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "LeaveType updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)

    @handle_exception
    def delete(self, request, id):
        leavetype = get_object_or_404(LeaveType, pk=id)
        leavetype.status = False
        leavetype.deleted_at = timezone.now()
        leavetype.deleted_by = request.user
        leavetype.save()
        return Response({"message": "LeaveType Deleted successfully"}, status=status.HTTP_200_OK)


class LeaveRuleCRUDAPIView(views.APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsHROrAdminOnly, IsAuthenticated]

    @handle_exception
    def post(self, request, *args, **kwargs):
        serializer = LeaveRuleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "LeaveType created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)

    @handle_exception
    def get(self, request, **kwargs):
        id = kwargs.get('id')
        if id:
            leaverule = get_object_or_404(LeaveRule, pk=id)
            serializer = LeaveRuleSerializer(leaverule)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        else:
            leaverules = LeaveRule.objects.all()
            serializer = LeaveRuleSerializer(leaverules, many=True)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    @handle_exception
    def patch(self, request, id):
        leaverule = get_object_or_404(LeaveRule, pk=id)
        serializer = LeaveRuleSerializer(leaverule, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "LeaveRule updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)

    @handle_exception
    def put(self, request, id):
        leaverule = get_object_or_404(LeaveRule, pk=id)
        serializer = LeaveRuleSerializer(leaverule, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "LeaveRule updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)

    @handle_exception
    def delete(self, request, id):
        leaverule = get_object_or_404(LeaveRule, pk=id)
        leaverule.status = False
        leaverule.deleted_at = timezone.now()
        leaverule.deleted_by = request.user
        leaverule.save()
        return Response({"message": "LeaveRule Deleted successfully"}, status=status.HTTP_200_OK)
