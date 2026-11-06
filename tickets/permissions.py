from rest_framework import permissions

class IsSupportManagerOrOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and request.user.role == 'support_manager':
            return True
        return obj.author == request.user

class IsSupportManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'support_manager'