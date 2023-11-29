from rest_framework import permissions


class IsAuthorPermission(permissions.BasePermission):
    """Доступ к изменению объекта разрешен только автору."""

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user == obj.author
        )
