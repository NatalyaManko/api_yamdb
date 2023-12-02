from rest_framework import serializers
from rest_framework.relations import SlugRelatedField, StringRelatedField
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from reviews.models import Review, Title, Category, Genre


User = get_user_model()


class ReviewSerializer(serializers.ModelSerializer):
#    author = SlugRelatedField(
#        read_only=True,
#        slug_field='username',
#        default=serializers.CurrentUserDefault()
#    )
    title = serializers.HiddenField(
        default=serializers.CreateOnlyDefault(Title))
        
    class Meta:
        model = Review
        fields = '__all__'
        validators = (
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title'),
                message=('Вы уже поставили оценку произведению!')
            ),
        )
            

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug',)
        model = Category


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug',)
        model = Genre


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Title
        fields = ('name', 'year', 'description',
                  'genre', 'category',)
