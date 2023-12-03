from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    '''Права на удаление и изменение отзывов и комментариев.'''
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.filter(role='moderator').exists()
            or request.user.filter(role='admin').exists()
            or request.user.is_superuser
        )


class AdminPermission(permissions.BasePermission):
    '''Права на создание и удаление произведений, категорий и жанров;
    на получение, изменение и удаление пользователя по username'''

    def has_object_permission(self, request, view, obj):
        return (
            request.user.filter(role='admin').exists()
            or request.user.is_superuser
        )
