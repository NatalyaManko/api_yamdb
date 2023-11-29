from django.shortcuts import render, get_object_or_404

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from reviews.models import Title
from .serializers import ReviewSerializer
from .permissions import IsAuthorPermission


class ReviewViewSet(viewsets.ModelViewSet):
    """Изменить или удалить отзыв может только автор."""
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorPermission]

    def get_queryset(self):
        title_id = get_object_or_404(Title, pk=self.kwargs['title_pk'])
        return title_id.reviews.all()

    def perform_create(self, serializer):
        title_id = get_object_or_404(Title, pk=self.kwargs.get('title_pk'))
        serializer.save(author=self.request.user, title=title_id)
