from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from django.shortcuts import get_object_or_404
from reviews.models import Review, Title, Category, Genre, Comment
from users.models import User
from django.db.models import Avg


class ReviewSerializer(serializers.ModelSerializer):
#    author = SlugRelatedField(
#        read_only=True,
#        slug_field='username',
#        default=serializers.CurrentUserDefault()
#    )
#    title = serializers.HiddenField(
#        default=serializers.CreateOnlyDefault(Title))
    
    def validate(self, data):
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        author = self.context.get('request').user.id
        if self.context.get('request').method == 'POST':
            if not title.reviews_title.filter(author=author).exists():
                raise serializers.ValidationError(
                    f'Вы уже оценили произведение: {title}!'
                    )
            return data
        return data

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')


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
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'category', 'genre',)
        model = Title
        fields = ('name', 'year', 'rating', 'description',
                  'genre', 'category')

    def get_rating(self, obj):
        score = Review.objects.filter(
            title=obj).aggregate(rating=(Avg('score')))
        return int(score['rating'])
