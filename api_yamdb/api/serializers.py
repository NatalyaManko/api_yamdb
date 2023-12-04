import datetime

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


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор Жанров"""
    class Meta:
        fields = ('name', 'slug',)
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор Произведений"""
    genres = GenreSerializer(many=True,
                             read_only=False, required=True)
    category = CategorySerializer(read_only=False,
                                  many=False,
                                  required=True)
    year = serializers.IntegerField(required=True)
    name = serializers.CharField(required=True)

    def validate(self, data):
        if data['year'] > datetime.date.year:
            raise serializers.ValidationError(
                'Дата произведения не может быть будущим годом!'
            )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'category', 'genres',)
