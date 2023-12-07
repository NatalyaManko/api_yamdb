from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    '''Права на удаление и изменение отзывов и комментариев.'''
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (
                request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.is_moderator
                or request.user.is_admin
                or request.user.is_superuser
            )
        return (
            request.method in permissions.SAFE_METHODS
        )


class AdminPermission(permissions.BasePermission):
    '''Права на получение, изменение и удаление пользователя по username'''

    def has_permission(self, request, view):
        return (
            request.user.is_admin
            or request.user.is_superuser
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    '''Права на создание и удаление произведений, категорий и жанров'''

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (
                request.method in permissions.SAFE_METHODS
                or request.user.is_admin
                or request.user.is_superuser
            )
        return (
            request.method in permissions.SAFE_METHODS
        )
