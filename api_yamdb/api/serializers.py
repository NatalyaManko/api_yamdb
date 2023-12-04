from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

from reviews.models import (Category, Genre,
                            Title, )


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор Категорий"""
    class Meta:
        fields = ('name', 'slug',)
        model = Category


class GenresSerializer(serializers.ModelSerializer):
    """Сериализатор Жанров"""
    class Meta:
        fields = ('name', 'slug',)
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор Произведений"""
    genre = GenresSerializer(many=True,
                             read_only=False, required=False)
    category = CategorySerializer(read_only=True,
                                  many=False)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'category', 'genre',)
