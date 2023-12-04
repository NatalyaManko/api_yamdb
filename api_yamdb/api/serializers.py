import re
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from django.shortcuts import get_object_or_404
from reviews.models import Review, Title, Category, Genre, Comment
from users.models import User
from django.db.models import Avg


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )


class MeSerializer(UsersSerializer):
    role = serializers.CharField(read_only=True)


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254,
                                   required=True)
    username = serializers.CharField(max_length=150,
                                     required=True)

    class Meta:
        model = User
        fields = (
            'email',
            'username'
        )

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError('me - недопустимое'
                                              'имя пользователя')
        if re.search(r'^[\w.@+-]+\Z', data['username']) is None:
            raise serializers.ValidationError('Недопустимые символы')
        return data


class GetTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code'
        )


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    def validate(self, data):
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        author = self.context.get('request').user.id
        if self.context.get('request').method == 'POST':
            if not title.reviews_title.filter(author=author, title=title).exists():
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

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


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
        fields = ('id', 'name', 'year', 'rating', 'description', 'category', 'genre',)

    def get_rating(self, obj):
        score = Review.objects.filter(
            title=obj).aggregate(rating=(Avg('score')))
        return int(score['rating'] if score['rating'] else 0)
