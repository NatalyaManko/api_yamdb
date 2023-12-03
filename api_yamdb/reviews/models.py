from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Categories(models.Model):
    """Модель Категорий"""
    name = models.CharField(max_length=256,
                            verbose_name='Название категории',
                            unique=True, blank=False)
    slug = models.SlugField(unique=True,
                            verbose_name='Slug категории',
                            blank=False)

    def __str__(self):
        return self.name


class Genres(models.Model):
    """Модель Жанров"""
    name = models.CharField(max_length=256,
                            verbose_name='Название жанра')
    slug = models.SlugField(unique=True,
                            verbose_name='Slug жанра')


class Titles(models.Model):
    """Модель Произведений"""
    category = models.ForeignKey(Categories,
                                 on_delete=models.SET_NULL,
                                 related_name='category', null=True, blank=True)
    name = models.CharField(max_length=256,
                            verbose_name='Название произведения',
                            blank=False)
    year = models.IntegerField(verbose_name='Год произведения',
                               blank=False)
    description = models.TextField(blank=True,
                                   verbose_name='Описание произведения')
    genres = models.ManyToManyField(Genres,
                                    verbose_name="Жанры произведений",
                                    blank=False)

    def __str__(self):
        return self.name


class Reviews(models.Model):
    pass


class Comments(models.Model):
    pass

