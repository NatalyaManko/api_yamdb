from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

from reviews.models import (Category, Genres, Titles)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug',)
        model = Category



class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug',)
        model = Genres


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Titles
        fields = ('name', 'year', 'description',
                  'genre', 'category',)

