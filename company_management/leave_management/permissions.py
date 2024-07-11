from rest_framework import permissions

class IsStaffOrHigherPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        
        if hasattr(user, 'role'):
            if user.role.title.strip() in ['HR', 'Team Leader', 'Admin', 'Project Manager']:
                return True
            else:
                return False
        return False
    

class IsHROrAdminOnly(permissions.BasePermission):
    ROLES = {'HR', 'Admin'}

    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated
            and hasattr(user, 'role')
            and user.role.title.strip() in self.ROLES
        )


# class IsHROrReadOnly(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.user and (request.user.role.title.strip() == 'HR') 