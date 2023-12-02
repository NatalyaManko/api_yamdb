from django.shortcuts import render
from rest_framework import viewsets
from reviews import (Category,
                     Genres,
                     Titles)


class CategoryViewSet(viewsets.ModelViewSet):
   queryset = Category.objects.all()


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()




