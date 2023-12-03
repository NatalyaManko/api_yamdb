from django.shortcuts import render, get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from reviews.models import Title, Review
from .serializers import ReviewSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework import viewsets, permissions, filters
from reviews.models import (Category, Genre, Title, Comment)
from .serializers import CategorySerializer, GenresSerializer, TitleSerializer, CommentSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Изменить или удалить отзыв может только автор."""
    serializer_class = ReviewSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('text', 'author', 'score')
 #   permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        title_id = get_object_or_404(Title, pk=self.kwargs['title_id'])
        return title_id.reviews_title.all()

    def perform_create(self, serializer):
        title_id = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(title=title_id) #author=self.request.user, 


class CommentViewSet(viewsets.ModelViewSet):
    """Изменить или удалить комментарий может только автор."""
    serializer_class = CommentSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('text', 'author')
 #   permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorPermission]

    def get_queryset(self):
        review_id = get_object_or_404(Review, pk=self.kwargs['review_pk'])
        return review_id.comments.all()

    def perform_create(self, serializer):
        review_id = get_object_or_404(Review, pk=self.kwargs.get('review_pk'))
        serializer.save(author=self.request.user, review=review_id)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('')


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer
    filter_backends = (filters.SearchFilter,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
