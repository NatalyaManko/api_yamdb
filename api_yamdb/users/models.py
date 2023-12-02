from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLES = (
        ('user', 'Пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор'),
    )
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        max_length=9,
        choices=ROLES,
        default='user'
    )
