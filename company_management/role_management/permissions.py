from rest_framework import permissions

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