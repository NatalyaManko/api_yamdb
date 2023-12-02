from rest_framework import serializers
from rest_framework.relations import SlugRelatedField, StringRelatedField
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth import get_user_model

from reviews.models import Review, Title, Category, Genre


User = get_user_model()


class ReviewSerializer(serializers.ModelSerializer):
    #author = SlugRelatedField(
#        read_only=True,
 #       slug_field='username',
  #      default=serializers.CurrentUserDefault()
   # )
    title = serializers.HiddenField(default='auto_replace_me')

    class Meta:
        model = Review
        fields = '__all__'
       # read_only_fields = ('title',)
        validators = (
            UniqueTogetherValidator(
               queryset=Review.objects.all(),
               fields=('title', 'author'),
               message=('Вы уже оценили произведение!')
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
