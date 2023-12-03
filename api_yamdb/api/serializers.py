from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Review, Title, Category, Genre, Comment
from users.models import User
from django.db.models import Avg


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    title = serializers.HiddenField(
        default=serializers.CreateOnlyDefault(Title))
        
    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pu_date', 'title',)


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев"""
    author = SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    review = serializers.HiddenField(
        default=serializers.CreateOnlyDefault(Review))

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date', 'review',)



class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug',)
        model = Category


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug',)
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('name', 'year', 'rating', 'description',
                  'genre', 'category')

    def get_rating(self, obj):
        score = Review.objects.filter(
            title=obj).aggregate(rating=(Avg('score')))
        return int(score['rating'])
