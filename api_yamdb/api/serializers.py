import re

from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class UsersSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя для действий с
       использованием прав администратора"""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )


class MeSerializer(UsersSerializer):
    """Сериализатор пользователя для действий с
       использованием прав администратора"""

    role = serializers.CharField(read_only=True)


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя"""
    
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
    """Сериализатор для регистрации пользователя"""
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code'
        )


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор Отзывов"""
    
    author = SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    def validate(self, data):
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        author = self.context.get('request').user
        if self.context.get('request').method == 'POST':
            if Review.objects.filter(author=author, title=title).exists():
                raise serializers.ValidationError(
                    f'Вы уже оценили произведение: {title}!')
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


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор Жанров"""
    
    class Meta:
        fields = ('name', 'slug',)
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор Чтение данных произведений"""
    
    genre = GenreSerializer(many=True,
                            read_only=False)
    category = CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        score = Review.objects.filter(
            title=obj
        ).aggregate(rating=(Avg('score')))
        return int(score['rating']) if score['rating'] else None

    class Meta:
        model = Title
        fields = ('id',
                  'name',
                  'year',
                  'rating',
                  'description',
                  'genre',
                  'category')


class TitleCreateSerializer(serializers.ModelSerializer):
    """Сериализатор Произведений"""
    
    genre = serializers.SlugRelatedField(slug_field='slug',
                                         many=True,
                                         read_only=False,
                                         queryset=Genre.objects.all())
    category = serializers.SlugRelatedField(read_only=False,
                                            required=True,
                                            slug_field='slug',
                                            queryset=Category.objects.all())

    class Meta:
        model = Title
        fields = ('id',
                  'name',
                  'year',
                  'description',
                  'genre',
                  'category')
