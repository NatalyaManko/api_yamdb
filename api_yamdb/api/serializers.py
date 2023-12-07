import datetime
import re
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from django.shortcuts import get_object_or_404
from reviews.models import (Review, Title, Category,
                            Genre, Comment, TitleGenre)
from datetime import date
from django.db.models import Avg

User = get_user_model()


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
        author = self.context.get('request').user
        if self.context.get('request').method == 'POST':
            if Review.objects.filter(author=author, title=title).exists():  # поменядлы
                raise serializers.ValidationError(
                    f'Вы уже оценили произведение: {title}!'
                    )
            return data
        return data
#        if self.context.get('request').method == 'PUT':
 #           raise serializers.ValidationError(
  #                  f'PUT-запрос не предусмотрен!'
   #                 )
    #    return data

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

#    def get_kwargs_create(self, data):
#        return self.context.get('view').kwargs.get('review_id') # Проверить еще раз создание коммента

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
    """Сериализатор Произведений"""
    genre = GenreSerializer(many=True,
                             read_only=False)
    category = CategorySerializer(read_only=True,)
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
                                         read_only=True)
    category = serializers.SlugRelatedField(read_only=True, slug_field='slug')

    def validate(self, data):
        if isinstance(data['year'], int):
            if data['year'] > datetime.date.today().year:
                serializers.ValidationError(
                    'Год не быть больше текущего')
        else:
            serializers.ValidationError('Год должен быть числом!!!')
        return data

    def save(self, **validated_data):
        data = validated_data.get('data')
        genres = data.pop('genre')
        category_slug = data.pop('category')
        category, status = Category.objects.get_or_create(slug=category_slug)
        title = Title.objects.create(**data, category=category)

        for slug_genre in genres:
            current_genre, status = Genre.objects.get_or_create(slug=slug_genre)
            TitleGenre.objects.create(genre=current_genre,
                                      title=title)
        return title

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
                  'description',
                 'genre',
                  'category')
