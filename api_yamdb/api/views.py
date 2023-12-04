
from rest_framework import viewsets, filters

from reviews.models import (Category,
                            Genre,
                            Title,
                            Comment,
                            )

from .permissions import IsOwnerOrReadOnly
from .serializers import (CategorySerializer,
                          GenresSerializer,
                          TitleSerializer,)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    permission_classes = (IsOwnerOrReadOnly,)
    search_fields = ('name',)


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer
    filter_backends = (filters.SearchFilter,)
    permission_classes = (IsOwnerOrReadOnly,)
    search_fields = ('name',)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (filters.SearchFilter,)
    permission_classes = (IsOwnerOrReadOnly,)
    search_fields = ('name', 'year',)
