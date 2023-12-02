from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, )


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
    rating = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.TextField('Текст')
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
        verbose_name='Автор'
        )
    score = models.PositiveSmallIntegerField(
        'Оценка',
        validators=[MaxValueValidator(10),
                    MinValueValidator(1)]
        )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ('pub_date',)
#        constraints = [
#            models.UniqueConstraint(
#                fields=['title', 'author'],
#                name='unique_title_author'
#            )
#        ]
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'


class Comment(models.Model):
    pass

