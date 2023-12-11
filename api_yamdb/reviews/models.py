import datetime

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from rest_framework import serializers

User = get_user_model()


def validate_year(data):
    if isinstance(data, int):
        if data > datetime.date.today().year:
            serializers.ValidationError(
                'Год не может быть больше текущего')
    else:
        serializers.ValidationError('Год должен быть числом!!!')
    return data


class Category(models.Model):
    """Модель Категорий"""

    name = models.CharField(max_length=256,
                            verbose_name='Название категории',
                            unique=True)
    slug = models.SlugField(unique=True,
                            verbose_name='Slug категории')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель Жанров"""

    name = models.CharField(max_length=256,
                            verbose_name='Название жанра')
    slug = models.SlugField(unique=True,
                            verbose_name='Slug жанра')

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Модель Произведений"""

    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 related_name='category')
    name = models.CharField(max_length=256,
                            verbose_name='Название произведения')
    year = models.PositiveSmallIntegerField(verbose_name='Год произведения',
                                            validators=[validate_year,])
    description = models.TextField(blank=True,
                                   verbose_name='Описание произведения')
    genre = models.ManyToManyField(Genre,
                                   verbose_name='Жанры произведений',
                                   through='TitleGenre')

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель Отзыв к произведению"""

    text = models.TextField('Текст отзыва')
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews_title',
        verbose_name='Произведение',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва'
    )
    score = models.PositiveSmallIntegerField(
        'Оценка произведения',
        validators=[
            MinValueValidator(
                1, message='Ожидается оценка от 1 до 10'),
            MaxValueValidator(
                10, message='Ожидается оценка от 1 до 10')
        ]
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author',
            )
        ]
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text[:50]


class Comment(models.Model):
    """Модель Комментарий к отзыву"""

    text = models.TextField('Текст комментария')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('pub_date',)
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:30]


class TitleGenre(models.Model):
    """Модель Связи произведений и жанров"""

    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='genre',
        verbose_name='Жанр'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='title',
        verbose_name='Произведение'
    )

    def __str__(self):
        return f'{self.title} {self.genre}'
