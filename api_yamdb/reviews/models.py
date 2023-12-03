from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)


class Title(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='titles', null=True, blank=True
        )
    genre = models.ForeignKey(
        Genre, on_delete=models.SET_NULL,
        related_name='titles', null=True, blank=True
        )
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.TextField()

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
