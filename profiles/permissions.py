from rest_framework import permissions

class VerifiedUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_verified