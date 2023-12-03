from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

from reviews.models import (Categories, Genres,
                            Titles, )


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор Категорий"""
    class Meta:
        fields = ('name', 'slug',)
        model = Categories


class GenresSerializer(serializers.ModelSerializer):
    """Сериализатор Жанров"""
    class Meta:
        fields = ('name', 'slug',)
        model = Genres


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор Произведений"""
    genre = GenresSerializer(many=True,
                             read_only=False, required=False)
    category = CategorySerializer(read_only=True,
                                  many=False)

    class Meta:
        model = Titles
        fields = ('id', 'name', 'year', 'description', 'category', 'genre',)
