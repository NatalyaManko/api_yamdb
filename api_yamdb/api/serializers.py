from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

from reviews.models import (Category, Genres, Titles)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Category


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '_all__'
        model = Genres


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Titles
        fields = '__all__'
