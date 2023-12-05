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
        validators=(AbstractUser.username_validator, validate_username,),
        max_length=150,
        unique=True,
        blank=False,
        null=False,
        help_text=_('Required. 150 characters or fewer.'
                    'Letters, digits and @/./+/-/_ only.'),
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    email = models.EmailField(
        _('email address'),
        max_length=254,
        unique=True,
        blank=False,
        null=False
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
    first_name = models.CharField(
        'имя',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        'фамилия',
        max_length=150,
        blank=True
    )

    REQUIRED_FIELDS = []

    @property
    def is_user(self):
        return self.role == 'user'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    @property
    def is_admin(self):
        return self.role == 'admin'
