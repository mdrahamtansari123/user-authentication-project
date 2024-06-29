from rest_framework.permissions import BasePermission,SAFE_METHODS

class IsSuperUser(BasePermission):
    """
    Allows access only to superusers.
    """
    def has_permission(self, request, view):
        # return request.user.user_type == "admin" and request.user.user_type == 'superuser'
        if request.user.is_anonymous:
            return False
        return request.user.user_type == 'superuser' 
    
    

class IsAdminUser(BasePermission):
    """
    Allows access only to admins.
    """
    def has_permission(self, request, view):
        # return request.user and request.user.user_type in ['superuser', 'admin']
        if request.user.is_anonymous:
            return False
        # print(request.user.user_type)
        return request.user.user_type == "admin"

class IsRegularUser(BasePermission):
    """
    Allows access only to regular users.
    """
    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        return False



