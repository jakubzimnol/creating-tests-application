from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    Custom permission to only allow admin to edit it.
    """

    def has_permission(self, request, view):
        return request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser


class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsTestOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return obj.test.user == request.user


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS


def permission_or(*args):
    class Permission(permissions.BasePermission):
        def has_object_permission(self, request, view, obj):
            for permission in args:
                if permission.has_object_permission(self=self, request=request, view=view, obj=obj):
                    return True
            return False

        def has_permission(self, request, view):
            for permission in args:
                if permission.has_permission(self=self, request=request, view=view):
                    return True
            return False

    return Permission
