from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Categories(models.Model):
    name = models.CharField(max_length=256,
                            verbose_name='Название категории',
                            unique=True, blank=False)
    slug = models.SlugField(unique=True,
                            verbose_name='Slug категории',
                            blank=False)

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название жанра')
    slug = models.SlugField(unique=True, verbose_name='Slug жанра')


class Titles(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL,
                                 related_name='titles', null=True, blank=True)
    name = models.CharField(max_length=256,
                            verbose_name='Название произведения',
                            blank=False)
    year = models.IntegerField(verbose_name='Год произведения',
                               blank=False)
    description = models.TextField(blank=False,
                                   verbose_name='Описание произведения')

    def __str__(self):
        return self.name


class GenreTitles(models.Model):
    genre = models.ForeignKey(Genres,
                              on_delete=models.CASCADE,
                              blank=False,
                              related_name='genre')
    title = models.ForeignKey(Titles,
                              on_delete=models.CASCADE,
                              blank=False,
                              related_name='title'
                              )

    class Meta:
        unique_together = ('genre', 'title',)

    def __str__(self):
        return self.title


class Reviews(models.Model):
    pass


class Comments(models.Model):
    pass

