from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from reviews import (Category,
                     Genres,
                     Titles)

from api_yamdb.api import serializers
from api_yamdb.api.serializers import CategorySerializer, GenresSerializer, TitleSerializer


class CategoryViewSet(viewsets.ModelViewSet):
   queryset = Category.objects.all()
   serializer_class = CategorySerializer
   filter_backends = (filters.SearchFilter,)
   search_fields = ('')


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    filter_backends = (filters.SearchFilter,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitleSerializer






