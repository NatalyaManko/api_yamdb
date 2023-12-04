from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters

from reviews.models import (Category,
                            Genre,
                            Title,
                            Comment,
                            )

from .permissions import IsOwnerOrReadOnly
from .serializers import (CategorySerializer,
                          GenreSerializer,
                          TitleSerializer,)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    permission_classes = (IsOwnerOrReadOnly,)
    search_fields = ('name',)


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    permission_classes = (IsOwnerOrReadOnly,)
    search_fields = ('name',)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (IsOwnerOrReadOnly,)
    filterset_fields = ('category__slug', 'genres__slug',
                        'name', 'year')
