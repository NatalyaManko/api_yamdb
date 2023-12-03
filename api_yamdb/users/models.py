from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.validators import validate_username

ROLES = (
        ('user', 'Пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор'),
)


class User(AbstractUser):
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer.'
                    'Letters, digits and @/./+/-/_ only.'),
        validators=[AbstractUser.username_validator, validate_username],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    email = models.EmailField(
        _('email address'),
        unique=True
    )

    bio = models.TextField(
        _('Биография'),
        blank=True
    )

    role = models.CharField(
        _('Роль пользователя'),
        max_length=9,
        choices=ROLES,
        default='user',
        blank=True
    )
    confirmation_code = models.CharField(
        _('код подтверждения'),
        max_length=8,
        blank=False,
        null=True
    )

    REQUIRED_FIELDS = []
