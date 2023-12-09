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
        help_text=_('Required. 150 characters or fewer.'
                    'Letters, digits and @/./+/-/_ only.'),
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(
        _('email address'),
        max_length=254,
        unique=True
    )
    bio = models.TextField(
        _('Биография'),
        blank=True
    )
    role = models.CharField(
        _('Роль пользователя'),
        max_length=30,
        choices=ROLES,
        default='user'
    )
    confirmation_code = models.CharField(
        _('код подтверждения'),
        max_length=255,
        null=True
    )
    first_name = models.CharField(
        _('имя'),
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        _('фамилия'),
        max_length=150,
        blank=True
    )

    @property
    def is_user(self):
        return self.role == 'user'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    @property
    def is_admin(self):
        return self.role == 'admin'

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
