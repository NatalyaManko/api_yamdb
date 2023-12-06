from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Category(models.Model):
    """Модель Категорий"""
    name = models.CharField(max_length=256,
                            verbose_name='Название категории',
                            unique=True, blank=False)
    slug = models.SlugField(unique=True,
                            verbose_name='Slug категории',
                            blank=False)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель Жанров"""
    name = models.CharField(max_length=256,
                            verbose_name='Название жанра')
    slug = models.SlugField(unique=True,
                            verbose_name='Slug жанра')


class Title(models.Model):
    """Модель Произведений"""
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 related_name='titles_category',
                                 verbose_name='Категории произведений')
    name = models.CharField(max_length=256,
                            verbose_name='Название произведения',
                            blank=False)
    year = models.IntegerField(verbose_name='Год произведения',
                               blank=False)
    description = models.TextField(blank=True,
                                   verbose_name='Описание произведения')
    genre = models.ManyToManyField(Genre,
                                   related_name='titles_genre',
                                   verbose_name='Жанры произведений')
    rating = models.PositiveIntegerField(null=True,
                                         verbose_name='Рейтинг произведений')

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
