from rest_framework import permissions


class OwnerOrReadOnly(permissions.BasePermission):

    # Определение права на уровне запроса или пользователя
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    # Определение права на уровне объекта
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class ReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
