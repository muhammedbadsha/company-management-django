from rest_framework.permissions import BasePermission

#permission for HR manegers

class IsHRManager(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.department.department == "hr_manager"
    
class IsManager(BasePermission):
    def has_permission(self, request, view):
        #Assuming you have an "is_department_manager"
        return request.user and request.user.is_authenticated and request.user.department.department == 'manager'