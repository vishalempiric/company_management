# Django Imports
from django.shortcuts import get_object_or_404
from django.utils import timezone

# Django Rest Framework Imports
from rest_framework import status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

# Local Imports
from .models import Role
from .serializers import RoleSerializer

from company_management.utils import handle_exception
from .permissions import IsHROrAdminOnly


# Create your views here.
class RoleCRUDAPIView(views.APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsHROrAdminOnly, IsAuthenticated]

    @handle_exception
    def post(self, request, *args, **kwargs):
        serializer = RoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Role created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)

    @handle_exception
    def get(self, request, **kwargs):
        id = kwargs.get('id')
        if id:
            role = get_object_or_404(Role, pk=id)
            if not role.status:
                return Response({"error": "Role Not Found", }, status=status.HTTP_404_NOT_FOUND)
            serializer = RoleSerializer(role)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        else:
            roles = Role.objects.all()
            serializer = RoleSerializer(roles, many=True)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    @handle_exception
    def patch(self, request, id):
        role = get_object_or_404(Role, pk=id)
        if not role.status:
            return Response({"error": "Role Not Found", }, status=status.HTTP_404_NOT_FOUND)
        serializer = RoleSerializer(role, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Role updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)

    @handle_exception
    def put(self, request, id):
        role = get_object_or_404(Role, pk=id)
        if not role.status:
            return Response({"error": "Role Not Found", }, status=status.HTTP_404_NOT_FOUND)
        serializer = RoleSerializer(role, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Role updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)

    @handle_exception
    def delete(self, request, id):
        role = get_object_or_404(Role, pk=id)
        role.status = False
        role.deleted_at = timezone.now()
        role.save()
        return Response({"message": "Role Deleted successfully"}, status=status.HTTP_200_OK)