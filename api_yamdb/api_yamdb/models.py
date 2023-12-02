from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Categories(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)


class Titles(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL,
                                 related_name='titles', null=True, blank=True)
    genre = models.ForeignKey(Genres, on_delete=models.SET_NULL,
                              related_name='titles', null=True, blank=True)
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.name


class Reviews(models.Model):
    pass


class Comments(models.Model):
    pass

